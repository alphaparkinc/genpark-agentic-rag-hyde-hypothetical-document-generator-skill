from client import AgenticRAGHyDEQueryExpander

def main():
    expander = AgenticRAGHyDEQueryExpander()
    query = "how to prevent postgresql deadlocks on concurrent bulk updates"
    res = expander.generate_hypothetical_passages(query, domain="database", perspectives_count=3)
    print("--- HyDE Hypothetical Expansion ---")
    print(f"Original Query: {res['original_query']}")
    for p in res['passages']:
        print(f"[{p['perspective_id']}] (Weight: {p['dense_retrieval_weight']}): {p['hypothetical_passage'][:100]}...")

if __name__ == "__main__":
    main()
