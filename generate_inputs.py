from sys import argv
import json
from typing import (
    List,
    Optional,
    Dict,
    Any,
    Iterator,
)
from decimal import Decimal


class Context:
    def __init__(
        self,
        width: Optional[int],
        height: Optional[int],
        from_value: Optional[str],
        to_value: Optional[str],
        skips: Optional[int],
        target_center: Optional[str],
        output_folder: Optional[str],
        output_filename: Optional[str],
        number_of_iterations: Optional[int],
        zoom: Optional[str],
        **kwargs: Dict[str, Any],
    ):
        self.width = width or 400
        self.height = height or 100
        self.from_value = Decimal(from_value or "0.0")
        self.to_value = Decimal(to_value or "4.0")
        self.target_center = Decimal(target_center or "3.0")
        self.zoom = Decimal(zoom or "0.95")
        self.skips = skips or 0
        self.output_folder = output_folder or "output"
        self.output_filename = output_filename or "n%05d.ppm"
        self.number_of_iterations = number_of_iterations or 10
        self.raw_command = f"python -c \"import generate_image\" -w {self.width} -h {self.height} -f %s -t %s -o {self.output_folder}/{self.output_filename}"
        print(self.raw_command)

    @staticmethod
    def from_file(filename: str) -> Context:
        with open(filename, "r") as fp:
            return Context(**json.loads(fp.read()))

    def next(self) -> Iterator[str]:
        skip_count: int = self.skips
        iteration_count: int = 0
        command: str = ""
        left: Decimal = self.from_value
        right: Decimal = self.to_value
        span: Decimal = right - left
        center: Decimal = span / 2

        while iteration_count < self.number_of_iterations:
            if skip_count > 0:
                skip_count -= 1
            else:
                command = self.raw_command % (str(left), str(right), iteration_count)
                yield command
            
            span *= self.zoom
            center = center + (1 - self.zoom) * (self.target_center - center) 
            left = center - span / 2
            right = center + span / 2
            iteration_count += 1


def main(args: List[str]):
    if len(args) == 0:
        print("Please provide a context file")
    context_filename: str = args[0]
    context = Context.from_file(context_filename)
    for command in context.next():
        print(command)


if __name__ == "generate_inputs":
    main(argv[1:])

