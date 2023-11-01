
class ChatGptInput:
    # https://platform.openai.com/docs/api-reference/chat/create
    def __init__(
            self,
            prompt,
            system_prompt,
            model,
            frequency_penalty=None,
            logit_bias=None,
            max_tokens=None,
            n=None,
            presence_penalty=None,
            stop=None,
            stream=False,
            temperature=None,
            top_p=None,
            user=None,
            function_call=None,
            functions=None
    ):
        # Prompt for the conversation.
        self.prompt = prompt

        # System level instructions to guide the model's behavior.
        self.system_prompt = system_prompt

        # The model ID to use for generating responses.
        self.model = model

        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on their existing frequency in the text so far,
        # decreasing the model's likelihood to repeat the same line verbatim.
        self.frequency_penalty = frequency_penalty

        # Modify the likelihood of specified tokens appearing in the completion.
        self.logit_bias = logit_bias

        # Maximum number of tokens in the response.
        self.max_tokens = max_tokens

        # Amount of chat completions to return
        self.n = n

        # Number between -2.0 and 2.0.
        # Positive values penalize new tokens based on whether they appear in the text so far,
        # increasing the model's likelihood to talk about new topics.
        self.presence_penalty = presence_penalty

        # Up to 4 sequences where the API will stop generating further tokens.
        self.stop = stop

        # If set, partial message deltas will be sent
        self.stream = stream

        # What sampling temperature to use, between 0 and 2.
        self.temperature = temperature

        # An alternative to sampling with temperature, called nucleus sampling, where the model considers the results
        # of the tokens with top_p probability mass.
        # So 0.1 means only the tokens comprising the top 10% probability mass are considered.
        # We generally recommend altering this or temperature but not both.
        self.top_p = top_p

        # A unique identifier representing your end-user, which can help OpenAI to monitor and detect abuse.
        self.user = user

        # The specific function call.
        self.function_call = function_call

        # List of available functions.
        self.functions = functions

    def to_dict(self):
        thedict = {
            "model": self.model,
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