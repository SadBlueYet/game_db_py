from database import Database
from tabulate import tabulate
from user_input import UserInput


"""
Класс для обработки действий с играми, таких как добавление, редактирование и удаление игр.
"""


class Actions:
    """
    Инициализация класса Actions.
    """
    def __init__(self):

        self.db = Database()
        self.user_input = UserInput()
        self.headers = ["Номер", "Название", "Издатель", "Год публикации"]

    """
    Отображение всех игр.
    """
    async def get_all_games(self):

        await self.user_input.clear_screen()

        cur = await self.db.get_all_games()
        games = await cur.fetchall()

        if not games:
            print("\n\nБаза данных пуста\n\n")
            return

        #  Вывод в формате таблицы
        await self.data_output(games)

    """
    Получение и отображение игры на основе определенных критериев.
    """
    async def get_game(self):
        
        await self.user_input.clear_screen()
        menu = (
            "[1] - Найти игру по названию\n"
            "[2] - Найти игру по издателю\n"
            "[3] - Найти игру по году публикации\n"
            "[0] - Назад"
        )

        user_choice = await self.user_input.input_integer(menu)
        if user_choice == 1:
            game_name = await self.user_input.input_string("Введите название игры")
            cur = await self.db.get_game(game_name=game_name)
        elif user_choice == 2:
            game_publisher = await self.user_input.input_string("Введите издателя игры")
            cur = await self.db.get_game(game_publisher=game_publisher)
        elif user_choice == 3:
            game_year = await self.user_input.input_integer("Введите год публикации игры")
            cur = await self.db.get_game(game_year=game_year)
        elif user_choice == 0:
            await self.user_input.clear_screen()
            return
        else:
            print("\n\nНеверный выбор\n\n")
            return

        game = await cur.fetchall()
        # Если игра не найдена
        if not game:
            print("\n\nИгра не найдена\n\n")
            return

        await self.data_output(game)

    """
    Метод добавления игры
    """
    async def add_game(self) -> None:

        await self.user_input.clear_screen()

        game_title = await self.user_input.input_string("Введите название игры")

        publisher = await self.user_input.input_string("Введите издателя")

        year_of_publication = await self.user_input.input_integer("Введите год публикации игры")

        await self.db.add_game(game_title, publisher, year_of_publication)

        print("\n\nИгра добавлена\n\n")

    """
    Этот метод проверяет, есть ли игра с таким названием в базе данных
    """
    async def check_game(self, game_name: str):

        cur = await self.db.get_game(game_name=game_name)
        games = await cur.fetchall()

        if not games:
            return

        if len(games) > 1:
            while True:
                await self.user_input.clear_screen()
                await self.data_output(games)
                game_id = await self.user_input.input_integer("Введите номер игры")
                for game in games:
                    if game[0] == game_id:
                        return game_id

                print("\n\nНеверный номер\n\n")

        else:
            return games[0][0]

    """
    Редактирование деталей игры на основе ввода пользователя.
    """
    async def edit_game(self):

        await self.user_input.clear_screen()

        menu = (
            "[1] - Изменить название игры\n"
            "[2] - Изменить издателя игры\n"
            "[3] - Изменить год публикации игры\n"
            "[0] - Назад"
        )

        game_name = await self.user_input.input_string("Введите название редактируемой игры")
        game_id = await self.check_game(game_name)

        if game_id is None:
            return

        user_choice = await self.user_input.input_integer(menu)
        # Изменение данных игры
        if user_choice == 1:
            new_name = await self.user_input.input_string("Введите новое название игры")
            await self.db.edit_game(id=game_id, game_name=new_name)
        elif user_choice == 2:
            new_publisher = await self.user_input.input_string("Введите нового издателя игры")
            await self.db.edit_game(id=game_id, game_publisher=new_publisher)
        elif user_choice == 3:
            new_year = await self.user_input.input_integer("Введите новый год публикации игры")
            await self.db.edit_game(id=game_id, game_year=new_year)
        elif user_choice == 0:
            return
        else:
            print("\n\nНеверный выбор\n\n")
            return

        print("\n\nИгра успешно отредактирована\n\n")

    # Удаление игры
    async def delete_game(self):
        await self.user_input.clear_screen()

        game_name = await self.user_input.input_string("Введите название удаляемой игры")
        game_id = await self.check_game(game_name)

        await self.db.delete_game(game_id=game_id)

        print("\n\nИгра удалена\n\n")

    """
    Этот метод выводит игр(у/ы) пользователю в формате таблицы 
    """
    async def data_output(self, data):

        print(tabulate(data, headers=self.headers, tablefmt="fancy_grid"), "\n\n")
