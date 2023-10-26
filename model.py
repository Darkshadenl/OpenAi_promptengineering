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