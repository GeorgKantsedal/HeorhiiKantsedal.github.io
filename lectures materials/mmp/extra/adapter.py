class Target:
    """
    Цільовий клас оголошує інтерфейс, з яким може працювати клієнтський код.
    """

    def request(self) -> str:
        return "Target: The default target's behavior."


class Adaptee:
    """
    Адаптований клас містить корисну поведінку, але його інтерфейс
    несумісний з існуючим клієнтським кодом. Адаптований клас потребує
    деякої доробки, перш ніж клієнтський код зможе його використовувати.
    """

    def specific_request(self) -> str:
        return ".eetpadA eht fo roivaheb laicepS"  # Текст у зворотному порядку


class Adapter(Target, Adaptee):
    """
    Адаптер робить інтерфейс адаптованого класу сумісним із цільовим
    інтерфейсом завдяки множинному успадкуванню.
    """

    def request(self) -> str:
        return f"Adapter: (TRANSLATED) {self.specific_request()[::-1]}"  # Розвертає текст


def client_code(target: "Target") -> None:
    """
    Клієнтський код підтримує всі класи, які використовують інтерфейс Target.
    """

    print(target.request(), end="")


if __name__ == "__main__":
    print("Client: Я можу працювати зі звичайними об'єктами Target:")
    target = Target()
    client_code(target)
    print("\n")

    adaptee = Adaptee()
    print("Client: Клас Adaptee має незрозумілий інтерфейс. "
          "Бачите, я його не розумію:")
    print(f"Adaptee: {adaptee.specific_request()}", end="\n\n")

    print("Client: Але я можу працювати з ним через Adapter:")
    adapter = Adapter()
    client_code(adapter)
