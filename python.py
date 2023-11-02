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


async def main():
    code = get_text_file_string('code.txt')
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

    # keep running until all prompts are done
    while prompts_left > 0:
        [print_pre_response_output_of_handler(handler) for handler in handlers]
        await asyncio.gather(*(handler.create_prediction_with_status(5) for handler in handlers))
        update_handlers_metrics(handlers)
        for handler in handlers:
            # add response of ai to messages, so it can be used as input for the next ai request
            handler.update_input_with_gpt_response()
            # add next prompt
            handler.input.add_to_messages(prompts[f'prompt_{prompts_left - 1}.txt'])

        [print_post_response_output_of_handler(handler) for handler in handlers]
        prompts_left -= 1

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
