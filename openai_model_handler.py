import math
from datetime import datetime
import openai

user_system_prompt = '''
You are a Typescript professional. You determine if comments are still up to date, and if not, update them 
while taking the context of the code into account. 
You don't change the code if it not clear what should be changed.
You don't return any text like "Here's the improved version". 
If a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. 
If you don't know the answer to a question, please don't share false information.
'''
user_max_tokens = math.inf
user_min_new_tokens = -1
user_temperature = 0.75
user_top_p = 0.9
user_top_k = 50
user_stop_sequences = None
user_seed = None
user_debug = True


class OpenAiModelHandler:
    def __init__(self, prompt_string, console_controller):
        self.prediction = None
        self.model = "gpt-3.5-turbo"
        self.input = ChatGptInput(prompt_string)  # TODO Inject this input class
        self.console_controller = console_controller
        self.start_time = None
        self.processing_start_time = None
        self.end_time = None

    def create_prediction(self):
        self.prediction = openai.ChatCompletion.create(
            **self.input.to_dict()
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


class ChatGptInput:
    # https://platform.openai.com/docs/api-reference/chat/create
    def __init__(self, prompt):
        self.prompt = prompt
        self.system_prompt = user_system_prompt
        self.model = "gpt-3.5-turbo"

        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on their existing frequency in the text so far,
        # decreasing the model's likelihood to repeat the same line verbatim.
        self.frequency_penalty = None

        # Modify the likelihood of specified tokens appearing in the completion.
        self.logit_bias = None
        self.max_tokens = user_max_tokens

        # Amount of chat completions to return
        self.n = None

        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on whether they appear in the text so far,
        # increasing the model's likelihood to talk about new topics.
        self.presence_penalty = None

        # Up to 4 sequences where the API will stop generating further tokens.
        self.stop = None

        # If set, partial message deltas will be sent
        self.stream = True

        # What sampling temperature to use, between 0 and 2.
        self.temperature = user_temperature

        # An alternative to sampling with temperature, called nucleus sampling, where the model considers the results
        # of the tokens with top_p probability mass.
        # So 0.1 means only the tokens comprising the top 10% probability mass are considered.
        # We generally  recommend altering this or temperature but not both.
        self.top_p = user_top_k
        # A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.
        self.user = None
        self.function_call = None
        self.functions = None

    def to_dict(self):
        thedict = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt
                },
                {
                    "role": "user",
                    "content": self.prompt
                }
            ]
        }
        thedict.update(
            {key: value
             for key, value in vars(self).items()
             if value is not None and key not in ["system_prompt", "prompt"]})
        return thedict
