from datetime import datetime
import replicate

user_system_prompt = '''
You are a Typescript professional. You determine if comments are still up to date, and if not, update them 
while taking the context of the code into account. 
You don't change the code if it not clear what should be changed.
You don't return any text like "Here's the improved version". 
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
If you don't know the answer to a question, please don't share false information.
'''
user_max_new_tokens = 4000
user_min_new_tokens = -1
user_temperature = 0.75
user_top_p = 0.9
user_top_k = 50
user_stop_sequences = None
user_seed = None
user_debug = True


class ReplicateModelHandler:
    def __init__(self, model_id, prompt_string, console_controller):
        self.prediction = None
        self.model_split = model_id.split(':')
        self.model = replicate.models.get(self.model_split[0])
        self.version = self.model.versions.get(self.model_split[1])
        self.input = Llama2ChatInput(prompt_string)  # TODO Inject this input class
        self.console_controller = console_controller
        self.start_time = None
        self.processing_start_time = None
        self.end_time = None

    def create_prediction(self):
        self.prediction = replicate.predictions.create(
            version=self.version,
            input=self.input.to_dict(),

        )
        self.start_time = datetime.now()

    def update_time_variables(self):
        if not self.processing_start_time:
            if self.prediction.status == "processing":
                self.processing_start_time = datetime.now()
            return
        if self.end_time:
            return
        if self.prediction.status == "succeeded":
            self.end_time = datetime.now()

    def print_prediction_status(self):
        self.console_controller.print_prediction_status(self.prediction.status, self.model.id)


class Llama2ChatInput:

    def __init__(self, prompt):
        self.prompt = prompt
        self.system_prompt = user_system_prompt
        self.max_new_tokens = user_max_new_tokens
        self.min_new_tokens = user_min_new_tokens
        self.temperature = user_temperature
        self.top_p = user_top_p
        self.top_k = user_top_k
        self.stop_sequences = user_stop_sequences
        self.seed = user_seed
        self.debug = user_debug

    def to_dict(self):
        thedict = {
            key: value
            for key, value in vars(self).items()
            if value is not None
        }
        return thedict
