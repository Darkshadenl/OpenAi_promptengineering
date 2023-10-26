import time
from dotenv import load_dotenv
import replicate
from model import Llama2ChatInput

load_dotenv()

models = [
        'meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3',
        'meta/llama-2-13b-chat:f4e2de70d66816a838a89eeeb621910adffb0dd0baba3976c96980970978018d'
    ]
prompt = "write me a joke"




class ModelHandler:
    def __init__(self, model_id, prompt):
        self.prediction = None
        self.model_split = model_id.split(':')
        self.model = replicate.models.get(self.model_split[0])
        self.version = self.model.versions.get(self.model_split[1])
        self.input = Llama2ChatInput(prompt)

    def create_prediction(self):
        self.prediction = replicate.predictions.create(
            version=self.version,
            input=self.input.to_dict()
        )

    def print_prediction_status(self):
        status_color = '\033[92m' if self.prediction.status == 'succeeded' else '\033[91m'
        print(f'\033[92m{self.model.id}\033[0m status: {status_color}{self.prediction.status}\033[0m')


def check_predictions_status(handlers):
    for handler in handlers:
        handler.prediction.reload()
    return all(handler.prediction.status == "succeeded" for handler in handlers)


def print_prediction_results(handlers):
    for handler in handlers:
        print(f'\n{handler.model.id} results:\n')
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
