from brain.memory.retrieval_engine import RetrievalEngine


retriever = RetrievalEngine()


product = {

    "id": "Partition001",

    "category": "partition",

    "material": {
        "primary": "rattan"
    },

    "style": [
        "bohemian",
        "natural",
        "luxury"
    ],

    "colors": {
        "primary": [
            "beige",
            "brown"
        ]
    }
}


results = retriever.retrieve(
    product
)


print("==============================")
print("RETRIEVAL TEST")
print("==============================")


for item in results:

    print(
        "Memory:",
        item.get("memory")
    )

    print(
        "Similarity:",
        item.get("similarity")
    )

    print(
        "Reasons:",
        item.get("reasons")
    )

    print("------------------------------")