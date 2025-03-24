from __future__ import annotations


class Facade:
    """
    Клас Фасад надає спрощений інтерфейс до складної логіки однієї або
    кількох підсистем. Фасад делегує запити клієнтів відповідним
    об'єктам усередині підсистеми. Також Фасад відповідає за управління їхнім
    життєвим циклом. Усе це захищає клієнта від зайвої складності підсистеми.
    """

    def __init__(self, subsystem1: Subsystem1, subsystem2: Subsystem2) -> None:
        """
        Залежно від потреб вашої програми ви можете надати Фасаду
        існуючі об'єкти підсистеми або дозволити Фасаду створювати їх
        самостійно.
        """

        self._subsystem1 = subsystem1 or Subsystem1()
        self._subsystem2 = subsystem2 or Subsystem2()

    def operation(self) -> str:
        """
        Методи Фасада зручні для швидкого доступу до складного функціоналу
        підсистем. Однак клієнти отримують лише частину можливостей підсистеми.
        """

        results = []
        results.append("Фасад ініціалізує підсистеми:")
        results.append(self._subsystem1.operation1())
        results.append(self._subsystem2.operation1())
        results.append("Фасад дає команди підсистемам виконати дію:")
        results.append(self._subsystem1.operation_n())
        results.append(self._subsystem2.operation_z())
        return "\n".join(results)


class Subsystem1:
    """
    Підсистема може приймати запити як від Фасаду, так і безпосередньо від клієнта.
    У будь-якому випадку, для підсистеми Фасад – це ще один клієнт, і він не є
    частиною підсистеми.
    """

    def operation1(self) -> str:
        return "Підсистема 1: Готова!"

    # ...

    def operation_n(self) -> str:
        return "Підсистема 1: Виконання!"


class Subsystem2:
    """
    Деякі Фасади можуть працювати з різними підсистемами одночасно.
    """

    def operation1(self) -> str:
        return "Підсистема 2: Приготуватися!"

    # ...

    def operation_z(self) -> str:
        return "Підсистема 2: Вогонь!"


def client_code(facade: Facade) -> None:
    """
    Клієнтський код працює зі складними підсистемами через простий інтерфейс,
    наданий Фасадом. Коли Фасад керує життєвим циклом підсистеми,
    клієнт може навіть не знати про існування підсистеми. Такий підхід
    допомагає тримати складність під контролем.
    """

    print(facade.operation(), end="")


if __name__ == "__main__":
    # У клієнтському коді можуть уже бути створені деякі об'єкти підсистеми.
    # У такому випадку може бути доцільним ініціалізувати Фасад із цими
    # об'єктами замість того, щоб дозволяти Фасаду створювати нові екземпляри.
    subsystem1 = Subsystem1()
    subsystem2 = Subsystem2()
    facade = Facade(subsystem1, subsystem2)
    client_code(facade)
