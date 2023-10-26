import replicate


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

    def __init__(self, prompt, system_prompt='You are a helpful assistant.',
                 max_new_tokens=128, min_new_tokens=-1,
                 temperature=0.75, top_p=0.9,
                 top_k=50, stop_sequences=None,
                 seed=None, debug=None):
        self.prompt = prompt
        self.system_prompt = system_prompt
        self.max_new_tokens = max_new_tokens
        self.min_new_tokens = min_new_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.stop_sequences = stop_sequences
        self.seed = seed
        self.debug = debug

    def to_dict(self):
        return {
            key: value
            for key, value in vars(self).items()
            if value is not None
        }