from datetime import datetime
import tiktoken
from dotenv import load_dotenv
from database import setup_db, save_to_db
from helpers import num_tokens_from_string
from openai_model_handler import OpenAiModelHandler, ChatGptInput
from time_tracker import Timetracker
import asyncio

load_dotenv()
models = ["gpt-3.5-turbo"]
time_tracker = Timetracker()


def get_text_file_string(filename) -> str:
    with open(filename, 'r') as bestand:
        return bestand.read()


def get_file_contents(*filenames):
    files = {}
    for filename in filenames:
        with open(filename, 'r') as file:
            files[filename] = file.read()
    return files


async def main():
    code = get_text_file_string('code.txt')
    system_prompt = get_text_file_string('system_prompt.txt')
    prompts = get_file_contents('prompt_1.txt', 'prompt_2.txt')
    prompts_left = prompts.__len__()
    handlers = []
    total_input_tokens = 0

    for model in models:
        prompt_w_code = prompts['prompt_1.txt'].replace('${code}', code)
        total_input_tokens = total_input_tokens + num_tokens_from_string(prompt_w_code) if total_input_tokens <= 0 \
            else total_input_tokens

        gpt_input = ChatGptInput(prompt_w_code, system_prompt, model)
        open_ai_model_handler = OpenAiModelHandler(gpt_input)
        handlers.append(open_ai_model_handler)

    total_input_tokens += num_tokens_from_string(system_prompt)
    print("\033[92m" + f"Number of input tokens: {total_input_tokens}" + "\033[0m")
    time_tracker.start()
    await asyncio.gather(*(handler.create_prediction_with_status(5) for handler in handlers))
    prompts_left -= 1

    # keep running until all prompts are done
    while prompts_left > 0:
        for handler in handlers:
            # update output tokens
            handler.update_output_tokens()
            # add response of ai to messages, so it can be used as input for the next ai request
            handler.update_input_with_gpt_response()

        await asyncio.gather(*(handler.create_prediction_with_status(5) for handler in handlers))
        prompts_left -= 1

    time_tracker.stop()
    print(f"Total time: {time_tracker.total_time}\n")

    for handler in handlers:
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
