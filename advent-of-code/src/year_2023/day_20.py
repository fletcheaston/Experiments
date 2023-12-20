import abc
from dataclasses import dataclass, field
from typing import Literal

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 20: Title"])


DOCUMENT_EXAMPLE = []


State = Literal["Low", "High"]


@dataclass
class Event:
    from_module: str

    to_module: str

    state: State

    def __repr__(self) -> str:
        return f"{self.from_module} -> {self.state} -> {self.to_module}"


@dataclass
class BaseModule(abc.ABC):
    key: str
    next_modules: list[str]

    @property
    @abc.abstractmethod
    def output(self) -> State | None:
        ...

    @abc.abstractmethod
    def pulse(self, module: str, state: State) -> list[Event]:
        ...


@dataclass
class Broadcast(BaseModule):
    @property
    def output(self) -> State | None:
        return "Low"

    def pulse(self, module: str, state: State) -> list[Event]:
        return [
            Event(
                from_module=self.key,
                to_module=next_module,
                state=self.output,
            )
            for next_module in self.next_modules
        ]


@dataclass
class FlipFlop(BaseModule):
    on: bool = False

    @property
    def output(self) -> State | None:
        if self.on:
            return "High"

        return "Low"

    def pulse(self, module: str, state: State) -> list[Event]:
        if state == "High":
            return []

        elif state == "Low":
            self.on = not self.on

            return [
                Event(
                    from_module=self.key,
                    to_module=next_module,
                    state=self.output,
                )
                for next_module in self.next_modules
            ]


@dataclass
class Conjunction(BaseModule):
    inputs: dict[str, State] = field(default_factory=dict)

    @property
    def output(self) -> State | None:
        if all([state == "High" for state in self.inputs.values()]):
            return "Low"

        return "High"

    def add_input(self, module: str) -> None:
        self.inputs[module] = "Low"

    def pulse(self, module: str, state: State) -> list[Event]:
        self.inputs[module] = state

        return [
            Event(
                from_module=self.key,
                to_module=next_module,
                state=self.output,
            )
            for next_module in self.next_modules
        ]


@router.post("/part-1")
async def year_2023_day_20_part_1(
    document: list[str] = Body(
        ...,
        embed=True,
        examples=[DOCUMENT_EXAMPLE],
    ),
) -> int:
    module_map: dict[str, BaseModule] = {}
    conjunctions: set[str] = set()

    # Parse inputs to a "module map"
    # Also pull out the conjunction keys
    for line in document:
        key, output = line.split(" -> ")
        outputs = [value.strip() for value in output.split(",")]

        if key == "broadcaster":
            module_map[key] = Broadcast(key=key, next_modules=outputs)

        elif key.startswith("%"):
            key = key.replace("%", "")
            module_map[key] = FlipFlop(key=key, next_modules=outputs)

        elif key.startswith("&"):
            key = key.replace("&", "")
            module_map[key] = Conjunction(key=key, next_modules=outputs)
            conjunctions.add(key)

        else:
            raise ValueError

    # Run through all modules
    # If they have any conjunctions, update said conjunction
    for key, module in module_map.items():
        for next_module in module.next_modules:
            if next_module in conjunctions:
                # Add to module inputs
                conjunction_module = module_map[next_module]
                assert isinstance(conjunction_module, Conjunction)
                conjunction_module.add_input(key)

    # Get the initial output state of all modules
    initial_state: dict[str, State] = {}

    for key, module in module_map.items():
        initial_state[key] = module.output

    # Callback for comparing against initial state
    def matches_initial_state() -> bool:
        for _key, _module in module_map.items():
            if initial_state[_key] != _module.output:
                return False

        return True

    # Fire events off one at a time
    steps_to_cycle = 0
    button_presses = 0
    pulses: dict[State, int] = {
        "High": 0,  # 11
        "Low": 0,  # 17
    }
    events: list[Event] = []

    while steps_to_cycle < 1 or not matches_initial_state():
        events.append(Event(to_module="broadcaster", from_module="button", state="Low"))
        button_presses += 1
        pulses["Low"] += 1

        # print(button_presses, steps_to_cycle)

        while events:
            steps_to_cycle += 1
            event = events.pop(0)

            if event.to_module not in module_map:
                continue

            event_module = module_map[event.to_module]

            new_events = event_module.pulse(event.from_module, event.state)
            events += new_events

            for new_event in new_events:
                pulses[new_event.state] += 1

        if button_presses >= 1000:
            break

    button_cycles = 1000 // button_presses

    return (pulses["Low"] * button_cycles * pulses["High"]) * button_cycles


@router.post("/part-2")
async def year_2023_day_20_part_2(
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
