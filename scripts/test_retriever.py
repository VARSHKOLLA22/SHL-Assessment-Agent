from services.retriever import SHLRetriever

retriever = SHLRetriever()

print("\nSearching...\n")

results = retriever.search(
    "Java Developer assessment",
    top_k=5
)

for i, assessment in enumerate(results, start=1):

    print(f"{i}. {assessment['name']}")

    print(assessment["link"])

    print("-" * 50)