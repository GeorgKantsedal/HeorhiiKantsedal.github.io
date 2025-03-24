import json
from typing import Dict


class Flyweight():
    """
    Легковаговик зберігає спільну частину стану (так званий внутрішній стан),
    яка належить кільком реальним бізнес-об'єктам.
    Легковаговик приймає залишкову частину стану (зовнішній стан, унікальний
    для кожного об'єкта) через його параметри методу.
    """

    def __init__(self, shared_state: str) -> None:
        self._shared_state = shared_state

    def operation(self, unique_state: str) -> None:
        s = json.dumps(self._shared_state)
        u = json.dumps(unique_state)
        print(f"Легковаговик: Відображення спільного ({s}) та унікального ({u}) стану.", end="")


class FlyweightFactory():
    """
    Фабрика Легковаговиків створює об'єкти-Легковаговики та керує ними.
    Вона забезпечує правильне розподілення легковаговиків.
    Коли клієнт запитує легковаговик, фабрика або повертає існуючий екземпляр,
    або створює новий, якщо його ще не існує.
    """

    _flyweights: Dict[str, Flyweight] = {}

    def __init__(self, initial_flyweights: Dict) -> None:
        for state in initial_flyweights:
            self._flyweights[self.get_key(state)] = Flyweight(state)

    def get_key(self, state: Dict) -> str:
        """
        Повертає хеш-рядок Легковаговика для даного стану.
        """

        return "_".join(sorted(state))

    def get_flyweight(self, shared_state: Dict) -> Flyweight:
        """
        Повертає існуючий Легковаговик із заданим станом або створює новий.
        """

        key = self.get_key(shared_state)

        if not self._flyweights.get(key):
            print("Фабрика Легковаговиків: Не знайдено відповідного легковаговика, створюємо новий.")
            self._flyweights[key] = Flyweight(shared_state)
        else:
            print("Фабрика Легковаговиків: Використання наявного легковаговика.")

        return self._flyweights[key]

    def list_flyweights(self) -> None:
        count = len(self._flyweights)
        print(f"Фабрика Легковаговиків: У мене є {count} легковаговиків:")
        print("\n".join(map(str, self._flyweights.keys())), end="")


def add_car_to_police_database(
    factory: FlyweightFactory, plates: str, owner: str,
    brand: str, model: str, color: str
) -> None:
    print("\n\nКлієнт: Додаємо автомобіль до бази даних.")
    flyweight = factory.get_flyweight([brand, model, color])
    # Клієнтський код або зберігає, або обчислює зовнішній стан і передає
    # його методам легковаговика.
    flyweight.operation([plates, owner])


if __name__ == "__main__":
    """
    Клієнтський код зазвичай створює купу попередньо заповнених легковаговиків
    на етапі ініціалізації програми.
    """

    factory = FlyweightFactory([
        ["Chevrolet", "Camaro2018", "pink"],
        ["Mercedes Benz", "C300", "black"],
        ["Mercedes Benz", "C500", "red"],
        ["BMW", "M5", "red"],
        ["BMW", "X6", "white"],
    ])

    factory.list_flyweights()

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "M5", "red")

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "X1", "red")

    print("\n")

    factory.list_flyweights()
    