

class BullsAndCows:

    def __init__(self, random_numbers: list) -> None:
        self.bulls = 0
        self.cows = 0
        self.random_numbers = random_numbers

    def guess_numbers(self, users_numbers: list) -> None:
        bulls = 0
        cows = 0

        for num1, num2 in zip(users_numbers, self.random_numbers):
            if num1 == num2:
                bulls += 1
            elif num1 in self.random_numbers:
                cows += 1

        self.bulls, self.cows = bulls, cows
