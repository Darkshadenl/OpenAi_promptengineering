from datetime import datetime
import tiktoken
from dotenv import load_dotenv
from database import setup_db, save_to_db
from openai_model_handler import OpenAiModelHandler, ChatGptInput
import asyncio

load_dotenv()
models = ["gpt-3.5-turbo", "gpt-4"]


def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_text_file_string(filename) -> str:
    with open(filename, 'r') as bestand:
        return bestand.read()


async def create_predictions_for_all(objects):
    # Start the prediction tasks
    prediction_tasks = asyncio.gather(*(obj.create_prediction_with_status(5) for obj in objects))
    # Wait for all prediction tasks to complete
    await prediction_tasks


async def main():
    prompt = get_text_file_string('prompt.txt')
    system_prompt = get_text_file_string('system_prompt.txt')
    code = get_text_file_string('code.txt')
    prompt_w_code = prompt.replace('${code}', code)
    prompt_tokens = num_tokens_from_string(prompt_w_code)
    system_tokens = num_tokens_from_string(system_prompt)
    total_input_tokens = prompt_tokens + system_tokens
    print("\033[92m" + f"Number of input tokens for: {total_input_tokens}" + "\033[0m")

    gpt_inputs = []
    for model in models:
        gpt_inputs.append(ChatGptInput(
            prompt_w_code,
            system_prompt,
            model,
        ))

    handlers = []
    for gpt_input in gpt_inputs:
        handlers.append(OpenAiModelHandler(gpt_input))

    global_start_time = datetime.now()
    print("\x1b[31mStarting predictions...\x1b[0m")
    await create_predictions_for_all(handlers)
    print("\x1b[32mFinished predictions!\x1b[0m")
    global_end_time = datetime.now()
    global_total_time = global_end_time - global_start_time
    print(f"Total time: {global_total_time}\n")

    for handler in handlers:
        handler_message = handler.completion.choices[0].message
        handler.output_tokens = num_tokens_from_string(handler_message.content)
        print(f"Number of output tokens for {handler.input.model}: {handler.output_tokens}")
        print(f"\x1b[32m{handler.input.model}\x1b[0m took \x1b[34m{handler.total_time}\x1b[0m seconds. Results:\n")
        print(handler_message.content + "\n")

    for handler in handlers:
        user_correct = input(f"\x1b[31mWas {handler.input.model}'s output Correct? y/n\x1b[0m")
        correct = False

        if user_correct == 'y':
            correct = True
        save_to_db(handler, prompt_w_code, system_prompt, total_input_tokens, correct)



if __name__ == '__main__':
    setup_db()
    asyncio.run(main())
