from memory.memory_search import MemorySearch

query = input("Search Topic: ")

results = MemorySearch.search(query)

print("\n========== MEMORY SEARCH ==========\n")

if not results:
    print("No similar memory found.")

else:
    for item in results:

        print(f"Topic : {item['topic']}")
        print(f"Score : {item['score']}")
        print("-" * 40)