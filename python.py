from datetime import datetime
import tiktoken
from dotenv import load_dotenv
from database import setup_db, save_to_db
from openai_model_handler import OpenAiModelHandler, ChatGptInput
from time_tracker import Timetracker
import asyncio

load_dotenv()
models = ["gpt-4"]
time_tracker = Timetracker()


def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_text_file_string(filename) -> str:
    with open(filename, 'r') as bestand:
        return bestand.read()


def get_file_contents(*filenames):
    files = {}
    for filename in filenames:
        with open(filename, 'r') as file:
            files[filename] = file.read()
    return files


async def create_predictions_for_all(objects):
    # Start the prediction tasks
    prediction_tasks = asyncio.gather(*(obj.create_prediction_with_status(5) for obj in objects))
    # Wait for all prediction tasks to complete
    await prediction_tasks


async def main():
    code = get_text_file_string('code.txt')
    system_prompt = get_text_file_string('system_prompt.txt')

    prompts = get_file_contents('prompt_1.txt', 'prompt_2.txt')

    handlers = []
    total_input_tokens = 0
    for key, value in prompts.items():
        prompt_w_code = value.replace('${code}', code)
        prompt_tokens = num_tokens_from_string(prompt_w_code) if total_input_tokens <= 0 else total_input_tokens

        for model in models:
            gpt_input = ChatGptInput(prompt_w_code, system_prompt, model)
            open_ai_model_handler = OpenAiModelHandler(gpt_input)
            handlers.append(open_ai_model_handler)

    total_input_tokens += num_tokens_from_string(system_prompt)
    print("\033[92m" + f"Number of input tokens: {total_input_tokens}" + "\033[0m")

    time_tracker.start()

    await create_predictions_for_all(handlers)

    time_tracker.stop()
    print(f"Total time: {time_tracker.total_time}\n")

    for handler in handlers:
        handler_message = handler.completion.choices[0].message
        handler.output_tokens = num_tokens_from_string(handler_message.content)

        print(f"Number of output tokens for {handler.input.model}: {handler.output_tokens}")
        print(f"\x1b[32m{handler.input.model}\x1b[0m took \x1b[34m{handler.total_time}\x1b[0m seconds. Results:\n")
        print(handler_message.content + "\n")

        user_correct = input(f"\x1b[31mWas {handler.input.model}'s output Correct? y/n\x1b[0m")
        correct = False

        if user_correct == 'y':
            correct = True

        # save_to_db(handler, prompt_w_code, system_prompt, total_input_tokens, correct)



if __name__ == '__main__':
    setup_db()
    asyncio.run(main())
