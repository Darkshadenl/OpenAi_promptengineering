import time
from dotenv import load_dotenv
from model import ModelHandler

load_dotenv()

models = [
        'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
        'meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d'
    ]
prompt = "write me a joke"


def check_predictions_status(handlers):
    for handler in handlers:
        handler.prediction.reload()
    return all(handler.prediction.status == "succeeded" for handler in handlers)


def print_prediction_results(handlers):
    for handler in handlers:
        print(f'\n\033[92m{handler.model.id}\033[0m results:\n')
        for item in handler.prediction.output:
            print(item, end="")


def main():
    handlers = [ModelHandler(model_id, prompt) for model_id in models]

    for handler in handlers:
        handler.create_prediction()

    # Wait for predictions to complete
    while not check_predictions_status(handlers):
        time.sleep(3)
        [handler.print_prediction_status() for handler in handlers]

    print_prediction_results(handlers)


if __name__ == '__main__':
    main()
