package main

import "github.com/charmbracelet/lipgloss"

const (
	colorAccentBlue   = lipgloss.Color("#4285F4")
	colorAccentCyan   = lipgloss.Color("#00BCD4")
	colorAccentGreen  = lipgloss.Color("#34A853")
	colorAccentPurple = lipgloss.Color("#AB47BC")
	colorAccentRed    = lipgloss.Color("#EA4335")
	colorAccentYellow = lipgloss.Color("#FBBC04")

	colorForeground = lipgloss.Color("#E8EAED")
	colorSecondary  = lipgloss.Color("#9AA0A6")
	colorMuted      = lipgloss.Color("#5F6368")
	colorBorder     = lipgloss.Color("#3C4043")
	colorFocusBg    = lipgloss.Color("#1A1E2E")
	colorInputBg    = lipgloss.Color("#202124")
	colorSurface    = lipgloss.Color("#1E1E1E")
)

var (
	stylePromptIcon = lipgloss.NewStyle().
			Foreground(colorAccentBlue).
			Bold(true)

	styleUserInput = lipgloss.NewStyle().
			Foreground(colorForeground)

	styleSecondary = lipgloss.NewStyle().
			Foreground(colorSecondary)

	styleMuted = lipgloss.NewStyle().
			Foreground(colorMuted)

	styleSuccess = lipgloss.NewStyle().
			Foreground(colorAccentGreen).
			Bold(true)

	styleWarning = lipgloss.NewStyle().
			Foreground(colorAccentYellow).
			Bold(true)

	styleError = lipgloss.NewStyle().
			Foreground(colorAccentRed).
			Bold(true)

	styleInfo = lipgloss.NewStyle().
			Foreground(colorAccentCyan)

	styleBorder = lipgloss.NewStyle().
			Foreground(colorBorder)

	styleHeaderLogo = lipgloss.NewStyle().
			Bold(true).
			Foreground(colorAccentBlue)

	styleHeaderVersion = lipgloss.NewStyle().
				Foreground(colorSecondary)

	styleHeaderHint = lipgloss.NewStyle().
			Foreground(colorMuted)

	styleFooter = lipgloss.NewStyle().
			Foreground(colorMuted).
			BorderTop(true).
			BorderStyle(lipgloss.NormalBorder()).
			BorderForeground(colorBorder)

	styleFooterKey = lipgloss.NewStyle().
			Foreground(colorAccentCyan).
			Bold(true)

	styleFooterSep = lipgloss.NewStyle().
			Foreground(colorBorder)

	styleFooterLang = lipgloss.NewStyle().
			Foreground(colorAccentBlue)

	styleInputBox = lipgloss.NewStyle().
			BorderStyle(lipgloss.RoundedBorder()).
			BorderForeground(colorBorder).
			Padding(0, 1)

	styleInputBoxFocused = lipgloss.NewStyle().
				BorderStyle(lipgloss.RoundedBorder()).
				BorderForeground(colorAccentBlue).
				Padding(0, 1)

	stylePaletteBox = lipgloss.NewStyle().
			BorderStyle(lipgloss.RoundedBorder()).
			BorderForeground(colorBorder).
			Padding(0, 1)

	stylePaletteItem = lipgloss.NewStyle().
				Foreground(colorSecondary)

	stylePaletteItemSelected = lipgloss.NewStyle().
					Foreground(colorAccentBlue).
					Bold(true)

	stylePaletteDesc = lipgloss.NewStyle().
				Foreground(colorMuted)

	stylePaletteDescSelected = lipgloss.NewStyle().
					Foreground(colorAccentCyan)

	stylePaletteSlash = lipgloss.NewStyle().
				Foreground(colorAccentBlue).
				Bold(true)

	styleProgressLabel = lipgloss.NewStyle().
				Foreground(colorMuted)

	styleSummaryKey = lipgloss.NewStyle().
			Foreground(colorSecondary)

	Reset   = "\033[0m"
	Bold    = "\033[1m"
	Accent  = "\033[38;5;111m"
	Success = "\033[38;5;114m"
	Warning = "\033[38;5;221m"
	Error   = "\033[38;5;167m"
	Muted   = "\033[38;5;244m"
)

func gradientColor(t float64) lipgloss.Color {
	if t < 0.5 {
		return colorAccentBlue
	}
	return colorAccentCyan
}
