class Llama2ChatInput:

    def __init__(self, prompt, system_prompt, max_new_tokens, min_new_tokens,
                 temperature, top_p, top_k, stop_sequences, seed, debug):
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
            'prompt': self.prompt,
            'system_prompt': self.system_prompt,
            'max_new_tokens': self.max_new_tokens,
            'min_new_tokens': self.min_new_tokens,
            'temperature': self.temperature,
            'top_p': self.top_p,
            'top_k': self.top_k,
            'stop_sequences': self.stop_sequences,
            'seed': self.seed,
            'debug': self.debug
        }