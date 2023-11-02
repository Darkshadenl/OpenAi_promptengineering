import tiktoken


def add_line_numbers(text: str):
    result = ""
    for i, line in enumerate(text.splitlines()):
        print(f"{i + 1}. {line}")
        result += f"{i + 1}. {line}\n"
    return result


def num_tokens_from_string(string: str, model: str) -> int:
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(string))
    return num_tokens