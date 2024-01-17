import os
from dotenv import load_dotenv
from add_line_numbers import add_line_numbers, read_file
from console import print_pre_response_output_of_handler, print_post_response_output_of_handler
from database import setup_db, save_to_db
from openai_model_handler import OpenAiModelHandler, ChatGptInput
from time_tracker import Timetracker
import asyncio

load_dotenv()
models = ["gpt-4-1106-preview"]
time_tracker = Timetracker()
save_to_database = False
save_to_output = True


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


def loop_code_files_and_return_array():
    folder = "code_files"
    files = []
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in [f for f in filenames if f.endswith(".ts")]:
            files.append(os.path.join(dirpath, filename))

    # return array
    return files



async def main():
    codes = loop_code_files_and_return_array()
    # code = add_line_numbers('code.txt')

    code_with_lines = []
    for c in codes:
        code_with_lines.append((f"./{c}", read_file(c)))

    # code_with_lines.append(("./code_files/code.txt", code))
    system_prompt = get_text_file_string('system_prompt.txt')
    prompts = get_file_contents('prompt_for_creating_faulty_comments.txt')
    prompts_left = len(prompts)
    handlers = []

    # first round so always prompt_1
    for model in models:
        for c in code_with_lines:
            if isinstance(c, tuple):
                prompt_w_code = prompts['prompt_for_creating_faulty_comments.txt'].replace('${code}', c[1])
            elif isinstance(c, str):
                prompt_w_code = prompts['prompt_for_creating_faulty_comments.txt'].replace('${code}', c)
            else:
                raise Exception('code is not a string or tuple')

            gpt_input = ChatGptInput(prompt_w_code, system_prompt, model)
            if isinstance(c, tuple):
                handler = OpenAiModelHandler(gpt_input, c[0])
            elif isinstance(c, str):
                handler = OpenAiModelHandler(gpt_input)
            else:
                raise Exception('code is not a string or tuple')

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
            if prompts_left != 0:
                handler.input.add_to_messages('user', prompts[f'prompt_{current_prompt}.txt'])
        current_prompt += 1
        [print_post_response_output_of_handler(handler) for handler in handlers]

    time_tracker.stop()
    print(f"Total time: {time_tracker.total_time}\n")

    for handler in handlers:
        correct = False

        if save_to_database:
            user_correct = input(f"\x1b[31mWas {handler.input.model}'s output Correct? y/n\x1b[0m")

            if user_correct == 'y':
                correct = True

        all_messages = [message['content'] for message in handler.input.messages]
        merged_messages = ' '.join(all_messages)
        handler.calculate_total_time()

        if save_to_database:
            save_to_db(handler, merged_messages, correct)

        if save_to_output:
            output_path = handler.filepath.replace('code_files', 'output')

            # Create directory if it does not exist
            directory = os.path.dirname(output_path)
            if not os.path.exists(directory):
                os.makedirs(directory)

            # Write to the file (will create if file does not exist, or overwrite if it does)
            with open(output_path, 'w') as output_file:
                output_file.write(all_messages[-1])


if __name__ == '__main__':
    setup_db()
    asyncio.run(main())
