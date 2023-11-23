import platform
import os

"""
Класс отвечающий за ввод пользователя
"""


class UserInput:
    """
    Конструктор класса UserInput
    """

    def __init__(self):
        self.__user_system = platform.system()

    """
    Метод очистки консоли
    """

    async def clear_screen(self):
        if self.__user_system == 'Windows':
            os.system('cls')
        else:
            os.system('clear')

    """
    Метод ввода строкового значения
    """

    async def input_string(self, print_value: str) -> str:
        while True:
            user_input = input(f"{print_value}\n>>")
            if user_input == "":
                await self.clear_screen()
                print("\n\nПоле не может быть пустым\n\n")
                continue
            return user_input

    """
    Метод ввода целого числа
    """

    async def input_integer(self, print_value: str) -> int:
        while True:
            try:
                user_input = int(input(f"{print_value}\n>>"))
            except ValueError:
                await self.clear_screen()
                print("\n\nНеобходимо ввести целое число\n\n")
                continue
            return user_input
