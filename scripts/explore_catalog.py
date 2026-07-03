import json

with open("data/catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)

print("=" * 50)
print("Total Assessments:", len(catalog))
print("=" * 50)

print("\nFields Available:\n")

for key in catalog[0].keys():
    print("-", key)