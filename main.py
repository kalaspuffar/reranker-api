#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
import json
import os
from rerankers import Reranker, Document

class Handler(BaseHTTPRequestHandler):
    def _send_json(self, code: int, obj: dict):
        body = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length) if length > 0 else b"{}"
            payload = json.loads(raw.decode("utf-8"))

            config = payload.get("config", {})
            data = payload.get("data", {})

            rk = Reranker(
                config.get("model_name", "flashrank"),
                model_type=config.get("model_type"),
                lang=config.get("lang"),
                api_provider=config.get("api_provider"),
                api_key=config.get("api_key"),
            )

            query = data["query"]
            docs_in = data["docs"]
            top_k = data.get("top_k")

            # Normalize docs: accept strings or dicts with {text, doc_id?, metadata?}
            docs = []
            for i, d in enumerate(docs_in):
                if isinstance(d, str):
                    docs.append(Document(text=d, doc_id=i))
                else:
                    docs.append(Document(
                        text=d.get("text", ""),
                        doc_id=d.get("doc_id", i),
                        metadata=d.get("metadata", {}) or {}
                    ))

            results = rk.rank(query=query, docs=docs)
            items = results.top_k(top_k) if top_k else results

            
            resp = [
                [getattr(r.document, "text", None), r.score]
                for r in items
            ]
            return self._send_json(200, resp)            
        except Exception as e:
            return self._send_json(400, {"error": str(e)})



def main():
    HOST = "0.0.0.0"
    PORT = int(os.getenv("PORT", "32300"))

    server = HTTPServer((HOST, PORT), Handler)
    print(f"Serving on http://{HOST}:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()
