import random

FIRST_BLOCK_SIZE = 7
FIRST_BLOCK_MAX = 35
SECOND_BLOCK_MAX = 54


def generate_ticket(rng: random.Random) -> tuple[tuple[int, ...], int]:
    first_block = tuple(sorted(rng.sample(range(1, FIRST_BLOCK_MAX + 1), FIRST_BLOCK_SIZE)))
    second_block = rng.randint(1, SECOND_BLOCK_MAX)
    return first_block, second_block


def format_ticket(ticket: tuple[tuple[int, ...], int]) -> str:
    first_block, second_block = ticket
    numbers = " ".join(str(number) for number in first_block)
    return f"{numbers} | {second_block}"


def main() -> None:
    print(format_ticket(generate_ticket(random.SystemRandom())))


if __name__ == "__main__":
    main()
