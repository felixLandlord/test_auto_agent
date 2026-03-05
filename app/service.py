import math
from typing import Union

class CalculatorService:
    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @staticmethod
    def modulo(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot perform modulo by zero")
        return a % b

    @staticmethod
    def floor_divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot perform floor division by zero")
        return a // b

    @staticmethod
    def power(base: float, exponent: float) -> float:
        return math.pow(base, exponent)

    @staticmethod
    def square(a: float) -> float:
        return a * a

    @staticmethod
    def root(a: float, n: float = 2) -> float:
        if a < 0 and n % 2 == 0:
            raise ValueError("Cannot take even root of negative number")
        return math.pow(a, 1/n)

    @staticmethod
    def absolute(a: float) -> float:
        return abs(a)

    @staticmethod
    def factorial(a: int) -> int:
        if a < 0:
            raise ValueError("Cannot calculate factorial of a negative number")
        return math.factorial(a)

    @staticmethod
    def log(a: float, base: float = math.e) -> float:
        if a <= 0:
            raise ValueError("Logarithm argument must be positive")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not 1")
        return math.log(a, base)
