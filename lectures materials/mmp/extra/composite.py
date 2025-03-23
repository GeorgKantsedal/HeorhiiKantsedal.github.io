rom __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Component(ABC):
    """
    Базовий клас Компонент оголошує спільні операції як для простих, так і для
    складних об'єктів структури.
    """

    @property
    def parent(self) -> Component:
        return self._parent

    @parent.setter
    def parent(self, parent: Component):
        """
        За необхідності базовий Компонент може оголосити інтерфейс для
        встановлення та отримання батьківського компонента в деревоподібній структурі.
        Він також може надати реалізацію за замовчуванням для цих методів.
        """

        self._parent = parent

    """
    У деяких випадках доцільно визначити операції управління нащадками
    безпосередньо в базовому класі Компонент. Це дозволяє уникнути необхідності
    використання конкретних класів компонентів у клієнтському коді під час
    побудови дерева. Недолік такого підходу в тому, що ці методи будуть порожніми
    для компонентів рівня листа.
    """

    def add(self, component: Component) -> None:
        pass

    def remove(self, component: Component) -> None:
        pass

    def is_composite(self) -> bool:
        """
        Ви можете додати метод, який дозволить клієнтському коду зрозуміти,
        чи може компонент містити вкладені об'єкти.
        """

        return False

    @abstractmethod
    def operation(self) -> str:
        """
        Базовий Компонент може сам реалізувати певну поведінку за замовчуванням
        або передати це конкретним класам, оголосивши метод як абстрактний.
        """

        pass


class Leaf(Component):
    """
    Клас Лист представляє кінцеві об'єкти структури. Лист не може
    мати вкладених компонентів.

    Зазвичай об'єкти Листя виконують фактичну роботу, тоді як об'єкти
    Контейнера лише делегують роботу своїм підкомпонентам.
    """

    def operation(self) -> str:
        return "Лист"


class Composite(Component):
    """
    Клас Контейнер містить складні компоненти, які можуть мати вкладені
    компоненти. Зазвичай об'єкти Контейнери делегують фактичну роботу своїм
    дочірнім елементам, а потім «підсумовують» результат.
    """

    def __init__(self) -> None:
        self._children: List[Component] = []

    """
    Об'єкт контейнера може додавати компоненти у свій список вкладених
    компонентів або видаляти їх, як прості, так і складні.
    """

    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def operation(self) -> str:
        """
        Контейнер виконує свою основну логіку особливим чином. Він проходить
        рекурсивно через усіх своїх дітей, збираючи та підсумовуючи їхні результати.
        Оскільки нащадки контейнера передають ці виклики своїм нащадкам і так
        далі, в результаті обходиться все дерево об'єктів.
        """

        results = []
        for child in self._children:
            results.append(child.operation())
        return f"Гілка({'+'.join(results)})"


def client_code(component: Component) -> None:
    """
    Клієнтський код працює з усіма компонентами через базовий інтерфейс.
    """

    print(f"РЕЗУЛЬТАТ: {component.operation()}", end="")


def client_code2(component1: Component, component2: Component) -> None:
    """
    Завдяки тому, що операції управління нащадками оголошені в базовому класі
    Компонента, клієнтський код може працювати як із простими, так і зі складними
    компонентами, незалежно від їх конкретних класів.
    """

    if component1.is_composite():
        component1.add(component2)

    print(f"РЕЗУЛЬТАТ: {component1.operation()}", end="")


if __name__ == "__main__":
    # Таким чином, клієнтський код може підтримувати прості компоненти-листи...
    simple = Leaf()
    print("Клієнт: У мене є простий компонент:")
    client_code(simple)
    print("\n")

    # ...а також складні контейнери.
    tree = Composite()

    branch1 = Composite()
    branch1.add(Leaf())
    branch1.add(Leaf())

    branch2 = Composite()
    branch2.add(Leaf())

    tree.add(branch1)
    tree.add(branch2)

    print("Клієнт: Тепер у мене є складне дерево:")
    client_code(tree)
    print("\n")

    print("Клієнт: Мені не потрібно перевіряти класи компонентів навіть під час керування деревом:")
    client_code2(tree, simple)
