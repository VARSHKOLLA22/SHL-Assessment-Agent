import requests
import os

CATALOG_URL = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

response = requests.get(CATALOG_URL)

os.makedirs("data", exist_ok=True)

with open("data/catalog.json", "w", encoding="utf-8") as f:
    f.write(response.text)

print("✅ Catalog downloaded successfully!")