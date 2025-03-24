from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Optional


class Handler(ABC):
    """
    Інтерфейс Обробника оголошує метод для побудови ланцюга обробників.
    Також оголошує метод для обробки запиту.
    """

    @abstractmethod
    def set_next(self, handler: Handler) -> Handler:
        pass

    @abstractmethod
    def handle(self, request) -> Optional[str]:
        pass


class AbstractHandler(Handler):
    """
    Типова поведінка ланцюга може бути реалізована в базовому класі
    обробника.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Повернення обробника дозволяє зв’язати обробники в ланцюг ось так:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def handle(self, request: Any) -> str:
        if self._next_handler:
            return self._next_handler.handle(request)

        return None


"""
Кожен Конкретний Обробник або обробляє запит, або передає його
наступному обробнику в ланцюзі.
"""


class MonkeyHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Banana":
            return f"Monkey: Я з'їм {request}"
        else:
            return super().handle(request)


class SquirrelHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "Nut":
            return f"Squirrel: Я з'їм {request}"
        else:
            return super().handle(request)


class DogHandler(AbstractHandler):
    def handle(self, request: Any) -> str:
        if request == "MeatBall":
            return f"Dog: Я з'їм {request}"
        else:
            return super().handle(request)


def client_code(handler: Handler) -> None:
    """
    Зазвичай клієнтський код працює з єдиним обробником.
    У більшості випадків клієнт навіть не знає, що цей обробник є
    частиною ланцюга.
    """

    for food in ["Nut", "Banana", "Cup of coffee"]:
        print(f"\nКлієнт: Хто хоче {food}?")
        result = handler.handle(food)
        if result:
            print(f"  {result}", end="")
        else:
            print(f"  {food} залишилося без уваги.", end="")


if __name__ == "__main__":
    monkey = MonkeyHandler()
    squirrel = SquirrelHandler()
    dog = DogHandler()

    monkey.set_next(squirrel).set_next(dog)

    # Клієнт може відправити запит будь-якому обробнику, а не тільки першому.
    print("Ланцюг: Мавпа > Білка > Собака")
    client_code(monkey)
    print("\n")

    print("Підланцюг: Білка > Собака")
    client_code(squirrel)
