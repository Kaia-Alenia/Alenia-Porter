import re
import json

app_file = "frontend/src/App.tsx"
with open(app_file, "r", encoding="utf-8") as f:
    content = f.read()

# Replace optgroup labels
def optgroup_repl(m):
    label = m.group(1)
    key = "optgroup_" + re.sub(r'[^a-zA-Z0-9]', '', label).lower()
    return f'<optgroup label={{t("{key}", "{label}")}}>'

content = re.sub(r'<optgroup label="([^"]+)">', optgroup_repl, content)

# Replace option texts
def option_repl(m):
    val = m.group(1)
    text = m.group(2)
    key = "opt_" + val.lower()
    return f'<option value="{val}">{{t("{key}", "{text}")}}</option>'

content = re.sub(r'<option value="([^"]+)">([^<]+)</option>', option_repl, content)

# Fix "Actualizar Ahora" missing key
# Just wrap if not wrapped? Actually we just need to add to locales.json for updateNow

with open(app_file, "w", encoding="utf-8") as f:
    f.write(content)

print("App.tsx modified successfully")
