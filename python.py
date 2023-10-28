from dotenv import load_dotenv
from console import ConsoleController
from openai_model_handler import OpenAiModelHandler

load_dotenv()

prompt = """${code}"""
code = """"""
prompt = prompt.replace('${code}', code)



def check_predictions_status(handlers):
    for handler in handlers:
        handler.prediction.reload()
        handler.update_time_variables()

    return all(handler.prediction.status == "succeeded" for handler in handlers)


def main():
    console_controller = ConsoleController()
    OpenAiModelHandler(prompt, console_controller).create_prediction()



if __name__ == '__main__':
    main()
