from sys import argv
from typing import Any
from decimal import Decimal, getcontext


STABILIZATION_STEPS: int = 2400
SELECTION_STEPS: int = 1000
HALF: Decimal = Decimal("0.5")
ONE: Decimal = Decimal(1)


def parse_context(args: list[str]) -> dict[str, Any]:
    context: dict[str, Any] = dict()
    state: int = 0

    for arg in args:
        if state == 0:
            if arg == "-w":
                state = 1
            if arg == "-h":
                state = 2
            if arg == "-f":
                state = 3
            if arg == "-t":
                state = 4
            if arg == "-o":
                state = 5
        elif state == 1:
            context["width"] = int(arg)
            state = 0
        elif state == 2:
            context["height"] = int(arg)
            state = 0
        elif state == 3:
            context["from_value"] = Decimal(arg)
            state = 0
        elif state == 4:
            context["to_value"] = Decimal(arg)
            state = 0
        elif state == 5:
            context["output_filename"] = arg 
            state = 0

    return context


def logistic_map(x: Decimal, r: Decimal) -> list[Decimal]:
    stable_points: set[Decimal] = set()

    for _ in range(STABILIZATION_STEPS):
        x = r * x * (ONE - x)

    for _ in range(SELECTION_STEPS):
        x = r * x * (ONE - x)
        if x not in stable_points:
            stable_points.add(x)

    return list(stable_points)


def generate_logistic_map(
    width: int,
    height: int,
    from_value: Decimal,
    to_value: Decimal,
    **kwargs: dict[str, Any],
) -> list[bool]:
    outlet: list[bool] = [False] * (height * width)
    step: Decimal = (to_value - from_value) / width
    r: Decimal = from_value
    points: list[Decimal] = []

    for x in range(width):
        for point in logistic_map(Decimal("0.5"), r):
            y: int = round(height * (ONE - point)) - 1
            outlet[x + y * width] = True
        r += step

    return outlet


def draw_logistic_map(
    outlet: list[bool],
    output_filename: str,
    width: int,
    height: int,
    **kwargs: dict[str, Any],
):
    with open(output_filename, "w") as fp:
        fp.write(f"P1 {width} {height} ")
        for x in outlet:
            fp.write("1 " if x else "0 ")


def main(args: list[str]):
    context: dict[str, Any] = parse_context(args)
    outlet: list[bool] = generate_logistic_map(**context)
    draw_logistic_map(outlet, **context)


if __name__ == "generate_image":
    main(argv[1:])

