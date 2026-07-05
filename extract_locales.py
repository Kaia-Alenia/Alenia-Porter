import re

with open("frontend/src/App.tsx", "r") as f:
    content = f.read()

# Pattern to find t("key", "default") or t('key', 'default')
pattern = r't\(\s*["\']([^"\']+)["\']\s*,\s*["\']([^"\']+)["\']\s*\)'

matches = re.findall(pattern, content)
# Also find t("key") with no default
pattern2 = r't\(\s*["\']([^"\']+)["\']\s*\)'
matches2 = re.findall(pattern2, content)

all_keys = set([m[0] for m in matches] + matches2)
# Create a dictionary of the ones with defaults
extracted = {m[0]: m[1] for m in matches}

# Load the current locales.json
import json
with open("src/alenia_porter/assets/locales/locales.json", "r") as f:
    locales = json.load(f)

# Find what's missing in "en" and "es"
en = locales.get("en", {})
es = locales.get("es", {})

missing = {}
for k in all_keys:
    if k not in en or k not in es:
        missing[k] = extracted.get(k, k) # use default if available, else key

print(json.dumps(missing, indent=2))
