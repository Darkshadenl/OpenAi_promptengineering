from datetime import datetime
from dotenv import load_dotenv
from database import setup_db, save_to_db
from openai_model_handler import OpenAiModelHandler, ChatGptInput


load_dotenv()

system_prompt = '''
You are a Typescript professional. 
You don't return any additional text or explanations like "Here's the improved version".
You give no return if you don't understand the given prompt. 
If you don't know the answer to a question, please don't share false information.
'''

model = "gpt-3.5-turbo"
prompt = """
The task is to update existing code comments based on the corresponding code. 
We assume that the code is correct and always the source of truth. 
If there is a discrepancy between the code and the comment, the comment is considered incorrect and needs to be updated 
to align with the code.
If this piece of code is given:
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

Here's the code that you have to correct:
${code} 
"""
code = """
/// <summary>
/// Converts a string to uppercase.
/// </summary>
/// <param name="input">The string to reverse</param>
/// <returns>The reversed string</returns>
public string ReverseString(string input)
{
    char[] charArray = input.ToCharArray();
    Array.Reverse(charArray);
    return new string(charArray);
}

"""
prompt = prompt.replace('${code}', code)


def main():
    gpt_input = ChatGptInput(
        prompt,
        system_prompt,
        model,
        None,
        None,
        None,
        None,
        None,
        None,
        False,
        None,
        None,
        None,
        None,
        None,
    )
    handler = OpenAiModelHandler(gpt_input)

    start_time = datetime.now()
    handler.create_prediction()
    end_time = datetime.now()

    message = handler.completion.choices[0].message
    print(message.content + "\n")
    user_correct = input("Correct? y/n")
    correct = False

    if user_correct == 'y':
        correct = True

    save_to_db(start_time, end_time, prompt, system_prompt, message.content, correct)


if __name__ == '__main__':
    setup_db()
    main()
