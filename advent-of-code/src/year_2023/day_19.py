import json
from dataclasses import dataclass

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 19: Title"])


DOCUMENT_EXAMPLE = []


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

    def __repr__(self) -> str:
        if self.field and self.operator and self.value:
            return f"{self.field} {self.operator} {self.value} => {self.result}"

        return self.result

    def result_for_part(self, part: Part) -> Result | None:
        # Returns self.result if passes
        if self.field is None or self.operator is None or self.value is None:
            return self.result

        if self.operator == ">":
            if part.raw[self.field] > int(self.value):
                return self.result

        if self.operator == "<":
            if part.raw[self.field] < int(self.value):
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

            return cls(field=field, operator=operator, value=value, result=result)

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


@router.post("/part-1")
async def year_2023_day_19_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
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


@router.post("/part-2")
async def year_2023_day_19_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    total = 0

    for line in document:
        pass

    return total
