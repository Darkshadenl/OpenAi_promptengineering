def add_line_numbers(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    numbered_lines = []
    for idx, line in enumerate(lines, start=1):
        numbered_line = f'{idx}. {line}'
        numbered_lines.append(numbered_line)

    return ''.join(numbered_lines)


if __name__ == '__main__':
    print(add_line_numbers("code.txt"))
