from services.catalog_loader import load_catalog

catalog = load_catalog()

print("Total Assessments:", len(catalog))

print()

print("First Assessment Name:")

print(catalog[0]["name"])