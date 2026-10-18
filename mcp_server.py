#!/usr/bin/env python3
import json
import sys
from client import AgenticRAGHyDEQueryExpander

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        expander = AgenticRAGHyDEQueryExpander()
        res = expander.generate_hypothetical_passages("kafka consumer lag high watermark drift", domain="devops", perspectives_count=3)
        assert res["hypothetical_passages_generated"] == 3
        assert "HYDE-1" in res["passages"][0]["perspective_id"]
        assert "kafka" in res["composite_dense_query_embedding_text"].lower()
        print(f"[TEST PASS] HyDE Expander Passages: {res['hypothetical_passages_generated']}")
        sys.exit(0)

    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            method = req.get("method")
            msg_id = req.get("id")
            if method == "initialize":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"serverInfo": {"name": "genpark-rag-hyde-expander", "version": "1.0.0"}}}))
            elif method == "tools/list":
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": [{"name": "generate_hypothetical_passages", "description": "Synthesize hypothetical answer passages for RAG retrieval"}]}}))
            elif method == "tools/call":
                args = req.get("params", {}).get("arguments", {})
                expander = AgenticRAGHyDEQueryExpander()
                out = expander.generate_hypothetical_passages(args.get("query", ""), args.get("domain", "general"), args.get("perspectives_count", 3))
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"content": [{"type": "text", "text": json.dumps(out)}]}}))
            else:
                print(json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}}))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}))
            sys.stdout.flush()

if __name__ == "__main__":
    main()
