class Component():
    """
    Базовий інтерфейс Компонента визначає поведінку, яку змінюють декоратори.
    """

    def operation(self) -> str:
        pass


class ConcreteComponent(Component):
    """
    Конкретні Компоненти надають реалізації поведінки за замовчуванням.
    Може існувати кілька варіацій цих класів.
    """

    def operation(self) -> str:
        return "ConcreteComponent"


class Decorator(Component):
    """
    Базовий клас Декоратора слідує тому ж інтерфейсу, що й інші компоненти.
    Основна мета цього класу – визначити інтерфейс обгортки для всіх конкретних декораторів.
    Реалізація коду обгортки за замовчуванням може включати поле для збереження
    загорнутого компонента та засоби його ініціалізації.
    """

    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        """
        Декоратор делегує всю роботу загорнутому компоненту.
        """
        return self._component

    def operation(self) -> str:
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    """
    Конкретні Декоратори викликають загорнутий об'єкт і змінюють його результат
    певним чином.
    """

    def operation(self) -> str:
        """
        Декоратори можуть викликати батьківську реалізацію операції замість
        прямого виклику загорнутого об'єкта. Такий підхід спрощує розширення
        класів декораторів.
        """
        return f"ConcreteDecoratorA({self.component.operation()})"


class ConcreteDecoratorB(Decorator):
    """
    Декоратори можуть виконувати свою поведінку до або після виклику загорнутого
    об'єкта.
    """

    def operation(self) -> str:
        return f"ConcreteDecoratorB({self.component.operation()})"


def client_code(component: Component) -> None:
    """
    Клієнтський код працює з усіма об'єктами, використовуючи інтерфейс Компонента.
    Таким чином, він залишається незалежним від конкретних класів компонентів,
    з якими працює.
    """

    print(f"РЕЗУЛЬТАТ: {component.operation()}", end="")


if __name__ == "__main__":
    # Таким чином, клієнтський код може підтримувати як прості компоненти...
    simple = ConcreteComponent()
    print("Клієнт: У мене є простий компонент:")
    client_code(simple)
    print("\n")

    # ...так і декоровані.
    #
    # Зверніть увагу, що декоратори можуть загортати не лише прості компоненти,
    # а й інші декоратори.
    decorator1 = ConcreteDecoratorA(simple)
    decorator2 = ConcreteDecoratorB(decorator1)
    print("Клієнт: Тепер у мене є декорований компонент:")
    client_code(decorator2)
