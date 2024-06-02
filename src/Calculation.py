import math


class Calculation:
    @staticmethod
    def add(x, y):
        return x + y

    @staticmethod
    def addWithPercentage(x, y):
        percentage = y / 100
        result = x + (x * percentage)
        return result
    @staticmethod
    def subtract(x, y):
        return x - y

    def subtractWithPercentage(x, y):
        percentage = y / 100
        result = x - (x * percentage)
        return result

    @staticmethod
    def multiply(x, y):
        return x * y

    def multiplyWithPercentage(x, y):
        percentage = y / 100
        result = x * percentage
        return result

    @staticmethod
    def divide(x, y):
        if y == 0:
            raise ValueError("Nie można dzielić przez zero.")
        return x / y

    def divideWithPercentage(x, y):
        percentage = y / 100
        result = x / percentage
        return result

    @staticmethod
    def power(x, y):
        return x ** y

    @staticmethod
    def square_root(x):
        if x < 0:
            raise ValueError("Nie można obliczyć pierwiastka z liczby ujemnej.")
        return math.sqrt(x)

    @staticmethod
    def percentage(x, previous_result):
        return (previous_result / 100) * x

    @staticmethod
    def factorial(x):
        if x < 0:
            raise ValueError("Nie można obliczyć silni z liczby ujemnej.")
        if x == int(x):
            return math.factorial(int(x))
        else:
            raise ValueError("Liczba musi być naturalna!")

    def sinus(x):
        x = math.sin(x)
        return x

    def cosinus(x):
        x = math.cos(x)
        return x

    def tanges(x):
        x = math.tan(x)
        return x

    def cotanges(x):
        x = 1/(Calculation.tanges(x))
        return x

    @staticmethod
    def validateExpression(parts):
        """
        Metoda waliduje czy dane wprowadzone przez użytkownika są prawidłowe.
        :param parts: będący podzielonym na części wprowadzonym przez użytkownika ciągiem znaków.
        :return : True/False.
        """
        if len(parts) == 1:
            return False
        if len(parts) == 2:
            if Calculation.is_float(parts[0]) and parts[1] in ['sqrt', 'sin', 'cos', 'tan', 'ctg', '!']:
                return parts[0], parts[1]
            else:
                return False

        if len(parts) == 3:
            if Calculation.is_float(parts[0]) and parts[1] in ['+', '-', '*', '/', '^'] and Calculation.is_float(parts[2]):
                return parts[0], parts[1], parts[2]
            elif (Calculation.is_float(parts[0]) and parts[1] in ['+', '-', '*', '/']
                  and Calculation.is_float(parts[2][:-1]) and parts[2][-1] == '%'):
                return parts[0], parts[1], parts[2].rstrip('%'), '%'
            else:
                return False

    @staticmethod
    def calculate(parts, first, operator, second=None):
        """
        Metoda wykonuje obliczenia wprowadzonego przez użytkownika działania.
        :param parts: cały ciąg wprowadzony przez użytkownika.
        :param first: pierwsza część ciągu parts (pierwsza liczba)
        :param operator: druga część ciągu parts (będącą operatorem)
        :param second: trzecia część ciągu parts (druga liczba, opcjonalna)
        :return: wynik obliczenia.
        """
        if len(Calculation.validateExpression(parts)) == 2:
            try:
                if operator == 'sqrt':
                    result = Calculation.square_root(first)
                    return result
                elif operator == 'sin':
                    result = Calculation.sinus(first)
                    return result
                elif operator == 'cos':
                    result = Calculation.cosinus(first)
                    return result
                elif operator == 'tan':
                    result = Calculation.tanges(first)
                    return result
                elif operator == 'ctg':
                    result = Calculation.cotanges(first)
                    return result
                elif operator == '!':
                    result = Calculation.factorial(first)
                    return result
            except ValueError as e:
                print(f"Błąd: {e}")

        if len(Calculation.validateExpression(parts)) == 3:
            try:
                if operator == '+':
                    result = Calculation.add(first, second)
                    return result
                elif operator == '-':
                    result = Calculation.subtract(first, second)
                    return result
                elif operator == '*':
                    result = Calculation.multiply(first, second)
                    return result
                elif operator == '/':
                    result = Calculation.divide(first, second)
                    return result
                elif operator == '^':
                    result = Calculation.power(first, second)
                    return result
            except ValueError as e:
                print(f"Błąd: {e}")

        if len(Calculation.validateExpression(parts)) == 4:
            try:
                if operator == '+':
                    result = Calculation.addWithPercentage(first, second)
                    return result
                elif operator == '-':
                    result = Calculation.subtractWithPercentage(first, second)
                    return result
                elif operator == '*':
                    result = Calculation.multiplyWithPercentage(first, second)
                    return result
                elif operator == '/':
                    result = Calculation.divideWithPercentage(first, second)
                    return result
            except ValueError:
                print(f"Błąd: {e}")

    def is_float(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

