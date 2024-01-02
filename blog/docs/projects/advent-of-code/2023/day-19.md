# Day 19: Aplenty

## Part 1

### Prompt

The Elves of Gear Island are thankful for your help and send you on your way.
They even have a hang glider that someone stole from Desert Island; since you're already going that direction, it would help them a lot if you would use it to get down there and return it to them.

As you reach the bottom of the **relentless avalanche of machine parts**, you discover that they're already forming a formidable heap.
Don't worry, though - a group of Elves is already here organizing the parts, and they have a **system**.

To start, each part is rated in each of four categories:

- `x`: E**x**tremely cool looking
- `m`: **M**usical (it makes a noise when you hit it)
- `a`: **A**erodynamic
- `s`: **S**hiny

Then, each part is sent through a series of **workflows** that will ultimately **accept** or **reject** the part.
Each workflow has a name and contains a list of rules; each rule specifies a condition and where to send the part if the condition is true.
The first rule that matches the part being considered is applied immediately, and the part moves on to the destination described by the rule.
(The last rule in each workflow has no condition and always applies if reached.)

Consider the workflow `ex{x>10:one,m<20:two,a>30:R,A}`.
This workflow is named `ex` and contains four rules.
If workflow `ex` were considering a specific part, it would perform the following steps in order:

- Rule "`x>10:one`": If the part's `x` is more than `10`, send the part to the workflow named `one`.
- Rule "`m<20:two`": Otherwise, if the part's `m` is less than `20`, send the part to the workflow named `two`.
- Rule "`a>30:R`": Otherwise, if the part's `a` is more than `30`, the part is immediately rejected (`R`).
- Rule "`A`": Otherwise, because no other rules matched the part, the part is immediately accepted (`A`).

If a part is sent to another workflow, it immediately switches to the start of that workflow instead and never returns.
If a part is **accepted** (sent to `A`) or **rejected** (sent to `R`), the part immediately stops any further processing.

The system works, but it's not keeping up with the torrent of weird metal shapes.
The Elves ask if you can help sort a few parts and give you the list of workflows and some part ratings (your puzzle input).
For example:

```
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
```

The workflows are listed first, followed by a blank line, then the ratings of the parts the Elves would like you to sort.
All parts begin in the workflow named in.
In this example, the five listed parts go through the following workflows:

- `{x=787,m=2655,a=1222,s=2876}`: `in` -> `qqz` -> `qs` -> `lnx` -> **`A`**
- `{x=1679,m=44,a=2067,s=496}`: `in` -> `px` -> `rfg` -> `gd` -> **`R`**
- `{x=2036,m=264,a=79,s=2244}`: `in` -> `qqz` -> `hdj` -> `pv` -> **`A`**
- `{x=2461,m=1339,a=466,s=291}`: `in` -> `px` -> `qkq` -> `crn` -> **`R`**
- `{x=2127,m=1623,a=2188,s=1013}`: `in` -> `px` -> `rfg` -> **`A`**

Ultimately, three parts are **accepted**.
Adding up the `x`, `m`, `a`, and `s` rating for each of the accepted parts gives `7540` for the part with `x=787`, `4623` for the part with `x=2036`, and `6951` for the part with `x=2127`.
Adding all of the ratings for **all** of the accepted parts gives the sum total of **`19114`**.

Sort through all of the parts you've been given; **what do you get if you add together all of the rating numbers for all of the parts that ultimately get accepted?**

### Solution

Create a map of each key to each workflow, and walk each part through the workflows.

```python
import json
from dataclasses import dataclass

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 19: Aplenty"])


DOCUMENT_EXAMPLE = [
    "px{a<2006:qkq,m>2090:A,rfg}",
    "pv{a>1716:R,A}",
    "lnx{m>1548:A,A}",
    "rfg{s<537:gd,x>2440:R,A}",
    "qs{s>3448:A,lnx}",
    "qkq{x<1416:A,crn}",
    "crn{x>2662:A,R}",
    "in{s<1351:px,qqz}",
    "qqz{s>2770:qs,m<1801:hdj,R}",
    "gd{a>3333:R,R}",
    "hdj{m>838:A,pv}",
    "",
    "{x=787,m=2655,a=1222,s=2876}",
    "{x=1679,m=44,a=2067,s=496}",
    "{x=2036,m=264,a=79,s=2244}",
    "{x=2461,m=1339,a=466,s=291}",
    "{x=2127,m=1623,a=2188,s=1013}",
]


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
```

## Part 2

### Prompt

Even with your help, the sorting process **still** isn't fast enough.

One of the Elves comes up with a new plan: rather than sort parts individually through all of these workflows, maybe you can figure out in advance which combinations of ratings will be accepted or rejected.

Each of the four ratings (`x`, `m`, `a`, `s`) can have an integer value ranging from a minimum of `1` to a maximum of `4000`.
Of **all possible distinct combinations** of ratings, your job is to figure out which ones will be **accepted**.

In the above example, there are **`167409079868000`** distinct combinations of ratings that will be accepted.

Consider only your list of workflows; the list of part ratings that the Elves wanted you to sort is no longer relevant.
**How many distinct combinations of ratings will be accepted by the Elves' workflows?**

### Solution

Same start as Part 1, but we ignore the back-half of the input.
Instead, we calculate the number of possible ranges for each step.

```python
from copy import deepcopy
from dataclasses import dataclass

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 19: Aplenty"])


DOCUMENT_EXAMPLE = [
    "px{a<2006:qkq,m>2090:A,rfg}",
    "pv{a>1716:R,A}",
    "lnx{m>1548:A,A}",
    "rfg{s<537:gd,x>2440:R,A}",
    "qs{s>3448:A,lnx}",
    "qkq{x<1416:A,crn}",
    "crn{x>2662:A,R}",
    "in{s<1351:px,qqz}",
    "qqz{s>2770:qs,m<1801:hdj,R}",
    "gd{a>3333:R,R}",
    "hdj{m>838:A,pv}",
    "",
    "{x=787,m=2655,a=1222,s=2876}",
    "{x=1679,m=44,a=2067,s=496}",
    "{x=2036,m=264,a=79,s=2244}",
    "{x=2461,m=1339,a=466,s=291}",
    "{x=2127,m=1623,a=2188,s=1013}",
]


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


@router.post("/part-2")
async def year_2023_day_19_part_2(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
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
```

## Recap

| Day | Part 1 Time | Part 1 Rank | Part 2 Time | Part 2 Rank |
|-----|-------------|-------------|-------------|-------------|
| 19  | 00:31:38    | 1,809       | 01:21:18    | 1,528       |

I hate range problems 😖.