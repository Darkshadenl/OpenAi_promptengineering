import time
from dotenv import load_dotenv
from console import ConsoleController
from openai_model_handler import OpenAiModelHandler

load_dotenv()

model = "gpt-3.5-turbo"
prompt = """Update the comments in the given piece:${code}"""
code = """
<RETURNABLE> 
/**
 * Adds two numbers and returns the result.
 * @param num1 - The first number to be added.
 * @param num2 - The second number to be added.
 * @returns The sum of the two numbers.
 */
function addNumbers(num1: number, num2: number): number {
</RETURNABLE> 
  return num1 + num2;
}
"""
prompt = prompt.replace('${code}', code)



def check_predictions_status(handlers):
    for handler in handlers:
        handler.completion.reload()
        handler.update_time_variables()

    return all(handler.completion.status == "succeeded" for handler in handlers)


def main():
    console_controller = ConsoleController()
    handler = OpenAiModelHandler(prompt, console_controller, model)
    handler.create_prediction()
    timer = 0

    while timer < 10:
        time.sleep(1)
        timer += 1
        handler.check_on_prediction()

    print("Done!")



if __name__ == '__main__':
    main()
