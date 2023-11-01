from datetime import datetime

import tiktoken
from dotenv import load_dotenv
from database import setup_db, save_to_db
from openai_model_handler import OpenAiModelHandler, ChatGptInput

load_dotenv()

system_prompt = '''
You are a Typescript professional. 
You don't return any additional text or explanations like "Here's the improved version".
You give no return if you don't understand the given prompt. 
'''
model = "gpt-3.5-turbo"


def num_tokens_from_string(string: str) -> int:
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    num_tokens = len(encoding.encode(string))
    return num_tokens


def get_text_file_string(filename) -> str:
    with open(filename, 'r') as bestand:
        return bestand.read()


def main():
    prompt = get_text_file_string('prompt.txt')
    code = get_text_file_string('code.txt')
    p = prompt.replace('${code}', code)

    gpt_input = ChatGptInput(
        p,
        system_prompt,
        model,
    )
    handler = OpenAiModelHandler(gpt_input)

    prompt_tokens = num_tokens_from_string(p)
    system_tokens = num_tokens_from_string(system_prompt)
    total_input_tokens = prompt_tokens + system_tokens
    print(f"Number of tokens: {total_input_tokens}")

    start_time = datetime.now()
    handler.create_prediction()
    end_time = datetime.now()
    total_time = end_time - start_time
    print(f"Total time: {total_time}")

    message = handler.completion.choices[0].message
    total_output_tokens = num_tokens_from_string(message.content)
    print(message.content + "\n")
    user_correct = input("Correct? y/n")
    correct = False

    if user_correct == 'y':
        correct = True

    save_to_db(str(total_time), p, system_prompt, message.content, total_input_tokens, total_output_tokens, correct)


if __name__ == '__main__':
    setup_db()
    main()
