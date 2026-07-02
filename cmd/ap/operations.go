package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/huh"
)

func resolveProjectRoot() string {
	candidates := []string{}
	if exePath, err := os.Executable(); err == nil {
		if realPath, err := filepath.EvalSymlinks(exePath); err == nil {
			candidates = append(candidates, filepath.Dir(realPath))
		} else {
			candidates = append(candidates, filepath.Dir(exePath))
		}
	}
	if cwd, err := os.Getwd(); err == nil {
		candidates = append(candidates, cwd)
	}
	visited := map[string]struct{}{}
	for _, start := range candidates {
		dir := start
		for {
			if _, ok := visited[dir]; ok {
				break
			}
			visited[dir] = struct{}{}
			if _, err := os.Stat(filepath.Join(dir, "go.mod")); err == nil {
				return dir
			}
			if _, err := os.Stat(filepath.Join(dir, "src", "alenia_porter")); err == nil {
				return dir
			}
			parent := filepath.Dir(dir)
			if parent == dir {
				break
			}
			dir = parent
		}
	}
	if len(candidates) > 0 {
		return candidates[0]
	}
	return "."
}

type quitMsg struct{}
type errorMsg struct{ err error }

func runUpdateCmd() tea.Cmd {
	projectRoot := resolveProjectRoot()
	updateScript := filepath.Join(projectRoot, "update.sh")
	if _, err := os.Stat(updateScript); err != nil {
		return warnCmd(T("no_update_script"), projectRoot)
	}
	cmdUpdate := exec.Command("bash", updateScript)
	cmdUpdate.Dir = projectRoot
	return tea.ExecProcess(cmdUpdate, func(err error) tea.Msg {
		if err != nil {
			return errorMsg{err}
		}
		return quitMsg{}
	})
}

func runSelfUpdateCmd() tea.Cmd {
	projectRoot := resolveProjectRoot()
	script := `
set -e
git pull --rebase --autostash
go build -o ap ./cmd/ap
`
	cmdUpdate := exec.Command("bash", "-c", script)
	cmdUpdate.Dir = projectRoot
	return tea.ExecProcess(cmdUpdate, func(err error) tea.Msg {
		if err != nil {
			return errorMsg{err}
		}
		return quitMsg{}
	})
}

func cleanPath(p string) string {
	p = strings.TrimSpace(p)
	p = strings.Trim(p, "'\"")
	return p
}

// NewDirForm — Fase 1: solo pide el directorio
func NewDirForm() *huh.Form {
	form := huh.NewForm(
		huh.NewGroup(
			huh.NewInput().
				Key("dir").
				Title(T("enter_dir")).
				Placeholder(T("dir_ph")).
				Description(T("dir_desc")),
		),
	)
	return form
}

// NewFormatsForm — Fase 2: selección de formatos uno por uno
// Solo incluye grupos para los tipos de archivo que existen en el dir
func NewFormatsForm(hasVideo, hasAudio, hasImage bool) *huh.Form {
	var groups []*huh.Group

	if hasVideo {
		groups = append(groups, huh.NewGroup(
			huh.NewSelect[string]().
				Key("video").
				Title(T("target_video")).
				Description(T("vid_desc")).
				Options(huhChoices(videoFormats)...).
				Value(ptr(defaultChoice(videoFormats, "mp4"))),
		))
	}

	if hasAudio {
		groups = append(groups, huh.NewGroup(
			huh.NewSelect[string]().
				Key("audio").
				Title(T("target_audio")).
				Description(T("aud_desc")).
				Options(huhChoices(audioFormats)...).
				Value(ptr(defaultChoice(audioFormats, "mp3"))),
		))
	}

	if hasImage {
		groups = append(groups, huh.NewGroup(
			huh.NewSelect[string]().
				Key("image").
				Title(T("target_image")).
				Description(T("img_desc")).
				Options(huhChoices(imageFormats)...).
				Value(ptr(defaultChoice(imageFormats, "webp"))),
		))
	}

	if len(groups) == 0 {
		// fallback — no debería ocurrir
		groups = append(groups, huh.NewGroup(
			huh.NewSelect[string]().
				Key("video").
				Title(T("target_video")).
				Options(huhChoices(videoFormats)...).
				Value(ptr(defaultChoice(videoFormats, "mp4"))),
		))
	}

	return huh.NewForm(groups...)
}

// NewOptimizeForm queda como alias de compatibilidad (modo directo)
func NewOptimizeForm() *huh.Form {
	return NewDirForm()
}


type engineProgressMsg struct {
	text string
	err  error
	done bool
}

func startEngineCmd(dir, video, vExtra, audio, aExtra, image, iExtra string, setEngineState func(*exec.Cmd, *bufio.Scanner)) tea.Cmd {
	cmdArgs := []string{"-m", "alenia_porter.headless", dir, "--vformat", video, "--aformat", audio, "--iformat", image}
	if vExtra != "" {
		cmdArgs = append(cmdArgs, "--vextra", vExtra)
	}
	if aExtra != "" {
		cmdArgs = append(cmdArgs, "--aextra", aExtra)
	}
	if iExtra != "" {
		cmdArgs = append(cmdArgs, "--iextra", iExtra)
	}
	projectRoot := resolveProjectRoot()
	srcPath := filepath.Join(projectRoot, "src")
	if _, err := os.Stat(filepath.Join(srcPath, "alenia_porter")); err != nil {
		srcPath = filepath.Join(projectRoot, "src")
	}
	env := append(os.Environ(), "PYTHONPATH="+srcPath)

	engineCmd := exec.Command("python3", cmdArgs...)
	engineCmd.Env = env
	stdout, err := engineCmd.StdoutPipe()
	if err != nil {
		return failCmd("Failed to create stdout pipe: %v", err)
	}
	engineCmd.Stderr = os.Stderr
	if err := engineCmd.Start(); err != nil {
		return failCmd("Failed to start optimization engine: %v", err)
	}

	scanner := bufio.NewScanner(stdout)
	setEngineState(engineCmd, scanner)
	
	return tea.Batch(
		infoCmd(T("engine_start")),
		readNextEngineLine(scanner),
	)
}

func readNextEngineLine(scanner *bufio.Scanner) tea.Cmd {
	return func() tea.Msg {
		if scanner.Scan() {
			return engineProgressMsg{text: scanner.Text()}
		}
		if err := scanner.Err(); err != nil {
			return engineProgressMsg{err: err, done: true}
		}
		return engineProgressMsg{done: true}
	}
}

// Keep direct execution intact for CLI flags
func runDirectOptimize() {
	optimizeCmd := flag.NewFlagSet("optimize", flag.ContinueOnError)
	optV := optimizeCmd.String("vformat", "mp4", "Target video format")
	optA := optimizeCmd.String("aformat", "mp3", "Target audio format")
	optI := optimizeCmd.String("iformat", "webp", "Target image format")
	optVExtra := optimizeCmd.String("vextra", "", "Extra video ffmpeg args")
	optAExtra := optimizeCmd.String("aextra", "", "Extra audio ffmpeg args")
	optIExtra := optimizeCmd.String("iextra", "", "Extra image ffmpeg args")
	optL := optimizeCmd.String("lang", currentLang, "UI language")
	if err := optimizeCmd.Parse(os.Args[2:]); err != nil {
		os.Exit(2)
	}
	if !applyLanguage(*optL) {
		warn("Unsupported language code: %s", *optL)
	}
	args := optimizeCmd.Args()
	if len(args) < 1 {
		fail("Target directory required.")
		os.Exit(1)
	}
	runEngine(args[0], *optV, *optVExtra, *optA, *optAExtra, *optI, *optIExtra)
}

func runEngine(targetDir, videoFormat, vExtra, audioFormat, aExtra, imageFormat, iExtra string) {
	fmt.Println()
	info(T("engine_start"))

	cmdArgs := []string{"-m", "alenia_porter.headless", targetDir, "--vformat", videoFormat, "--aformat", audioFormat, "--iformat", imageFormat}
	if vExtra != "" {
		cmdArgs = append(cmdArgs, "--vextra", vExtra)
	}
	if aExtra != "" {
		cmdArgs = append(cmdArgs, "--aextra", aExtra)
	}
	if iExtra != "" {
		cmdArgs = append(cmdArgs, "--iextra", iExtra)
	}
	projectRoot := resolveProjectRoot()
	srcPath := filepath.Join(projectRoot, "src")
	if _, err := os.Stat(filepath.Join(srcPath, "alenia_porter")); err != nil {
		srcPath = filepath.Join(projectRoot, "src")
	}
	env := append(os.Environ(), "PYTHONPATH="+srcPath)

	cmd := exec.Command("python3", cmdArgs...)
	cmd.Env = env
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fail("Failed to create stdout pipe: %v", err)
		return
	}
	cmd.Stderr = os.Stderr
	if err := cmd.Start(); err != nil {
		fail("Failed to start optimization engine: %v", err)
		return
	}

	scanner := bufio.NewScanner(stdout)
	for scanner.Scan() {
		line := scanner.Text()
		switch {
		case strings.HasPrefix(line, "PROGRESS:"):
			parts := strings.SplitN(line, ":", 2)
			if len(parts) == 2 {
				fmt.Printf("\r\033[K  %s %s", T("processing"), parts[1])
			}
		case strings.HasPrefix(line, "DONE:"):
			parts := strings.SplitN(line, ":", 3)
			fmt.Println()
			if len(parts) >= 2 {
				successMsg("%s %s", T("processed"), parts[1])
			}
			if len(parts) >= 3 {
				fmt.Printf("  %s%s:%s %s\n", Muted, T("output"), Reset, parts[2])
			}
			fmt.Println()
		case strings.HasPrefix(line, "ERROR:"):
			fmt.Println()
			fail("%s", strings.TrimPrefix(line, "ERROR:"))
			fmt.Println()
		default:
			fmt.Println("  " + line)
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Println()
		warn("Stream error: %v", err)
		fmt.Println()
	}
	if err := cmd.Wait(); err != nil {
		fmt.Println()
		fail("Engine exited with errors: %v", err)
		fmt.Println()
	}
}
