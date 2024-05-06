import asyncio
import websockets
import asyncio
import websockets
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Tuple 
import torch
import json

device = "cuda:0" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert").to(device)
labels = ["positive", "negative", "neutral"]

def estimate_sentiment(news):
    if news:
        tokens = tokenizer(news, return_tensors="pt", padding=True).to(device)

        result = model(tokens["input_ids"], attention_mask=tokens["attention_mask"])[
            "logits"
        ]
        result = torch.nn.functional.softmax(torch.sum(result, 0), dim=-1)
        probability = result[torch.argmax(result)].item()
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1]


async def start(websocket, path):
    print("connected")
    while True:
       data = await websocket.recv()
       print(f"< {data}")
       result = estimate_sentiment(data)
       print(f"< {result}")
       await websocket.send(json.dumps(result))
       print("Sent data")

async def main():
    server = await websockets.serve(start, 'localhost', 8080)
    await server.wait_closed()
asyncio.run(main())