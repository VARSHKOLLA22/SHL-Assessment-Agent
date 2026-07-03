import json

with open("data/catalog.json", "r", encoding="utf-8") as file:
    catalog = json.load(file)

print("Total Assessments:", len(catalog))

print("\nFirst Assessment:\n")

print(catalog[0])