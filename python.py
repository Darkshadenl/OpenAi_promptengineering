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
prompt = """
The task is to update existing code comments based on the corresponding code. 
We assume that the code is correct and always the source of truth. 
If there is a discrepancy between the code and the comment, the comment is considered incorrect and needs to be updated 
to align with the code.
example, If this piece of code is given:
/// <summary>
/// Checks if a string contains only alphabets.
/// </summary>
/// <param name="str">The string to check</param>
/// <returns>True if the string is a palindrome, else False</returns>
public bool IsPalindrome(string str)
{
    string reversed = new string(str.Reverse().ToArray());
    return str.Equals(reversed, StringComparison.OrdinalIgnoreCase);
}


You place returnable tags and only return the comment and signature of the class or function:
<RETURNABLE>
/// <summary>
/// Checks if a string is a palindrome.
/// </summary>
/// <param name="str">The string to check</param>
/// <returns>True if the string is a palindrome, else False</returns>
public bool IsPalindrome(string str)
</RETURNABLE>


If a bigger piece of code is given (like a class), you should return multiple comments.  

Here's the code that you have to correct:
${code} 
"""
code = """
/// <summary>
/// Reverses an array of strings.
/// </summary>
/// <param name="strings">The array of strings</param>
/// <returns>The concatenated string</returns>
public string ConcatenateStrings(string[] strings)
{
    return string.Join("", strings);
}

"""


def num_tokens_from_string(string: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
    num_tokens = len(encoding.encode(string))
    return num_tokens


def main():
    p = prompt.replace('${code}', code)
    gpt_input = ChatGptInput(
        p,
        system_prompt,
        model,
    )
    handler = OpenAiModelHandler(gpt_input)

    prompt_tokens = num_tokens_from_string(p)
    system_tokens = num_tokens_from_string(system_prompt)
    total_tokens = prompt_tokens + system_tokens
    print(f"Number of tokens: {total_tokens}")

    start_time = datetime.now()
    handler.create_prediction()
    end_time = datetime.now()
    total_time = end_time - start_time
    print(f"Total time: {total_time}")

    message = handler.completion.choices[0].message
    print(message.content + "\n")
    user_correct = input("Correct? y/n")
    correct = False

    if user_correct == 'y':
        correct = True

    save_to_db(str(total_time), p, system_prompt, message.content, total_tokens, correct)


if __name__ == '__main__':
    setup_db()
    main()
