import replicate

user_system_prompt = ''
user_max_new_tokens = 128
user_min_new_tokens = -1
user_temperature = 0.75
user_top_p = 0.9
user_top_k = 50
user_stop_sequences = None
user_seed = None
user_debug = None



class ModelHandler:
    def __init__(self, model_id, prompt_string):
        self.prediction = None
        self.model_split = model_id.split(':')
        self.model = replicate.models.get(self.model_split[0])
        self.version = self.model.versions.get(self.model_split[1])
        self.input = Llama2ChatInput(prompt_string)

    def create_prediction(self):
        self.prediction = replicate.predictions.create(
            version=self.version,
            input=self.input.to_dict()
        )

    def print_prediction_status(self):
        status_color = '\033[92m' if self.prediction.status == 'succeeded' else '\033[91m'
        print(f'\033[92m{self.model.id}\033[0m status: {status_color}{self.prediction.status}\033[0m')


class Llama2ChatInput:

    def __init__(self, prompt):
            self.prompt = prompt
            self.user_system_prompt = user_system_prompt
            self.user_max_new_tokens = user_max_new_tokens
            self.user_min_new_tokens = user_min_new_tokens
            self.user_temperature = user_temperature
            self.user_top_p = user_top_p
            self.user_top_k = user_top_k
            self.user_stop_sequences = user_stop_sequences
            self.user_seed = user_seed
            self.debug = user_debug

    def to_dict(self):
        return {
            key: value
            for key, value in vars(self).items()
            if value is not None
        }