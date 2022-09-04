from handlers import input_handler


def hello_parser(user_input, str):
    return "hello", []


def add_parser(user_input, str):
    args = user_input.lstrip("add ")
    username, phone = args.strip().split(" ")
    if username == "" or phone == "":
        raise ValueError("Bad input")
    else:
        return "add", [username, phone]


def change_parser(user_input: str):
    args = user_input.lstrip("change ")
    username, phone = args.strip().split(" ")
    if username == "" or phone == "":
        raise ValueError("Bad input")
    else:
        return "change", [username, phone]


def phone_parser(user_input: str):
    username = user_input.strip().lstrip("phone ")
    if username == "":
        raise ValueError("Bad input")
    else:
        return "phone", [username]


def show_all_parser(user_input: str):
    if user_input == "show all":
        return "show all", []
    else:
        raise ValueError("Bad input")


def exit_parser(user_input: str):
    for item in ["good bye", "close", "exit"]:
        if item == user_input:
            return "exit", []
    raise ValueError("Bad input")


command_parser = {
    "hello": hello_parser,
    "add": add_parser,
    "change": change_parser,
    "phone": phone_parser,
    "show all": show_all_parser,
    "good bye": exit_parser,
    "close": exit_parser,
    "exit": exit_parser,
}


def parse_user_input(user_input: str) -> tuple[str, list]:
    for command in command_parser.keys():
        normalized_input = " ".join(
            list(filter(lambda x: x != "", user_input.lower().split(" ")))
        )
        normalized_input = normalized_input.ljust(len(normalized_input) + 1, " ")
        if normalized_input.startswith(command + " "):
            parser = command_parser.get(command)
            return parser(user_input=normalized_input)
    raise ValueError("Unknown command")
