import os
from collections import deque
from Calculation import Calculation
from pynput import keyboard


class Calculator:
    def __init__(self):
        self.history_index = 0
        self.history = deque(maxlen=5)
        self.last_result = None
        self.history_entry = None
        self.first = None
        self.active_listeners = []
        self.lookingForHistory = False
        self.result = None

    def show_history(self):
        """
        Metoda odpowiedzialna za wyświetlanie poprzednich działań na konsoli.

        :return: funkcja nic nie zwraca.
        """
        if self.history:
            print("Historia działań:")
            for i, (expression, result) in enumerate(self.history, 1):
                print(f"{i}. {expression} = {result}")
        else:
            print("Historia działań jest pusta.")

    def get_history_up(self):
        """
        Metoda umożliwia przekazywanie historii wyników działań z self.history 'w górę', po indeksie.

        :return: Wpis z historii działania self.history.
                 Jeśli nie ma historii zwraca komunikat "Brak historii".
        """
        if self.history and self.history_index is not None:
            if self.history_index < len(self.history) - 1:
                self.history_index += 1
            else:
                self.history_index = 0
            _, result = self.history[self.history_index]
            if isinstance(result, (int, float)):
                return result
        return "Brak historii"

    def get_history_down(self):
        """
        Metoda umożliwia przekazywanie historii wyników działań z self.history 'w dół', po indeksie.

        :return: Wpis z historii działania self.history.
                 Jeśli nie ma historii zwraca komunikat "Brak historii".
        """
        if self.history and self.history_index is not None:
            if self.history_index > 0:
                self.history_index -= 1
            else:
                self.history_index = len(self.history) - 1
            _, result = self.history[self.history_index]
            if isinstance(result, (int, float)):
                return result
        return "Brak historii"

    def on_press(self, key):
        """
        Metoda obsługuje kliknięcia klawiatury przycisków. Klawisze up/down służą do wyświetlania liczb z wyników
        z działań historii. Implementuje metody get_history_up() oraz get_history_down()

        :param key: kliknięty przycisk. w metodzie obsługuje kliknięcia: up,down,enter,esc.

        :return: Funkcja nic nie zwraca bezpośrednio (ale zmienia atrybut self.history_entry, który
        zostaje później wykorzystany do zastąpienia ostatniego wyniku wybranym wynikiem z historii działań.
        """
        if self.lookingForHistory:
            if key == keyboard.Key.up:
                self.history_entry = self.get_history_up()
                print("Kolejny wynik z historii:", self.history_entry, ", aby zatwierdzić, kliknij Enter")
            elif key == keyboard.Key.down:
                self.history_entry = self.get_history_down()
                print("Poprzedni wynik z historii:", self.history_entry, ", aby zatwierdzić, kliknij Enter")
            elif key == keyboard.Key.enter:
                for listener in self.active_listeners:
                    listener.stop()
        if key == keyboard.Key.esc:
            for listener in self.active_listeners:
                listener.stop()
            os._exit(0)

    def run(self):
        """
        Jest to główna metoda programu, będącą wątkiem.
        Działa w pętli while do momentu zatrzymania programu.
        w zależności od sytuacji (czy jest to pierwsze działanie od uruchomienia programu czy kolejne)
        informuje użytkownika o sposobie funkcjonowania i kolejnych krokach do realizacji obliczeń.


        :return: Brak.
        """
        print("=== Witaj w programie do kalkulacji. =============")
        print("=== Możliwe działania to: ========================")
        print("+ dodawanie np. 'x + y'")
        print("- odejmowanie np. 'x - y'")
        print("* mnożenie np. 'x * y'")
        print("/ dzielenie np. 'x / y'")
        print("^ potęgi np. 'x ^ y'")
        print("sqrt pierwiastki np. 'sqrt x'")
        print("sin np. 'sin x'")
        print("cos np. 'cos x'")
        print("tan np. 'tan x'")
        print("ctg np. 'ctg x'")
        print("% procenty np. '100 + 5%'")
        print("! silnia np. '5 !'")
        print("!!!KAŻDĄ LICZBĘ/OPERATOR ODDZIELAJ SPACJĄ!!!")

        while True:
            first, second = None, None
            print("==================================================")
            self.show_history()
            print("==================================================")
            if self.last_result is None:
                print("Wprowadź działanie lub wprowadź 'koniec' aby zakończyć działanie programu. ")
                print("W każdym momencie wprowadzania danych, możesz zakończyć działanie programu, klikając ESC")
                expression = input()
                if expression == "koniec":
                    print("Kończenie programu...")
                    break

            elif self.last_result is not None:
                print("Czy chcesz skorzystać z wyniku z historii? (T/N)")
                endlistener = keyboard.Listener(on_press=self.on_press)
                self.active_listeners.append(endlistener)
                endlistener.start()
                decision = input()
                endlistener.stop()
                if decision == "koniec":
                    print("Kończenie programu...")
                    break
                elif decision == 'T':
                    self.lookingForHistory = True
                    print("Wybierz wynik z historii za pomocą strzałek góra/dół")
                    listener = keyboard.Listener(on_press=self.on_press)
                    self.active_listeners.append(listener)
                    listener.start()
                    listener.join()
                    self.last_result = self.history_entry
                    print(f"{self.last_result} ...")
                    first = self.last_result
                    expression = input()
                    expression = input()
                    if expression == "koniec":
                        print("Kończenie programu...")
                        break
                    expression = str(self.last_result) + ' ' + expression

                elif decision == 'N':
                    print(f"{self.last_result} ... wprowadź kolejne działanie (np. '+ x')")
                    endListener = keyboard.Listener(on_press=self.on_press)
                    self.active_listeners.append(endListener)
                    endListener.start()
                    first = self.last_result
                    expression = input()
                    endListener.stop()
                    if expression == "koniec":
                        print("Kończenie programu...")
                        break
                    expression = str(self.last_result) + ' ' + expression
                    print(f"expression: {expression}")
            self.lookingForHistory = False
            parts = expression.split()
            if Calculation.validateExpression(parts) is False:
                print("Nieprawidłowe działanie...")
                continue
            else:
                if len(parts) == 2:
                    first, operator = Calculation.validateExpression(parts)
                    first = float(first)
                    self.result = Calculation.calculate(parts, first, operator)
                elif len(parts) == 3 and len(Calculation.validateExpression(parts)) == 3:
                    first, operator, second = Calculation.validateExpression(parts)
                    first = float(first)
                    second = float(second)
                    self.result = Calculation.calculate(parts, first, operator, second)
                else:
                    first, operator, second, percent = Calculation.validateExpression(parts)
                    first = float(first)
                    second = float(second)
                    self.result = Calculation.calculate(parts, first, operator, second)

            expression = None
            if len(Calculation.validateExpression(parts)) == 4:
                expression = f"{first} {operator} {second}"'%' if second is not None else f"{first} {operator}"
            else:
                if second is None:
                    expression = f"{first} {operator}"
                elif second is not None:
                    expression = f"{first} {operator} {second}"
            self.history.append((expression, self.result))
            self.last_result = self.result
            print(f"Wynik: {self.result}")


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
