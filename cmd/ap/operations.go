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

type updateResultMsg struct {
	out string
	err error
}

func runUpdateCmd() tea.Cmd {
	projectRoot := resolveProjectRoot()
	updateScript := filepath.Join(projectRoot, "update.sh")
	if _, err := os.Stat(updateScript); err != nil {
		return warnCmd(T("no_update_script"), projectRoot)
	}
	return func() tea.Msg {
		cmdUpdate := exec.Command("bash", updateScript)
		cmdUpdate.Dir = projectRoot
		out, err := cmdUpdate.CombinedOutput()
		return updateResultMsg{out: string(out), err: err}
	}
}

func runSelfUpdateCmd() tea.Cmd {
	projectRoot := resolveProjectRoot()
	script := fmt.Sprintf(`
set -e
OS="$(uname -s)"
if [ "$OS" = "Linux" ]; then
    ARCHIVE="AleniaPorter-Linux.tar.gz"
elif [ "$OS" = "Darwin" ]; then
    ARCHIVE="AleniaPorter-macOS.zip"
else
    ARCHIVE="AleniaPorter-Windows.zip"
fi

URL="https://github.com/Kaia-Alenia/Alenia-Porter/releases/latest/download/${ARCHIVE}"

if command -v curl &> /dev/null; then
    curl -L "$URL" -o "/tmp/${ARCHIVE}"
elif command -v wget &> /dev/null; then
    wget -q --show-progress "$URL" -O "/tmp/${ARCHIVE}"
else
    echo "%[3]s"
    exit 1
fi

rm -rf "/tmp/porter_update_temp"
mkdir -p "/tmp/porter_update_temp"

if [ "$OS" = "Linux" ]; then
    tar -xzf "/tmp/${ARCHIVE}" -C "/tmp/porter_update_temp"
else
    unzip -o "/tmp/${ARCHIVE}" -d "/tmp/porter_update_temp"
fi

# Buscar el directorio interno
EXTRACTED_DIR="/tmp/porter_update_temp"
INNER_DIR=$(ls -d /tmp/porter_update_temp/*/ 2>/dev/null | head -n 1 || true)
if [ -n "$INNER_DIR" ]; then
    EXTRACTED_DIR="$INNER_DIR"
fi

rm -f "%[1]s/porter" "%[1]s/ap" "%[1]s/AleniaPorter" "%[1]s/AleniaPorter.exe"
cp -a "$EXTRACTED_DIR/." "%[1]s/"
chmod +x "%[1]s/ap" 2>/dev/null || true
if [ -f "%[1]s/ap" ]; then
    cp -a "%[1]s/ap" "%[1]s/porter"
fi
chmod +x "%[1]s/porter" "%[1]s/AleniaPorter" 2>/dev/null || true

if [ -d "$HOME/.local/share/porter" ]; then
    rm -f "$HOME/.local/share/porter/porter"
    cp -a "$EXTRACTED_DIR/." "$HOME/.local/share/porter/"
    chmod +x "$HOME/.local/share/porter/porter" "$HOME/.local/share/porter/AleniaPorter" 2>/dev/null || true
fi
if [ -d "$HOME/.alenia-porter" ]; then
    rm -f "$HOME/.alenia-porter/porter"
    cp -a "$EXTRACTED_DIR/." "$HOME/.alenia-porter/"
    chmod +x "$HOME/.alenia-porter/porter" "$HOME/.alenia-porter/AleniaPorter" 2>/dev/null || true
fi
rm -rf "/tmp/${ARCHIVE}" "/tmp/porter_update_temp"
echo "%[2]s"
`, projectRoot, T("update_success_msg"), T("update_error_no_curl"))

	return func() tea.Msg {
		cmdUpdate := exec.Command("bash", "-c", script)
		cmdUpdate.Dir = projectRoot
		out, err := cmdUpdate.CombinedOutput()
		return updateResultMsg{out: string(out), err: err}
	}
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

func getEngineCmd(baseArgs []string) *exec.Cmd {
	projectRoot := resolveProjectRoot()

	// Check for Windows executable
	winExe := filepath.Join(projectRoot, "AleniaPorter.exe")
	if _, err := os.Stat(winExe); err == nil {
		return exec.Command(winExe, append([]string{"--cli-engine"}, baseArgs...)...)
	}

	// Check for Linux executable
	linExe := filepath.Join(projectRoot, "AleniaPorter")
	if _, err := os.Stat(linExe); err == nil {
		return exec.Command(linExe, append([]string{"--cli-engine"}, baseArgs...)...)
	}

	// Check for macOS App Bundle executable
	macExe := filepath.Join(projectRoot, "AleniaPorter.app", "Contents", "MacOS", "AleniaPorter")
	if _, err := os.Stat(macExe); err == nil {
		return exec.Command(macExe, append([]string{"--cli-engine"}, baseArgs...)...)
	}

	// Fallback for development: use python3
	srcPath := filepath.Join(projectRoot, "src")
	if _, err := os.Stat(filepath.Join(srcPath, "alenia_porter")); err != nil {
		srcPath = filepath.Join(projectRoot, "src")
	}
	env := append(os.Environ(), "PYTHONPATH="+srcPath)

	pythonArgs := append([]string{"-m", "alenia_porter.headless"}, baseArgs...)
	cmd := exec.Command("python3", pythonArgs...)
	cmd.Env = env
	return cmd
}

func startEngineCmd(dir, video, vExtra, audio, aExtra, image, iExtra string, setEngineState func(*exec.Cmd, *bufio.Scanner)) tea.Cmd {
	cmdArgs := []string{dir, "--vformat", video, "--aformat", audio, "--iformat", image}
	if vExtra != "" {
		cmdArgs = append(cmdArgs, "--vextra", vExtra)
	}
	if aExtra != "" {
		cmdArgs = append(cmdArgs, "--aextra", aExtra)
	}
	if iExtra != "" {
		cmdArgs = append(cmdArgs, "--iextra", iExtra)
	}

	engineCmd := getEngineCmd(cmdArgs)
	stdout, err := engineCmd.StdoutPipe()
	if err != nil {
		return failCmd(T("stream_error"), err)
	}
	engineCmd.Stderr = os.Stderr
	if err := engineCmd.Start(); err != nil {
		return failCmd(T("engine_error"), err)
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
	optimizeCmd.Usage = func() {
		fmt.Printf("%s\n\n%s:\n", T("cli_usage_optimize"), T("cli_options"))
		optimizeCmd.PrintDefaults()
	}
	optV := optimizeCmd.String("vformat", "mp4", T("cli_target_video"))
	optA := optimizeCmd.String("aformat", "mp3", T("cli_target_audio"))
	optI := optimizeCmd.String("iformat", "webp", T("cli_target_image"))
	optVExtra := optimizeCmd.String("vextra", "", T("cli_extra_video"))
	optAExtra := optimizeCmd.String("aextra", "", T("cli_extra_audio"))
	optIExtra := optimizeCmd.String("iextra", "", T("cli_extra_image"))
	optL := optimizeCmd.String("lang", currentLang, T("cli_lang"))
	if err := optimizeCmd.Parse(os.Args[2:]); err != nil {
		os.Exit(2)
	}
	if !applyLanguage(*optL) {
		warn(T("unsupported_lang"), *optL)
	}
	args := optimizeCmd.Args()
	if len(args) < 1 {
		fail(T("invalid_dir"))
		os.Exit(1)
	}
	runEngine(args[0], *optV, *optVExtra, *optA, *optAExtra, *optI, *optIExtra)
}

func runEngine(targetDir, videoFormat, vExtra, audioFormat, aExtra, imageFormat, iExtra string) {
	fmt.Println()
	info(T("engine_start"))

	cmdArgs := []string{targetDir, "--vformat", videoFormat, "--aformat", audioFormat, "--iformat", imageFormat}
	if vExtra != "" {
		cmdArgs = append(cmdArgs, "--vextra", vExtra)
	}
	if aExtra != "" {
		cmdArgs = append(cmdArgs, "--aextra", aExtra)
	}
	if iExtra != "" {
		cmdArgs = append(cmdArgs, "--iextra", iExtra)
	}

	cmd := getEngineCmd(cmdArgs)
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		fail(T("stream_error"), err)
		return
	}
	cmd.Stderr = os.Stderr
	if err := cmd.Start(); err != nil {
		fail(T("engine_error"), err)
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
		warn(T("stream_error"), err)
		fmt.Println()
	}
	if err := cmd.Wait(); err != nil {
		fmt.Println()
		fail(T("engine_error"), err)
		fmt.Println()
	}
}

func handleMeCommand() {
	loadCLIConfig()
	fmt.Println(T("me_profile_title"))
	fmt.Printf("%s %s\n", T("me_nick_current"), currentConfig.Nickname)
	fmt.Printf("%s %s\n", T("me_uuid"), currentConfig.Uuid)
	fmt.Printf("%s %t\n\n", T("me_telemetry_status"), currentConfig.TelemetryEnabled)

	var changeNickname string
	var newNickname string
	var telemetry bool = currentConfig.TelemetryEnabled

	form := huh.NewForm(
		huh.NewGroup(
			huh.NewSelect[string]().
				Title(T("me_change_nick_prompt")).
				Options(
					huh.NewOption(T("yes"), "yes"),
					huh.NewOption(T("no"), "no"),
				).
				Value(&changeNickname),
		),
	)
	err := form.Run()
	if err != nil {
		return
	}

	if changeNickname == "yes" {
		form2 := huh.NewForm(
			huh.NewGroup(
				huh.NewInput().
					Title(T("me_new_nick")).
					Value(&newNickname),
			),
		)
		form2.Run()
		if newNickname != "" {
			currentConfig.Nickname = newNickname
		}
	}

	form3 := huh.NewForm(
		huh.NewGroup(
			huh.NewConfirm().
				Title(T("me_tel_prompt")).
				Value(&telemetry),
		),
	)
	form3.Run()

	currentConfig.TelemetryEnabled = telemetry
	saveCLIConfig()
	fmt.Println(T("me_saved"))
}
