from dotenv import load_dotenv

from console import print_pre_response_output_of_handler, print_post_response_output_of_handler
from database import setup_db, save_to_db
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


def update_handlers_metrics(handlers):
    for handler in handlers:
        handler.update_total_output_tokens()
        handler.update_total_input_tokens()
        handler.update_request_output_tokens()


def add_line_numbers(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    numbered_lines = []
    for idx, line in enumerate(lines, start=1):
        numbered_line = f'{idx}. {line}'
        numbered_lines.append(numbered_line)

    return ''.join(numbered_lines)


async def main():
    code = add_line_numbers('code.txt')
    system_prompt = get_text_file_string('system_prompt.txt')
    prompts = get_file_contents('prompt_1.txt', 'prompt_2.txt')
    prompts_left = len(prompts)
    handlers = []

    for model in models:
        prompt_w_code = prompts['prompt_1.txt'].replace('${code}', code)
        gpt_input = ChatGptInput(prompt_w_code, system_prompt, model)
        handler = OpenAiModelHandler(gpt_input)
        handler.update_request_input_tokens()
        handler.update_total_input_tokens()
        handlers.append(handler)

    time_tracker.start()

    current_prompt = 2
    # keep running until all prompts are done
    while prompts_left > 0:
        [print_pre_response_output_of_handler(handler) for handler in handlers]
        await asyncio.gather(*(handler.create_prediction_with_status(2) for handler in handlers))
        update_handlers_metrics(handlers)
        prompts_left -= 1
        for handler in handlers:
            # add response of ai to messages, so it can be used as input for the next ai request
            handler.update_input_with_gpt_response()
            # add next prompt
            handler.input.add_to_messages('user', prompts[f'prompt_{current_prompt}.txt'])
        current_prompt += 1
        [print_post_response_output_of_handler(handler) for handler in handlers]

    time_tracker.stop()
    print(f"Total time: {time_tracker.total_time}\n")

    for handler in handlers:
        user_correct = input(f"\x1b[31mWas {handler.input.model}'s output Correct? y/n\x1b[0m")
        correct = False

        if user_correct == 'y':
            correct = True

        all_messages = [message['content'] for message in handler.input.messages]
        merged_messages = ' '.join(all_messages)
        save_to_db(handler, merged_messages, correct)



if __name__ == '__main__':
    setup_db()
    asyncio.run(main())
