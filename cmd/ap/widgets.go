package main

import (
	"fmt"
	"strings"
	"time"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/lipgloss"
)

// ═══════════════════════════════════════════════════════════════════════════
// LOGO ASCII  — texto compacto al estilo Gemini CLI
// ═══════════════════════════════════════════════════════════════════════════

// Logo braille compacto (líneas 5-36 del kaia_mini_braille.txt, recortado)
const logoMascot = `⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣤⣶⣶⣶⣶⣶⣶⣶⣶⣦⣄⡀
⠀⠀⠀⠀⠀⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣀
⠀⠀⠀⠀⣠⣾⣿⣿⣿⠛⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠙⠻⣿⣿⣿⣿
⠀⠀⠀⣴⣿⣿⡿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⡿
⠀⠀⣸⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠻⠟⠋
⣶⣾⣿⣿⣿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿
⣿⣿⣿⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⠇
⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⡟
⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⢿⣿⣿⣿⣇`

// Logo texto "Alenia Porter" en estilo bloque compacto
const logoText = ` █████╗ ██╗     ███████╗███╗  ██╗██╗ █████╗
██╔══██╗██║     ██╔════╝████╗ ██║██║██╔══██╗
███████║██║     █████╗  ██╔██╗██║██║███████║
██╔══██║██║     ██╔══╝  ██║╚████║██║██╔══██║
██║  ██║███████╗███████╗██║ ╚███║██║██║  ██║
╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚══╝╚═╝╚═╝  ╚═╝`

const logoCompact = `▄▀█ █░░ █▀▀ █▄░█ █ ▄▀█   █▀█ █▀█ █▀█ ▀█▀ █▀▀ █▀█
█▀█ █▄▄ ██▄ █░▀█ █ █▀█   █▀▀ █▄█ █▀▄ ░█░ ██▄ █▀▄`

// renderLogoGradient dibuja el logo ASCII con gradiente azul→cian
func renderLogoGradient(art string) string {
	lines := strings.Split(art, "\n")
	maxLen := 0
	for _, l := range lines {
		w := lipgloss.Width(l)
		if w > maxLen {
			maxLen = w
		}
	}
	var sb strings.Builder
	for _, line := range lines {
		runes := []rune(line)
		for ci, ch := range runes {
			t := 0.0
			if maxLen > 0 {
				t = float64(ci) / float64(maxLen)
			}
			c := gradientColor(t)
			sb.WriteString(lipgloss.NewStyle().Foreground(c).Render(string(ch)))
		}
		sb.WriteString("\n")
	}
	return strings.TrimRight(sb.String(), "\n")
}

// ═══════════════════════════════════════════════════════════════════════════
// HEADER — layout idéntico a Gemini CLI
// ═══════════════════════════════════════════════════════════════════════════

func renderHeader(width int) string {
	var logoStr string
	if width >= 90 {
		// Pantalla amplia: logo bloque completo
		logoStr = renderLogoGradient(logoText)
	} else if width >= 60 {
		// Pantalla mediana: logo compacto 2 líneas
		logoStr = renderLogoGradient(logoCompact)
	} else {
		// Pantalla pequeña: solo mascota 2 líneas
		logoStr = renderLogoGradient(logoCompact)
	}

	// Línea de metadata bajo el logo
	ver := styleHeaderVersion.Render("v" + version)
	lang := styleMuted.Render("  " + languageLabel(currentLang))
	hint := styleMuted.Render("  ·  " + T("header_hint"))
	metaLine := "  " + ver + lang + hint

	sep := styleBorder.Render(strings.Repeat("─", width))
	return "\n" + logoStr + "\n" + metaLine + "\n" + sep + "\n"
}

// ═══════════════════════════════════════════════════════════════════════════
// FOOTER / STATUS BAR
// ═══════════════════════════════════════════════════════════════════════════

func renderFooter(width int, isProcessing bool, spinnerFrame string) string {
	// Lado izquierdo: shortcuts
	left := styleFooterKey.Render("ESC") +
		styleSecondary.Render(T("footer_exit")) +
		styleFooterKey.Render("/") +
		styleSecondary.Render(T("footer_cmds")) +
		styleFooterKey.Render("↑↓") +
		styleSecondary.Render(T("footer_hist"))

	// Lado derecho: idioma y estado
	right := ""
	if isProcessing {
		right = styleInfo.Render(spinnerFrame+T("footer_proc")) + styleFooterLang.Render("["+currentLang+"]")
	} else {
		right = styleFooterLang.Render("[" + currentLang + "]")
	}

	// Calcular padding para separar left y right
	leftW := lipgloss.Width(left)
	rightW := lipgloss.Width(right)
	space := width - leftW - rightW - 2 // 2 de padding lateral
	if space < 1 {
		space = 1
	}
	pad := strings.Repeat(" ", space)

	line := " " + left + pad + right + " "
	sep := styleBorder.Render(strings.Repeat("─", width))
	return sep + "\n" + styleMuted.Render(line)
}

// ═══════════════════════════════════════════════════════════════════════════
// COMMAND PALETTE (sugerencias flotantes estilo Gemini SuggestionsDisplay)
// ═══════════════════════════════════════════════════════════════════════════

type cmdSuggestion struct {
	cmd  string
	desc string
}

func makeCommands() []cmdSuggestion {
	return []cmdSuggestion{
		{"/optimize", T("cmd_optimize")},
		{"/v-crf", T("cmd_vcrf")},
		{"/v-preset", T("cmd_vpreset")},
		{"/a-bitrate", T("cmd_abitrate")},
		{"/lang", T("cmd_lang")},
		{"/clear", T("cmd_clear")},
		{"/update", T("cmd_update")},
		{"/self-update", T("cmd_self_update")},
		{"/help", T("cmd_help_desc")},
		{"/formulas", T("cmd_formulas")},
		{"/exit", T("cmd_exit")},
	}
}

func filterSuggestions(cmds []cmdSuggestion, prefix string) []cmdSuggestion {
	if prefix == "" || prefix == "/" {
		return cmds
	}
	var out []cmdSuggestion
	for _, c := range cmds {
		if strings.HasPrefix(c.cmd, prefix) {
			out = append(out, c)
		}
	}
	return out
}

const maxSuggestionsVisible = 8

func renderSuggestions(sugs []cmdSuggestion, activeIdx int, width int) string {
	if len(sugs) == 0 {
		return ""
	}

	start := 0
	end := len(sugs)

	if end > maxSuggestionsVisible {
		if activeIdx >= maxSuggestionsVisible {
			start = activeIdx - maxSuggestionsVisible + 1
			end = activeIdx + 1
		} else {
			end = maxSuggestionsVisible
		}
	}
	visible := sugs[start:end]

	// Calcular ancho máximo de comando
	maxCmd := 0
	for _, s := range sugs {
		if len(s.cmd) > maxCmd {
			maxCmd = len(s.cmd)
		}
	}

	var rows []string
	if start > 0 {
		rows = append(rows, styleMuted.Render(fmt.Sprintf(T("palette_prev"), start)))
	}

	for i, s := range visible {
		isActive := (start + i) == activeIdx

		var cmdPart string
		if isActive {
			slash := stylePaletteSlash.Render("/")
			rest := stylePaletteItemSelected.Render(strings.TrimPrefix(s.cmd, "/"))
			cmdPart = slash + rest
		} else {
			cmdPart = stylePaletteItem.Render(s.cmd)
		}

		// Padding para alinear descripción
		padLen := maxCmd - len(s.cmd) + 3
		pad := strings.Repeat(" ", padLen)

		var descPart string
		if isActive {
			descPart = stylePaletteDescSelected.Render(s.desc)
		} else {
			descPart = stylePaletteDesc.Render(s.desc)
		}

		row := cmdPart + pad + descPart
		if isActive {
			row = lipgloss.NewStyle().
				Background(colorFocusBg).
				Width(width - 4).
				Render(row)
		}
		rows = append(rows, row)
	}

	// Indicador de más elementos
	if len(sugs) > end {
		rows = append(rows, styleMuted.Render(fmt.Sprintf(T("palette_more"), len(sugs)-end)))
	}

	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder(), true).
		BorderForeground(colorBorder).
		Width(width - 2).
		Render(strings.Join(rows, "\n"))
}

// ═══════════════════════════════════════════════════════════════════════════
// SPINNER (estilo Gemini CliSpinner)
// ═══════════════════════════════════════════════════════════════════════════

var spinnerFrames = []string{"⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"}

type tickMsg time.Time

func tickCmd() tea.Cmd {
	return tea.Tick(100*time.Millisecond, func(t time.Time) tea.Msg {
		return tickMsg(t)
	})
}

// ═══════════════════════════════════════════════════════════════════════════
// HELPER
// ═══════════════════════════════════════════════════════════════════════════

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}
