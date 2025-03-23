from __future__ import annotations
from abc import ABC, abstractmethod


class Abstraction:
    """
    Абстракція встановлює інтерфейс для «керуючої» частини двох ієрархій
    класів. Вона містить посилання на об'єкт із ієрархії Реалізації
    та делегує йому всю реальну роботу.
    """

    def __init__(self, implementation: Implementation) -> None:
        self.implementation = implementation

    def operation(self) -> str:
        return (f"Abstraction: Базова операція з:\n"
                f"{self.implementation.operation_implementation()}")


class ExtendedAbstraction(Abstraction):
    """
    Абстракцію можна розширювати без зміни класів Реалізації.
    """

    def operation(self) -> str:
        return (f"ExtendedAbstraction: Розширена операція з:\n"
                f"{self.implementation.operation_implementation()}")


class Implementation(ABC):
    """
    Реалізація визначає інтерфейс для всіх класів реалізації. Вона не обов'язково
    повинна відповідати інтерфейсу Абстракції. На практиці обидва інтерфейси можуть
    бути абсолютно різними. Зазвичай інтерфейс Реалізації містить лише примітивні
    операції, тоді як Абстракція визначає операції вищого рівня, що базуються на цих
    примітивах.
    """

    @abstractmethod
    def operation_implementation(self) -> str:
        pass


"""
Кожна Конкретна Реалізація відповідає певній платформі та реалізує
інтерфейс Реалізації за допомогою API цієї платформи.
"""


class ConcreteImplementationA(Implementation):
    def operation_implementation(self) -> str:
        return "ConcreteImplementationA: Ось результат на платформі A."


class ConcreteImplementationB(Implementation):
    def operation_implementation(self) -> str:
        return "ConcreteImplementationB: Ось результат на платформі B."


def client_code(abstraction: Abstraction) -> None:
    """
    За винятком етапу ініціалізації, коли об'єкт Абстракції пов'язується з
    конкретним об'єктом Реалізації, клієнтський код повинен залежати лише від
    класу Абстракції. Таким чином, клієнтський код може працювати з будь-якою
    комбінацією абстракції та реалізації.
    """

    print(abstraction.operation(), end="")


if __name__ == "__main__":
    """
    Клієнтський код повинен працювати з будь-якою попередньо налаштованою
    комбінацією абстракції та реалізації.
    """

    implementation = ConcreteImplementationA()
    abstraction = Abstraction(implementation)
    client_code(abstraction)

    print("\n")

    implementation = ConcreteImplementationB()
    abstraction = ExtendedAbstraction(implementation)
    client_code(abstraction)