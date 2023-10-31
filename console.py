import os
from datetime import datetime
from openai_model_handler import OpenAiModelHandler


class ConsoleController:

    def __init__(self):
        self.end_time = None
        self.start_time = None

    def print_end_result(self, handlers):
        self.print_total_start_time()
        self.print_and_save_total_end_time()
        self.print_and_save_total_elapsed_time()
        print("\n")
        # [self.print_model_processing_time(handler) for handler in handlers]
        # [self.print_model_elapsed_time(handler) for handler in handlers]
        self.print_prediction_results(handlers)

    def print_prediction_results(self, handlers):
        for handler in handlers:
            print(f'\n\033[92m{handler.model.id}\033[0m results:\n')
            for item in handler.completion.output:
                print(item, end="")

    def print_prediction_status(self, status, model_name):
        status_color = '\033[92m' if status == 'succeeded' else '\033[91m'
        print(f'\033[92m{model_name}\033[0m status: {status_color}{status}\033[0m')

    def print_and_save_total_start_time(self):
        self.start_time = datetime.now()
        print(f"Start time: {self.start_time}")

    def print_total_start_time(self):
        print(f"Start time: {self.start_time}")


    # def print_model_processing_time(self, model: OpenAiModelHandler):
    #     print(f"\033[92m{model.model.id}\033[0m processing time: {model.end_time - model.processing_start_time}")
    #
    # def print_model_elapsed_time(self, model: OpenAiModelHandler):
    #     print(f"\033[92m{model.model.id}\033[0m elapsed time: {model.end_time - model.start_time}")

    def print_and_save_total_end_time(self):
        self.end_time = datetime.now()
        print(f"All predictions end time: {self.end_time}")

    def print_and_save_total_elapsed_time(self):
        elapsed_time = self.end_time - self.start_time
        print(f"Total elapsed time: {elapsed_time}")