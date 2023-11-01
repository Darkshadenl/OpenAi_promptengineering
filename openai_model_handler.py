import asyncio
from datetime import datetime

import tiktoken
from openai import AsyncOpenAI
from gpt_input import ChatGptInput


class OpenAiModelHandler:
    def __init__(self, gpt_input: ChatGptInput):
        self.client = AsyncOpenAI()
        self.input = gpt_input
        self.completion = None
        self.start_time = None
        self.end_time = None
        self.total_time = None
        self.output_tokens = None

    async def create_prediction(self):
        self.start_time = datetime.now()
        self.completion = await self.client.chat.completions.create(
            **self.input.to_dict()
        )
        self.end_time = datetime.now()
        self.total_time = self.end_time - self.start_time

    async def create_prediction_with_status(self, interval=5):
        print_task = asyncio.create_task(self.print_status_every(interval))
        await self.create_prediction()
        print_task.cancel()
        print(f"{self.input.model} finished in {self.total_time}")

    async def print_status_every(self, seconds):
        while True:
            print(f"{self.input.model} is still running...")
            await asyncio.sleep(seconds)