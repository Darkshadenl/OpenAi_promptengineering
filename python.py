from dotenv import load_dotenv
from openai_model_handler import OpenAiModelHandler, ChatGptInput

load_dotenv()

system_prompt = '''
You are a Typescript professional. 
You are not allowed to change or update any implementation code (code that is not a comment).
You don't return any additional text or explanations like "Here's the improved version".
You give no return if you don't understand the given prompt. 
If you don't know the answer to a question, please don't share false information.
'''
max_tokens = None
min_new_tokens = -1
temperature = 1
top_p = 1
stop_sequences = None
seed = None
debug = True
frequency_penalty = None

model = "gpt-3.5-turbo"
prompt = """
The task is to update existing code comments based on the corresponding code. 
We assume that the code is correct and always the source of truth. 
If there is a discrepancy between the code and the comment, the comment is considered incorrect and needs to be updated 
to align with the code.
Only return what is placed between the tags.   
<RETURNABLE></RETURNABLE> 

If this piece of code is given:
<RETURNABLE> 
/// <summary>
/// Checks if a string contains only alphabets.
/// </summary>
/// <param name="str">The string to check</param>
/// <returns>True if the string is a palindrome, else False</returns>
public bool IsPalindrome(string str)
</RETURNABLE> 
{
    string reversed = new string(str.Reverse().ToArray());
    return str.Equals(reversed, StringComparison.OrdinalIgnoreCase);
}


You return this:
/// <summary>
/// Checks if a string is a palindrome.
/// </summary>
/// <param name="str">The string to check</param>
/// <returns>True if the string is a palindrome, else False</returns>
public bool IsPalindrome(string str)

Here's the code:```typescript ${code} ```
"""
code = """
<RETURNABLE> 
/// <summary>
/// Splits a string by space.
/// </summary>
/// <param name="a">The first string</param>
/// <param name="b">The second string</param>
/// <returns>The concatenated string</returns>
public string ConcatStrings(string a, string b)
</RETURNABLE> 
{
    return a + b;
}
"""
prompt = prompt.replace('${code}', code)


def main():
    gpt_input = ChatGptInput(
        prompt,
        system_prompt,
        model,
        frequency_penalty,
        None,
        max_tokens,
        None,
        None,
        stop_sequences,
        False,
        temperature,
        top_p,
        None,
        None,
        None,
    )
    handler = OpenAiModelHandler(gpt_input)
    handler.create_prediction()

    print("Done!")
    message = handler.completion.choices[0].message
    print(message.content)



if __name__ == '__main__':
    main()
