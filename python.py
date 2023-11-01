from datetime import datetime
import tiktoken
from dotenv import load_dotenv
from database import setup_db, save_to_db
from openai_model_handler import OpenAiModelHandler, ChatGptInput
import asyncio

load_dotenv()

system_prompt = '''
You are a Typescript professional. 
You don't return any additional text or explanations like "Here's the improved version".
You give no return if you don't understand the given prompt. 
'''
models = ["gpt-3.5-turbo", "gpt-4"]


def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_text_file_string(filename) -> str:
    with open(filename, 'r') as bestand:
        return bestand.read()


async def create_predictions_for_all(objects):
    await asyncio.gather(*(obj.create_prediction() for obj in objects))


async def main():
    prompt = get_text_file_string('prompt.txt')
    code = get_text_file_string('code.txt')
    prompt_w_code = prompt.replace('${code}', code)
    prompt_tokens = num_tokens_from_string(prompt_w_code)
    system_tokens = num_tokens_from_string(system_prompt)
    total_input_tokens = prompt_tokens + system_tokens
    print(f"Number of input tokens for: {total_input_tokens}")

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
    await create_predictions_for_all(handlers)
    global_end_time = datetime.now()
    global_total_time = global_end_time - global_start_time
    print(f"Total time: {global_total_time}")

    for handler in handlers:
        handler_message = handler.completion.choices[0].message
        handler.output_tokens = num_tokens_from_string(handler_message.content)
        print(f"Number of output tokens for {handler.input.model}: {handler.output_tokens}")
        print(f"{handler.input.model} took {handler.total_time} seconds. Results:")
        print(handler_message.content + "\n")


    for handler in handlers:
        user_correct = input(f"Was {handler.input.model}'s output Correct? y/n")
        correct = False

        if user_correct == 'y':
            correct = True
        handler_message = handler.completion.choices[0].message
        save_to_db(str(handler.total_time), prompt_w_code, system_prompt, handler_message.content,
                   total_input_tokens, handler.output_tokens, correct)



if __name__ == '__main__':
    setup_db()
    asyncio.run(main())
