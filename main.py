from parser_1 import create_json
from cobbler_1 import create_hosts  # супер анти-паттерн импорта со *


if __name__ == "__main__":
    create_json(3, 7)
    create_json(13, 20)
    create_hosts()
