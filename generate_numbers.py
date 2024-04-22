from random import choices


def generate_numbers():
    numbers = [num for num in range(1, 11)]
    random_numbers_set = set()

    while len(random_numbers_set) != 4:
        random_numbers_set = set(choices(numbers, k=4))

    random_numbers = [num for num in random_numbers_set]

    return random_numbers
