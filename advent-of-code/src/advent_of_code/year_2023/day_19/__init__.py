import json
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

import pytest

Result = str


@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int
    raw: dict[str, int]

    result: Result | None = None

    @property
    def total(self) -> int:
        return self.x + self.m + self.a + self.s

    def __repr__(self) -> str:
        return f"{self.x} | {self.m} | {self.a} | {self.s}"


@dataclass
class Step:
    field: str | None
    operator: str | None
    value: int | None

    result: Result

    @property
    def does_math(self) -> bool:
        return (
            self.field is not None
            and self.operator is not None
            and self.value is not None
        )

    def __repr__(self) -> str:
        if self.field and self.operator and self.value:
            return f"{self.field} {self.operator} {self.value} => {self.result}"

        return self.result

    def result_for_part(self, part: Part) -> Result | None:
        # Returns self.result if passes
        if self.field is None or self.operator is None or self.value is None:
            return self.result

        if self.operator == ">":
            if part.raw[self.field] > self.value:
                return self.result

        if self.operator == "<":
            if part.raw[self.field] < self.value:
                return self.result

        # Returns None if fails
        return None

    @classmethod
    def from_str(cls, raw_value: str) -> "Step":
        if ":" in raw_value:
            condition, result = raw_value.split(":")
            field = condition[0]
            operator = condition[1]
            value = condition[2:]

            return cls(field=field, operator=operator, value=int(value), result=result)

        else:
            return cls(field=None, operator=None, value=None, result=raw_value)


@dataclass
class Workflow:
    steps: list[Step]

    def __repr__(self) -> str:
        return f"{self.steps}"

    def result_for_part(self, part: Part) -> Result:
        for step in self.steps:
            result = step.result_for_part(part)

            if isinstance(result, str):
                return result


def part_1(document: list[str]) -> int:
    reading_workflows = True
    workflows: dict[str, Workflow] = {}
    parts: list[Part] = []

    for line in document:
        # Switch modes
        if line == "":
            reading_workflows = False
            continue

        if reading_workflows:
            key, rest = line.split("{")
            step_strings = rest.replace("}", "").split(",")

            steps = [Step.from_str(value) for value in step_strings]

            workflows[key] = Workflow(steps=steps)

        else:
            json_line = (
                line.replace("x", '"x"')
                .replace("m", '"m"')
                .replace("a", '"a"')
                .replace("s", '"s"')
                .replace("=", ":")
            )
            data = json.loads(json_line)
            parts.append(
                Part(
                    **data,
                    raw=data,
                ),
            )

    for part in parts:
        next_workflow: Workflow | None = workflows["in"]

        while part.result not in ["A", "R"]:
            part.result = next_workflow.result_for_part(part)

            if part.result not in ["A", "R"]:
                next_workflow = workflows[part.result]

    return sum([part.total for part in parts if part.result == "A"])


@dataclass
class Range:
    lower: int
    upper: int


Ranges = dict[str, Range]


def range_combos(ranges: Ranges) -> int:
    count = 1

    for _range in ranges.values():
        count *= _range.upper - _range.lower + 1

    return count


def part_2(document: list[str]) -> int:
    reading_workflows = True
    workflows: dict[str, Workflow] = {}

    for line in document:
        # Switch modes
        if line == "":
            reading_workflows = False
            continue

        if reading_workflows:
            key, rest = line.split("{")
            step_strings = rest.replace("}", "").split(",")

            steps = [Step.from_str(value) for value in step_strings]

            workflows[key] = Workflow(steps=steps)

    def calculate_combos(ranges: Ranges, workflow_id: str) -> int:
        combos = 0

        for step in workflows[workflow_id].steps:
            if step.does_math:
                new_ranges = deepcopy(ranges)

                if step.operator == ">":
                    if new_ranges[step.field].upper > step.value:
                        new_ranges[step.field].lower = max(
                            new_ranges[step.field].lower, step.value + 1
                        )

                        # Step results in accept, get all combos for the new ranges
                        if step.result == "A":
                            combos += range_combos(new_ranges)

                        # We're not counting the rejects
                        elif step.result == "R":
                            pass

                        # Everything else refers to another workflow
                        else:
                            combos += calculate_combos(new_ranges, step.result)

                        # Update base ranges for next steps
                        ranges[step.field].upper = min(
                            ranges[step.field].upper, step.value
                        )

                elif step.operator == "<":
                    if new_ranges[step.field].lower < step.value:
                        new_ranges[step.field].upper = min(
                            new_ranges[step.field].upper, step.value - 1
                        )

                        # Step results in accept, get all combos for the new ranges
                        if step.result == "A":
                            combos += range_combos(new_ranges)

                        # We're not counting the rejects
                        elif step.result == "R":
                            pass

                        # Everything else refers to another workflow
                        else:
                            combos += calculate_combos(new_ranges, step.result)

                        # Update base ranges for next steps
                        ranges[step.field].lower = max(
                            ranges[step.field].lower, step.value
                        )

            else:
                # Base case, our step results in accept
                if step.result == "A":
                    combos += range_combos(ranges)

                # We're not counting the rejects
                elif step.result == "R":
                    pass

                # Everything else refers to another workflow
                else:
                    combos += calculate_combos(ranges, step.result)

        return combos

    return calculate_combos(
        {
            "x": Range(lower=1, upper=4000),
            "m": Range(lower=1, upper=4000),
            "a": Range(lower=1, upper=4000),
            "s": Range(lower=1, upper=4000),
        },
        "in",
    )


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 19114),
        ("input.txt", 348378),
    ],
)
def test_part_1(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_1(file.read().splitlines()) == output


@pytest.mark.parametrize(
    "filename,output",
    [
        ("example.txt", 167409079868000),
        ("input.txt", 121158073425385),
    ],
)
def test_part_2(
    filename: str,
    output: int,
) -> None:
    with open(Path(__file__).with_name(filename), "r") as file:
        assert part_2(file.read().splitlines()) == output
