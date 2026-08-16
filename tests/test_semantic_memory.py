from memory.semantic_memory import SemanticMemory

topic = input("Enter Topic: ")

results = SemanticMemory.search(topic)

print("\n========== SEMANTIC SEARCH ==========\n")

if not results:
    print("No semantic matches found.")

else:

    for item in results:

        print(f"Topic : {item['topic']}")
        print(f"Score : {item['score']}")
        print()