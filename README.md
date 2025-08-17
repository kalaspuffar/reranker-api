# Reranker-API

This repository wraps [rerankers](https://github.com/AnswerDotAI/rerankers) with an API and docker environment so you can spin it up and have a port you can query for reranking.

Bringing up the service:
```
docker compose up
```


Testing the API:
```
curl -s http://localhost:32300 -H 'Content-Type: application/json' -d '{
    "config": {
      "model_name":"mixedbread-ai/mxbai-rerank-large-v1",
      "model_type":"cross-encoder"
    },
    "data": { "query":"I love you", "docs":["I hate you","I really like you"] }
}'
```

Expected response:
```
[["I really like you", -1.5379297733306885], ["I hate you", -4.309110164642334]]
```
