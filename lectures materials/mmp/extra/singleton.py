from threading import Lock, Thread


class SingletonMeta(type):
    """
    Це потокобезпечна реалізація класу Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    Тепер у нас є об'єкт-блокування для синхронізації потоків під час
    першого доступу до Одинака.
    """

    def __call__(cls, *args, **kwargs):
        """
        Дана реалізація не враховує можливу зміну переданих
        аргументів у `__init__`.
        """
        # Тепер уявіть, що програма тільки-но запустилася.
        # Об'єкт-одинак ще ніхто не створював, тому кілька потоків
        # цілком могли одночасно пройти через попередню умову і досягти
        # блокування. Найшвидший потік поставить блокування і зайде всередину
        # секції, тоді як інші потоки чекатимуть тут.
        with cls._lock:
            # Перший потік досягає цієї умови і проходить всередину, створюючи
            # об'єкт-одинак. Як тільки цей потік вийде із секції та звільнить
            # блокування, наступний потік може знову встановити блокування і
            # зайти всередину. Однак тепер екземпляр одинака вже буде створений, і
            # потік не зможе пройти через цю умову, а отже, новий об'єкт не
            # буде створений.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    value: str = None
    """
    Ми використовуємо це поле, щоб довести, що наш Одинак дійсно
    працює.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def some_business_logic(self):
        """
        Нарешті, будь-який Одинак повинен містити певну бізнес-логіку,
        яка може виконуватися на його екземплярі.
        """


def test_singleton(value: str) -> None:
    singleton = Singleton(value)
    print(singleton.value)


if __name__ == "__main__":
    # Клієнтський код.

    print("Якщо ви бачите однакове значення, значить, одинак повторно використовується (ура!)\n"
          "Якщо ви бачите різні значення, "
          "значить, було створено 2 одинаки (ой-йой!)\n\n"
          "РЕЗУЛЬТАТ:\n")

    process1 = Thread(target=test_singleton, args=("FOO",))
    process2 = Thread(target=test_singleton, args=("BAR",))
    process1.start()
    process2.start()
