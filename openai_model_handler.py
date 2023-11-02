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
        self.start_end_times = [
            ("start_time", "end_time")
        ]
        self.total_time = None
        self.output_tokens = 0

    async def create_prediction(self):
        start_time = datetime.now()
        x = self.input.to_dict()
        self.completion = await self.client.chat.completions.create(
            **self.input.to_dict()
        )
        end_time = datetime.now()
        self.start_end_times.append((str(start_time), str(end_time)))

    def num_tokens_from_string(self, string: str) -> int:
        encoding = tiktoken.encoding_for_model(self.input.model)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def update_output_tokens(self):
        self.output_tokens += self.num_tokens_from_string(self.get_completion_message())

    def update_input_with_gpt_response(self):
        self.input.add_to_messages("assistant", self.get_completion_message())

    def get_completion_message(self) -> str:
        return self.completion.choices[0].message.content

    def calculate_total_time(self):
        format = '%Y-%m-%d %H:%M:%S.%f'
        total_time = 0

        for i in range(1, len(self.start_end_times)):
            start_time = datetime.strptime(self.start_end_times[i][0], format)
            end_time = datetime.strptime(self.start_end_times[i][1], format)
            total_time += (end_time - start_time).total_seconds()

        return total_time

    async def create_prediction_with_status(self, interval=5):
        print_task = asyncio.create_task(self.print_status_every(interval))
        await self.create_prediction()
        print_task.cancel()
        print(f"\x1b[32m{self.input.model} finished in {self.calculate_total_time()}\x1b[0m\n")

    async def print_status_every(self, seconds):
        while True:
            print(f"{self.input.model} is still running...")
            await asyncio.sleep(seconds)