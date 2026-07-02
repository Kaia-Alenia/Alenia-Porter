package main

import (
	"bufio"
	"fmt"
	"os"
	"os/exec"
	"strings"

	"github.com/charmbracelet/bubbles/textinput"
	"github.com/charmbracelet/bubbles/viewport"
	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// ═══════════════════════════════════════════════════════════════════════════
// ESTADO DE FOCO
// ═══════════════════════════════════════════════════════════════════════════

type focusState int

const (
	InputFocus focusState = iota
	PaletteFocus
)

// ═══════════════════════════════════════════════════════════════════════════
// MODELO PRINCIPAL
// ═══════════════════════════════════════════════════════════════════════════

type optFlowState int

const (
	optStateNone optFlowState = iota
	optStateDir
	optStateVideo
	optStateAudio
	optStateImage
)

type mainModel struct {
	// Layout
	width  int
	height int

	// Zona 2: historial scrollable
	viewport viewport.Model
	messages []string

	// Zona 3: input
	textInput textinput.Model
	focus     focusState

	// Command palette (suggestions)
	allCmds      []cmdSuggestion
	filteredCmds []cmdSuggestion
	paletteIdx   int
	showPalette  bool

	// Sub-modelos (flujos huh)
	langModel tea.Model

	// Engine Python
	engineCmd       *exec.Cmd
	scanner         *bufio.Scanner
	processing      bool
	currentProgress string

	// Spinner
	spinnerIdx int

	// Historial de inputs del usuario
	inputHistory []string
	historyIdx   int

	// Estado pendiente para flujo de optimize
	optState    optFlowState
	optDir      string
	optVideo    string
	optVExtra   string
	optAudio    string
	optAExtra   string
	optImage    string
	optIExtra   string
	optPendingV int
	optPendingA int
	optPendingI int
}

func initialModel() mainModel {
	ti := textinput.New()
	ti.Placeholder = T("placeholder_main")
	ti.Prompt = stylePromptIcon.Render("❯") + " "
	ti.TextStyle = styleUserInput
	ti.PlaceholderStyle = styleMuted
	ti.Focus()
	ti.CharLimit = 512
	ti.Width = 80

	vp := viewport.New(80, 20)
	vp.Style = lipgloss.NewStyle()

	cmds := makeCommands()

	m := mainModel{
		textInput:    ti,
		viewport:     vp,
		allCmds:      cmds,
		filteredCmds: cmds,
		focus:        InputFocus,
		historyIdx:   -1,
	}

	// Mensaje de bienvenida inicial
	m = m.appendMessage(styleMuted.Render("  " + T("ready_msg")))
	return m
}

// ═══════════════════════════════════════════════════════════════════════════
// HELPERS DE MENSAJES
// ═══════════════════════════════════════════════════════════════════════════

func (m mainModel) appendMessage(msg string) mainModel {
	m.messages = append(m.messages, msg)
	
	content := strings.Join(m.messages, "\n")
	if m.currentProgress != "" {
		spinner := styleInfo.Render(spinnerFrames[m.spinnerIdx])
		progressLine := "  " + styleProgressLabel.Render(T("processing")) + " " + styleMuted.Render(m.currentProgress) + " " + spinner
		content += "\n\n" + progressLine
	}
	m.viewport.SetContent(content)
	m.viewport.GotoBottom()
	return m
}

func (m mainModel) appendInfo(format string, a ...interface{}) mainModel {
	msg := fmt.Sprintf("  "+styleInfo.Render("ℹ")+" "+format, a...)
	return m.appendMessage(msg)
}

func (m mainModel) appendSuccess(format string, a ...interface{}) mainModel {
	msg := fmt.Sprintf("  "+styleSuccess.Render("✓")+" "+format, a...)
	return m.appendMessage(msg)
}

func (m mainModel) appendWarn(format string, a ...interface{}) mainModel {
	msg := fmt.Sprintf("  "+styleWarning.Render("!")+" "+format, a...)
	return m.appendMessage(msg)
}

func (m mainModel) appendError(format string, a ...interface{}) mainModel {
	msg := fmt.Sprintf("  "+styleError.Render("✗")+" "+format, a...)
	return m.appendMessage(msg)
}

func (m mainModel) echoInput(line string) mainModel {
	echo := "\n" + stylePromptIcon.Render("❯") + " " + styleUserInput.Render(line)
	return m.appendMessage(echo)
}

// ═══════════════════════════════════════════════════════════════════════════
// PALETTE HELPERS
// ═══════════════════════════════════════════════════════════════════════════

func (m *mainModel) updatePalette() {
	val := m.textInput.Value()

	if m.optState == optStateVideo || m.optState == optStateAudio || m.optState == optStateImage {
		var choices []choice
		switch m.optState {
		case optStateVideo:
			choices = videoFormats
		case optStateAudio:
			choices = audioFormats
		case optStateImage:
			choices = imageFormats
		}
		
		var filtered []cmdSuggestion
		for _, c := range choices {
			if strings.HasPrefix(strings.ToLower(c.Value), strings.ToLower(val)) || strings.HasPrefix(strings.ToLower(c.Label), strings.ToLower(val)) {
				filtered = append(filtered, cmdSuggestion{cmd: c.Value, desc: c.Label})
			}
		}
		m.filteredCmds = filtered
		m.showPalette = true
		if len(m.filteredCmds) > 0 && m.paletteIdx >= len(m.filteredCmds) {
			m.paletteIdx = 0
		} else if len(m.filteredCmds) == 0 {
			m.showPalette = false
		}
		return
	}

	if strings.HasPrefix(val, "/") {
		m.filteredCmds = filterSuggestions(m.allCmds, val)
		m.showPalette = true
		if m.paletteIdx >= len(m.filteredCmds) {
			m.paletteIdx = 0
		}
	} else {
		m.showPalette = false
		m.filteredCmds = m.allCmds
		m.paletteIdx = 0
	}
}

// ═══════════════════════════════════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════════════════════════════════

func (m mainModel) Init() tea.Cmd {
	return tea.Batch(textinput.Blink, tickCmd())
}

// ═══════════════════════════════════════════════════════════════════════════
// EJECUTAR COMANDO
// ═══════════════════════════════════════════════════════════════════════════

func (m mainModel) executeCommand(line string) (tea.Model, tea.Cmd) {
	line = strings.TrimSpace(line)
	if line == "" {
		return m, nil
	}

	// Guardar en historial
	m.inputHistory = append(m.inputHistory, line)
	m.historyIdx = -1

	m = m.echoInput(line)

	fields := strings.Fields(line)
	cmd := fields[0]

	switch cmd {
	case "/optimize":
		m.optState = optStateDir
		m.optVideo = ""
		m.optVExtra = ""
		m.optAudio = ""
		m.optAExtra = ""
		m.optImage = ""
		m.optIExtra = ""
		m.textInput.Placeholder = T("placeholder_dir")
		m.updatePalette()
		return m, nil

	case "/v-preset":
		return m, handleSetValue("Video preset", fields, "/v-preset slow")

	case "/v-crf":
		return m, handleSetValue("Video CRF", fields, "/v-crf 17")

	case "/a-bitrate":
		return m, handleSetValue("Audio bitrate", fields, "/a-bitrate 320k")

	case "/lang":
		if len(fields) > 1 {
			if !applyLanguage(fields[1]) {
				return m, warnCmd(T("unsupported_lang"), fields[1])
			}
			m.allCmds = makeCommands()
			m.filteredCmds = m.allCmds
			m.textInput.Placeholder = T("placeholder_main")
			return m, successMsgCmd("%s: %s", T("lang_changed"), languageLabel(currentLang))
		}
		m.langModel = NewLangModel()
		m.recalcLayout()
		return m, m.langModel.Init()

	case "/clear":
		m.messages = []string{}
		m.viewport.SetContent("")
		return m, nil

	case "/update", "update":
		m = m.appendInfo(T("checking_updates"))
		return m, runUpdateCmd()

	case "/self-update", "self-update":
		m = m.appendInfo(T("pulling_source"))
		return m, runSelfUpdateCmd()

	case "/exit", "exit":
		return m, tea.Quit

	case "/help", "help":
		return m, func() tea.Msg { return logMsg(getHelpText()) }

	case "/formulas", "formulas":
		return m, func() tea.Msg { return logMsg(getFormulasText()) }

	default:
		return m, failCmd("%s '%s'", T("unknown_cmd"), cmd)
	}
}

// ═══════════════════════════════════════════════════════════════════════════
// HANDLE OPT INPUT
// ═══════════════════════════════════════════════════════════════════════════

func (m mainModel) handleOptInput(line string) (tea.Model, tea.Cmd) {
	line = strings.TrimSpace(line)
	if line == "/cancel" {
		m.optState = optStateNone
		m.textInput.Placeholder = T("placeholder_main")
		m.updatePalette()
		return m, warnCmd(T("cancelled"))
	}

	switch m.optState {
	case optStateDir:
		if line == "" {
			return m, nil
		}
		m = m.echoInput(line)
		dir := cleanPath(line)
		
		v, a, i := countMediaFiles(dir)
		if v == 0 && a == 0 && i == 0 {
			m = m.appendError("%s", T("no_media")+" → "+styleUserInput.Render(dir))
			m = m.appendMessage("  " + styleMuted.Render(T("invalid_dir")))
			return m, nil
		}

		sep := styleBorder.Render(strings.Repeat("─", 50))
		m = m.appendMessage("\n" + sep)
		m = m.appendMessage("  " + styleHeaderLogo.Render(T("summary")))
		m = m.appendMessage("")
		m = m.appendMessage(fmt.Sprintf("  %s  %s", styleSummaryKey.Render(fmt.Sprintf("%-10s", T("directory"))), styleUserInput.Render(dir)))
		if v > 0 { m = m.appendMessage(fmt.Sprintf("  %s  %s", styleSummaryKey.Render(fmt.Sprintf("%-10s", T("video"))), styleSuccess.Render(fmt.Sprintf("%d %s", v, T("files"))))) }
		if a > 0 { m = m.appendMessage(fmt.Sprintf("  %s  %s", styleSummaryKey.Render(fmt.Sprintf("%-10s", T("audio"))), styleSuccess.Render(fmt.Sprintf("%d %s", a, T("files"))))) }
		if i > 0 { m = m.appendMessage(fmt.Sprintf("  %s  %s", styleSummaryKey.Render(fmt.Sprintf("%-10s", T("image"))), styleSuccess.Render(fmt.Sprintf("%d %s", i, T("files"))))) }
		m = m.appendMessage(sep + "\n")

		m.optDir = dir
		m.optPendingV = v
		m.optPendingA = a
		m.optPendingI = i
		return m.advanceOptState()

	case optStateVideo:
		m = m.echoInput(line)
		if line == "" { line = "mp4" }
		parts := strings.SplitN(line, " ", 2)
		m.optVideo = parts[0]
		if len(parts) > 1 {
			m.optVExtra = strings.TrimSpace(parts[1])
		}
		return m.advanceOptState()

	case optStateAudio:
		m = m.echoInput(line)
		if line == "" { line = "mp3" }
		parts := strings.SplitN(line, " ", 2)
		m.optAudio = parts[0]
		if len(parts) > 1 {
			m.optAExtra = strings.TrimSpace(parts[1])
		}
		return m.advanceOptState()

	case optStateImage:
		m = m.echoInput(line)
		if line == "" { line = "webp" }
		parts := strings.SplitN(line, " ", 2)
		m.optImage = parts[0]
		if len(parts) > 1 {
			m.optIExtra = strings.TrimSpace(parts[1])
		}
		return m.advanceOptState()
	}

	return m, nil
}

func (m mainModel) advanceOptState() (mainModel, tea.Cmd) {
	if m.optState == optStateDir {
		if m.optPendingV > 0 {
			m.optState = optStateVideo
			m.textInput.Placeholder = T("placeholder_video")
			m.updatePalette()
			return m, nil
		}
		m.optState = optStateVideo
	}
	if m.optState == optStateVideo {
		if m.optPendingA > 0 {
			m.optState = optStateAudio
			m.textInput.Placeholder = T("placeholder_audio")
			m.updatePalette()
			return m, nil
		}
		m.optState = optStateAudio
	}
	if m.optState == optStateAudio {
		if m.optPendingI > 0 {
			m.optState = optStateImage
			m.textInput.Placeholder = T("placeholder_image")
			m.updatePalette()
			return m, nil
		}
		m.optState = optStateImage
	}
	if m.optState == optStateImage {
		m.optState = optStateNone
		m.textInput.Placeholder = T("placeholder_main")
		m.updatePalette()

		if m.optVideo == "" { m.optVideo = "mp4" }
		if m.optAudio == "" { m.optAudio = "mp3" }
		if m.optImage == "" { m.optImage = "webp" }

		m = m.appendInfo(T("starting_format"),
			styleSuccess.Render(m.optVideo),
			styleSuccess.Render(m.optAudio),
			styleSuccess.Render(m.optImage))

		m.processing = true
		setEngineState := func(ec *exec.Cmd, sc *bufio.Scanner) {
			m.engineCmd = ec
			m.scanner = sc
		}
		return m, startEngineCmd(m.optDir, m.optVideo, m.optVExtra, m.optAudio, m.optAExtra, m.optImage, m.optIExtra, setEngineState)
	}
	return m, nil
}


// ═══════════════════════════════════════════════════════════════════════════
// UPDATE
// ═══════════════════════════════════════════════════════════════════════════

func (m mainModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	var cmds []tea.Cmd

	switch msg := msg.(type) {

	// ─── Tamaño de ventana ──────────────────────────────────────────────────
	case tea.WindowSizeMsg:
		m.width = msg.Width
		m.height = msg.Height
		m.textInput.Width = msg.Width - 6
		m.recalcLayout()
		return m, nil

	// ─── Spinner tick ───────────────────────────────────────────────────────
	case tickMsg:
		m.spinnerIdx = (m.spinnerIdx + 1) % len(spinnerFrames)
		if m.currentProgress != "" {
			m.recalcLayout()
		}
		return m, tickCmd()

	// ─── Mensajes del sistema ───────────────────────────────────────────────
	case logMsg:
		m = m.appendMessage(string(msg))
		return m, nil

	case progressMsg:
		m = m.appendMessage(string(msg))
		return m, nil

	case clearMsg:
		m.messages = []string{}
		m.viewport.SetContent("")
		return m, nil

	// ─── Progreso del engine Python ─────────────────────────────────────────
	case engineProgressMsg:
		if msg.done {
			m.processing = false
			if m.engineCmd != nil {
				if err := m.engineCmd.Wait(); err != nil {
					m = m.appendError(T("engine_error"), err)
				}
				m.engineCmd = nil
				m.scanner = nil
				m.currentProgress = ""
			}
			if msg.err != nil {
				m = m.appendWarn(T("stream_error"), msg.err)
			}
			m = m.appendSuccess(T("process_complete"))
			return m, nil
		}

		line := msg.text
		switch {
		case strings.HasPrefix(line, "PROGRESS:"):
			parts := strings.SplitN(line, ":", 2)
			if len(parts) == 2 {
				m.currentProgress = strings.TrimSpace(parts[1])
				m.recalcLayout()
			}
		case strings.HasPrefix(line, "DONE:"):
			parts := strings.SplitN(line, ":", 3)
			if len(parts) >= 2 {
				m = m.appendSuccess("%s %s", T("processed"), parts[1])
			}
			if len(parts) >= 3 {
				m = m.appendMessage("    " + styleMuted.Render(T("output")+":") + " " + styleSecondary.Render(parts[2]))
			}
		case strings.HasPrefix(line, "ERROR:"):
			m = m.appendError("%s", strings.TrimPrefix(line, "ERROR:"))
		default:
			m = m.appendMessage("  " + styleMuted.Render(line))
		}
		return m, readNextEngineLine(m.scanner)
	}

	// ─── Delegar a flujo de idioma ───────────────────────────────────────────
	if m.langModel != nil {
		lang, cmd := m.langModel.Update(msg)
		if lang == nil {
			m.langModel = nil
			m.allCmds = makeCommands()
			m.filteredCmds = m.allCmds
			m.textInput.Placeholder = T("placeholder_main")
			m.recalcLayout()
			return m, cmd
		}
		m.langModel = lang
		return m, cmd
	}

	// ─── Teclado ─────────────────────────────────────────────────────────────
	switch msg := msg.(type) {
	case tea.KeyMsg:
		switch msg.Type {

		case tea.KeyCtrlC:
			return m, tea.Quit

		case tea.KeyEsc:
			if m.showPalette {
				m.showPalette = false
				m.textInput.SetValue("")
				m.textInput.Focus()
				return m, nil
			}
			return m, tea.Quit

		case tea.KeyUp:
			if m.showPalette {
				if m.paletteIdx > 0 {
					m.paletteIdx--
				}
				return m, nil
			}
			// Historial de inputs
			if len(m.inputHistory) > 0 {
				if m.historyIdx < len(m.inputHistory)-1 {
					m.historyIdx++
				}
				idx := len(m.inputHistory) - 1 - m.historyIdx
				m.textInput.SetValue(m.inputHistory[idx])
				m.textInput.CursorEnd()
			}
			return m, nil

		case tea.KeyDown:
			if m.showPalette {
				if m.paletteIdx < len(m.filteredCmds)-1 {
					m.paletteIdx++
				}
				return m, nil
			}
			// Historial hacia adelante
			if m.historyIdx > 0 {
				m.historyIdx--
				idx := len(m.inputHistory) - 1 - m.historyIdx
				m.textInput.SetValue(m.inputHistory[idx])
				m.textInput.CursorEnd()
			} else if m.historyIdx == 0 {
				m.historyIdx = -1
				m.textInput.SetValue("")
			}
			return m, nil

		case tea.KeyTab:
			if m.showPalette && len(m.filteredCmds) > 0 {
				selected := m.filteredCmds[m.paletteIdx].cmd
				m.textInput.SetValue(selected)
				m.textInput.CursorEnd()
				m.updatePalette()
				return m, nil
			}

		case tea.KeyEnter:
			if m.showPalette && len(m.filteredCmds) > 0 {
				selected := m.filteredCmds[m.paletteIdx].cmd
				m.textInput.SetValue("")
				m.showPalette = false
				
				if m.optState != optStateNone {
					return m.handleOptInput(selected)
				}
				return m.executeCommand(selected)
			}
			line := m.textInput.Value()
			m.textInput.SetValue("")
			m.showPalette = false
			
			if m.optState != optStateNone {
				return m.handleOptInput(line)
			}
			return m.executeCommand(line)

		default:
			var cmd tea.Cmd
			m.textInput, cmd = m.textInput.Update(msg)
			cmds = append(cmds, cmd)
			m.updatePalette()
			return m, tea.Batch(cmds...)
		}
	}

	// Scroll del viewport con el ratón
	var cmd tea.Cmd
	m.viewport, cmd = m.viewport.Update(msg)
	cmds = append(cmds, cmd)

	return m, tea.Batch(cmds...)
}

// ═══════════════════════════════════════════════════════════════════════════
// RECALC LAYOUT  (exactamente como Gemini: header+viewport+palette?+input+footer)
// ═══════════════════════════════════════════════════════════════════════════

func (m *mainModel) recalcLayout() {
	if m.width == 0 {
		return
	}

	// Alturas fijas
	headerH := 5 // logo + separador ≈ 5 líneas
	footerH := 2 // separador + status bar
	inputBoxH := 3 // borde redondeado + 1 línea de texto
	paletteH := 0
	if m.showPalette {
		visible := len(m.filteredCmds)
		if visible > maxSuggestionsVisible {
			visible = maxSuggestionsVisible
		}
		paletteH = visible + 2 // +2 por bordes del box
	}

	vpH := m.height - headerH - footerH - inputBoxH - paletteH - 1
	if vpH < 2 {
		vpH = 2
	}

	m.viewport.Width = m.width
	m.viewport.Height = vpH
	
	content := strings.Join(m.messages, "\n")
	if m.currentProgress != "" {
		spinner := styleInfo.Render(spinnerFrames[m.spinnerIdx])
		progressLine := "  " + styleProgressLabel.Render(T("processing")) + " " + styleMuted.Render(m.currentProgress) + " " + spinner
		content += "\n\n" + progressLine
	}
	m.viewport.SetContent(content)
	m.viewport.GotoBottom()
}

// ═══════════════════════════════════════════════════════════════════════════
// VIEW  (layout: header | viewport | palette? | input | footer)
// ═══════════════════════════════════════════════════════════════════════════

func (m mainModel) View() string {
	// ─── Flujos modales (huh) toman pantalla completa ────────────────────────
	if m.langModel != nil {
		return m.langModel.View()
	}

	var sb strings.Builder

	// ── Zona 1: Header ───────────────────────────────────────────────────────
	sb.WriteString(renderHeader(m.width))

	// ── Zona 2: Historial scrollable ─────────────────────────────────────────
	sb.WriteString(m.viewport.View())
	sb.WriteString("\n")

	// ── Zona 3a: Command palette (flotante sobre el input, igual que Gemini) ─
	if m.showPalette && len(m.filteredCmds) > 0 {
		palette := renderSuggestions(m.filteredCmds, m.paletteIdx, m.width)
		sb.WriteString(palette)
		sb.WriteString("\n")
	}

	// ── Zona 3b: Input box con borde redondeado ───────────────────────────────
	inputContent := m.textInput.View()
	var inputBox string
	if m.focus == InputFocus {
		inputBox = styleInputBoxFocused.Width(m.width - 2).Render(inputContent)
	} else {
		inputBox = styleInputBox.Width(m.width - 2).Render(inputContent)
	}
	sb.WriteString(inputBox)
	sb.WriteString("\n")

	// ── Zona 4: Footer / status bar ──────────────────────────────────────────
	// Remove spinner from footer if it's processing to avoid duplicate, or just keep it simple.
	// Since the user wanted it inline, we'll keep the footer clean.
	var spinner string
	if !m.processing {
		spinner = ""
	} else {
		// Just a static space or something if needed, or we can leave it empty
		spinner = " "
	}
	sb.WriteString(renderFooter(m.width, m.processing, spinner))

	return sb.String()
}

// ═══════════════════════════════════════════════════════════════════════════
// MAIN
// ═══════════════════════════════════════════════════════════════════════════

func main() {
	if len(os.Args) > 1 {
		switch os.Args[1] {
		case "version":
			fmt.Printf("alenia porter %s\n", version)
			os.Exit(0)
		case "optimize":
			if len(os.Args) > 2 {
				runDirectOptimize()
				os.Exit(0)
			}
		}
	}

	p := tea.NewProgram(
		initialModel(),
		tea.WithAltScreen(),
		tea.WithMouseCellMotion(),
	)
	if _, err := p.Run(); err != nil {
		fmt.Fprintf(os.Stderr, "Error iniciando Alenia Porter: %v\n", err)
		os.Exit(1)
	}
}
