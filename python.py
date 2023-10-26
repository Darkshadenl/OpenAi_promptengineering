import time
from dotenv import load_dotenv
from console import ConsoleController
from model import ModelHandler

load_dotenv()

models = [
        'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
        'meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d'
    ]


prompt = """
[INST]
Check the comments in the given piece of code. If the comments are not correct, update them.
Replace the text within the <summary></summary>, <param></param> and <returns></returns> blocks with the newly generated comment
if one is applicable. 
Only return the text within <RETURNABLE></RETURNABLE> blocks. 
Comments are not code. Do not add or change any code. COMMENT ONLY.  
Do not add any new comments. UPDATE EXISTING COMMENTS ONLY. 
Do not add any text.[/INST]\n
${code}
"""

code = """
<RETURNABLE>
/// <summary>
/// Finds the minimum of two integers.
/// </summary>
/// <param name="a">The first integer.</param>
/// <param name="b">The second integer.</param>
/// <returns>The minimum of the two integers.</returns>
</RETURNABLE>
public int FindMax(int a, int b)
{
    return (a > b) ? a : b;
}
"""
prompt = prompt.replace('${code}', code)



def check_predictions_status(handlers):
    for handler in handlers:
        handler.prediction.reload()
        handler.update_time_variables()

    return all(handler.prediction.status == "succeeded" for handler in handlers)


def main():
    console_controller = ConsoleController()
    handlers = [ModelHandler(model_id, prompt, console_controller) for model_id in models]

    console_controller.print_and_save_total_start_time()
    for handler in handlers:
        handler.create_prediction()

    # Wait for predictions to complete
    while not check_predictions_status(handlers):
        time.sleep(0.2)
        [handler.print_prediction_status() for handler in handlers]

    print('\n')
    console_controller.print_end_result(handlers)


if __name__ == '__main__':
    main()
