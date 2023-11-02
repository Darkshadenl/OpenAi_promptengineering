from openai_model_handler import OpenAiModelHandler


def print_non_system_input_of_handler(handler):
    for messageDict in handler.input.messages:
        if messageDict['role'] != "system":
            print(f"{str(messageDict['role']).capitalize()}:\n{messageDict['content']}")


def print_total_input_tokens_of_handler(handler: OpenAiModelHandler):
    print("\033[92m" + f"Total input tokens for {handler.input.model}:" + "\033[0m" +
          "\x1b[31m" + f"{handler.total_input_tokens}" + "\x1b[0m")


def print_input_tokens_of_handler(handler: OpenAiModelHandler):
    print("\033[92m" + f"Request input tokens for {handler.input.model}:" + "\033[0m" +
          "\x1b[31m" + f"{handler.request_input_tokens}" + "\x1b[0m")


def print_output_tokens_of_handler(handler: OpenAiModelHandler):
    print("\033[92m" + f"Request output tokens for {handler.input.model}:" + "\033[0m" +
          "\x1b[31m" + f"{handler.request_output_tokens}" + "\x1b[0m")


def print_total_output_tokens_of_handler(handler: OpenAiModelHandler):
    print("\033[92m" + f"Total output tokens for {handler.input.model}:" + "\033[0m" +
          "\x1b[31m" + f"{handler.total_output_tokens}" + "\x1b[0m")


def print_reponse_of_llm(handler: OpenAiModelHandler):
    print(f"Response of {handler.input.model}:\n" + "\033[93m" + f"{handler.get_completion_message()}\n" + "\033[0m")


def print_pre_response_output_of_handler(handler: OpenAiModelHandler):
    print_input_tokens_of_handler(handler)
    print_total_input_tokens_of_handler(handler)
    print_non_system_input_of_handler(handler)


def print_post_response_output_of_handler(handler: OpenAiModelHandler):
    print_output_tokens_of_handler(handler)
    print_total_output_tokens_of_handler(handler)
    print_reponse_of_llm(handler)
