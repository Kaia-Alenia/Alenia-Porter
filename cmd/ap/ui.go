package main

import (
	"fmt"
	"strings"

	tea "github.com/charmbracelet/bubbletea"
	"github.com/charmbracelet/huh"
)

// ═══════════════════════════════════════════════════════════════════════════
// TIPOS DE MENSAJE BUBBLETEA
// ═══════════════════════════════════════════════════════════════════════════

type logMsg string
type clearMsg struct{}
type progressMsg string

// ═══════════════════════════════════════════════════════════════════════════
// COMANDOS TEA QUE PRODUCEN MENSAJES
// ═══════════════════════════════════════════════════════════════════════════

func msgCmd(text string) tea.Cmd {
	return func() tea.Msg { return logMsg(text) }
}

func infoCmd(format string, a ...interface{}) tea.Cmd {
	msg := fmt.Sprintf("  "+styleInfo.Render("ℹ")+" "+format, a...)
	return msgCmd(msg)
}

func successMsgCmd(format string, a ...interface{}) tea.Cmd {
	msg := fmt.Sprintf("  "+styleSuccess.Render("✓")+" "+format, a...)
	return msgCmd(msg)
}

func warnCmd(format string, a ...interface{}) tea.Cmd {
	msg := fmt.Sprintf("  "+styleWarning.Render("!")+" "+format, a...)
	return msgCmd(msg)
}

func failCmd(format string, a ...interface{}) tea.Cmd {
	msg := fmt.Sprintf("  "+styleError.Render("✗")+" "+format, a...)
	return msgCmd(msg)
}

// ═══════════════════════════════════════════════════════════════════════════
// FUNCIONES DE PRINT DIRECTAS (para modo non-interactive / direct optimize)
// ═══════════════════════════════════════════════════════════════════════════

func info(format string, a ...interface{}) {
	fmt.Printf("  "+styleInfo.Render("ℹ")+" "+format+"\n", a...)
}

func successMsg(format string, a ...interface{}) {
	fmt.Printf("  "+styleSuccess.Render("✓")+" "+format+"\n", a...)
}

func warn(format string, a ...interface{}) {
	fmt.Printf("  "+styleWarning.Render("!")+" "+format+"\n", a...)
}

func fail(format string, a ...interface{}) {
	fmt.Printf("  "+styleError.Render("✗")+" "+format+"\n", a...)
}

func divider() string {
	return strings.Repeat("─", 56)
}

// ═══════════════════════════════════════════════════════════════════════════
// FLUJO DE IDIOMA (huh select)
// ═══════════════════════════════════════════════════════════════════════════

type LangModel struct {
	form *huh.Form
}

func NewLangModel() *LangModel {
	opts := make([]huh.Option[string], len(languageChoices))
	for i, lc := range languageChoices {
		opts[i] = huh.NewOption(lc.Label, lc.Value)
	}

	form := huh.NewForm(
		huh.NewGroup(
			huh.NewSelect[string]().
				Key("lang").
				Title(T("lang_prompt")).
				Options(opts...).
				Value(ptr(currentLang)),
		),
	)
	form.Init()
	return &LangModel{form: form}
}

func (m *LangModel) Init() tea.Cmd {
	return m.form.Init()
}

func (m *LangModel) Update(msg tea.Msg) (tea.Model, tea.Cmd) {
	form, cmd := m.form.Update(msg)
	if f, ok := form.(*huh.Form); ok {
		m.form = f
		if m.form.State == huh.StateCompleted {
			lang := m.form.GetString("lang")
			if !applyLanguage(lang) {
				return nil, warnCmd(T("unsupported_lang"), lang)
			}
			return nil, successMsgCmd("%s: %s", T("lang_changed"), languageLabel(currentLang))
		}
		if m.form.State == huh.StateAborted {
			return nil, warnCmd(T("cancelled"))
		}
	}
	return m, cmd
}

func (m *LangModel) View() string {
	return m.form.View()
}

// ═══════════════════════════════════════════════════════════════════════════
// AYUDA
// ═══════════════════════════════════════════════════════════════════════════

func getHelpText() string {
	cmds := makeCommands()
	var sb strings.Builder
	sep := styleBorder.Render(strings.Repeat("─", 56))

	sb.WriteString("\n" + sep + "\n")
	sb.WriteString("  " + styleHeaderLogo.Render(T("available_cmds")) + "\n\n")

	for _, c := range cmds {
		cmdPart := stylePaletteSlash.Render("/") + stylePaletteItemSelected.Render(strings.TrimPrefix(c.cmd, "/"))
		padLen := 18 - len(c.cmd)
		if padLen < 1 {
			padLen = 1
		}
		pad := strings.Repeat(" ", padLen)
		descPart := stylePaletteDesc.Render(c.desc)
		sb.WriteString(fmt.Sprintf("  %s%s%s\n", cmdPart, pad, descPart))
	}

	sb.WriteString(sep + "\n")
	return sb.String()
}

// ═══════════════════════════════════════════════════════════════════════════
// FORMULAS
// ═══════════════════════════════════════════════════════════════════════════

func getFormulasText() string {
	formulas := []struct {
		title string
		cmd   string
	}{
		{T("formula_bw"), "-vf hue=s=0"},
		{T("formula_rotate"), "-vf transpose=1"},
		{T("formula_volume"), "-af volume=2.0"},
		{T("formula_crop"), "-vf crop=in_w:in_w"},
		{T("formula_mute"), "-an"},
	}

	var sb strings.Builder
	sep := styleBorder.Render(strings.Repeat("─", 56))

	sb.WriteString("\n" + sep + "\n")
	sb.WriteString("  " + styleHeaderLogo.Render(T("formulas_title")) + "\n\n")

	for _, f := range formulas {
		titlePart := stylePaletteDesc.Render(fmt.Sprintf("%-20s", f.title))
		cmdPart := styleUserInput.Render(f.cmd)
		sb.WriteString(fmt.Sprintf("  %s %s\n", titlePart, cmdPart))
	}

	sb.WriteString("\n  " + styleMuted.Render(T("formulas_hint")))
	sb.WriteString("\n" + sep + "\n")
	return sb.String()
}

// ═══════════════════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════════════════

func ptr[T any](v T) *T {
	return &v
}

func huhChoices(opts []choice) []huh.Option[string] {
	var choices []huh.Option[string]
	for _, o := range opts {
		choices = append(choices, huh.NewOption(o.Label, o.Value))
	}
	return choices
}

func handleSetValue(label string, parts []string, example string) tea.Cmd {
	if len(parts) > 1 {
		value := strings.TrimSpace(strings.Join(parts[1:], " "))
		return successMsgCmd("%s → %s", label, styleUserInput.Render(value))
	}
	return warnCmd(T("value_required"), styleInfo.Render(example))
}
