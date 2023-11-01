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
        self.input_tokens = None
        self.output_tokens = None

    async def create_prediction(self):
        print("start ai call")
        self.start_time = datetime.now()
        self.completion = await self.client.chat.completions.create(
            **self.input.to_dict()
        )
        self.end_time = datetime.now()
        self.total_time = self.end_time - self.start_time
        print("end ai call")
