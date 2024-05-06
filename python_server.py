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
        probability = result[torch.argmax(result)]
        sentiment = labels[torch.argmax(result)]
        return probability, sentiment
    else:
        return 0, labels[-1]


# if __name__ == "__main__":
#     tensor, sentiment = estimate_sentiment(['markets responded negatively to the news!','traders were displeased!'])
#     print(tensor, sentiment)
#     print(torch.cuda.is_available())

async def handle_connection(websocket, path):
    async for message in websocket:
        data = json.loads(message)
        if data['action'] == 'invoke_function':
            headline = data['headline']
            result = estimate_sentiment(headline)
            await websocket.send(json.dumps(result))

async def main():
    async with websockets.serve(handle_connection, "localhost", 8765):
        await asyncio.Future()  # Run forever

asyncio.run(main())
