import abc
import math
from dataclasses import dataclass, field
from typing import Literal

from fastapi import APIRouter, Body

router = APIRouter(tags=["2023 - Day 20: Pulse Propagation"])


DOCUMENT_EXAMPLE = [
    "broadcaster -> a, b, c",
    "%a -> b",
    "%b -> c",
    "%c -> inv",
    "&inv -> a",
]


State = Literal["Low", "High"]


@dataclass
class Event:
    from_module: str

    to_module: str

    state: State


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
    """
    With your help, the Elves manage to find the right parts and fix all of the machines.
    Now, they just need to send the command to boot up the machines and get the sand flowing again.

    The machines are far apart and wired together with long **cables**.
    The cables don't connect to the machines directly, but rather to communication **modules** attached to the machines that perform various initialization tasks and also act as communication relays.

    Modules communicate using **pulses**.
    Each pulse is either a **high pulse** or a **low pulse**.
    When a module sends a pulse, it sends that type of pulse to each module in its list of **destination modules**.

    There are several different types of modules:

    **Flip-flop** modules (prefix `%`) are either **on** or **off**; they are initially **off**.
    If a flip-flop module receives a high pulse, it is ignored and nothing happens.
    However, if a flip-flop module receives a low pulse, it **flips between on and off**.
    If it was off, it turns on and sends a high pulse.
    If it was on, it turns off and sends a low pulse.

    **Conjunction** modules (prefix `&`) **remember** the type of the most recent pulse received from **each** of their connected input modules; they initially default to remembering a **low pulse** for each input.
    When a pulse is received, the conjunction module first updates its memory for that input.
    Then, if it remembers **high pulses** for all inputs, it sends a **low pulse**; otherwise, it sends a **high pulse**.

    There is a single **broadcast module** (named `broadcaster`).
    When it receives a pulse, it sends the same pulse to all of its destination modules.

    Here at Desert Machine Headquarters, there is a module with a single button on it called, aptly, the **button module**.
    When you push the button, a single **low pulse** is sent directly to the `broadcaster` module.

    After pushing the button, you must wait until all pulses have been delivered and fully handled before pushing it again.
    Never push the button if modules are still processing pulses.

    Pulses are always processed **in the order they are sent**.
    So, if a pulse is sent to modules `a`, `b`, and `c`, and then module a processes its pulse and sends more pulses, the pulses sent to modules `b` and `c` would have to be handled first.

    The module configuration (your puzzle input) lists each module.
    The name of the module is preceded by a symbol identifying its type, if any.
    The name is then followed by an arrow and a list of its destination modules.
    For example:

    ```
    broadcaster -> a, b, c
    %a -> b
    %b -> c
    %c -> inv
    &inv -> a
    ```

    In this module configuration, the broadcaster has three destination modules named `a`, `b`, and `c`.
    Each of these modules is a flip-flop module (as indicated by the `%` prefix).
    `a` outputs to `b` which outputs to `c` which outputs to another module named `inv`.
    `inv` is a conjunction module (as indicated by the `&` prefix) which, because it has only one input, acts like an inverter (it sends the opposite of the pulse type it receives); it outputs to `a`.

    By pushing the button once, the following pulses are sent:

    ```
    button -low-> broadcaster
    broadcaster -low-> a
    broadcaster -low-> b
    broadcaster -low-> c
    a -high-> b
    b -high-> c
    c -high-> inv
    inv -low-> a
    a -low-> b
    b -low-> c
    c -low-> inv
    inv -high-> a
    ```

    After this sequence, the flip-flop modules all end up **off**, so pushing the button again repeats the same sequence.

    Here's a more interesting example:

    ```
    broadcaster -> a
    %a -> inv, con
    &inv -> b
    %b -> con
    &con -> output
    ```

    This module configuration includes the `broadcaster`, two flip-flops (named `a` and `b`), a single-input conjunction module (`inv`), a multi-input conjunction module (`con`), and an untyped module named `output` (for testing purposes).
    The multi-input conjunction module `con` watches the two flip-flop modules and, if they're both on, sends a **low pulse** to the `output` module.

    Here's what happens if you push the button once:

    ```
    button -low-> broadcaster
    broadcaster -low-> a
    a -high-> inv
    a -high-> con
    inv -low-> b
    con -high-> output
    b -high-> con
    con -low-> output
    ```

    Both flip-flops turn on and a low pulse is sent to `output`!
    However, now that both flip-flops are on and `con` remembers a high pulse from each of its two inputs, pushing the button a second time does something different:

    ```
    button -low-> broadcaster
    broadcaster -low-> a
    a -low-> inv
    a -low-> con
    inv -high-> b
    con -high-> output
    ```

    Flip-flop `a` turns off! Now, `con` remembers a low pulse from module `a`, and so it sends only a high pulse to `output`.

    Push the button a third time:

    ```
    button -low-> broadcaster
    broadcaster -low-> a
    a -high-> inv
    a -high-> con
    inv -low-> b
    con -low-> output
    b -low-> con
    con -high-> output
    ```

    This time, flip-flop `a` turns on, then flip-flop `b` turns off.
    However, before `b` can turn off, the pulse sent to `con` is handled first, so it **briefly remembers all high pulses** for its inputs and sends a low pulse to `output`.
    After that, flip-flop b turns off, which causes con to update its state and send a high pulse to output.

    Finally, with `a` on and `b` off, push the button a fourth time:

    ```
    button -low-> broadcaster
    broadcaster -low-> a
    a -low-> inv
    a -low-> con
    inv -high-> b
    con -high-> output
    ```

    This completes the cycle: `a` turns off, causing `con` to remember only low pulses and restoring all modules to their original states.

    To get the cables warmed up, the Elves have pushed the button `1000` times.
    How many pulses got sent as a result (including the pulses sent by the button itself)?

    In the first example, the same thing happens every time the button is pushed: `8` low pulses and `4` high pulses are sent.
    So, after pushing the button `1000` times, `8000` low pulses and `4000` high pulses are sent.
    Multiplying these together gives **`32000000`**.

    In the second example, after pushing the button `1000` times, `4250` low pulses and `2750` high pulses are sent.
    Multiplying these together gives **`11687500`**.

    Consult your module configuration; determine the number of low pulses and high pulses that would be sent after pushing the button `1000` times, waiting for all pulses to be fully handled after each push of the button.
    **What do you get if you multiply the total number of low pulses sent by the total number of high pulses sent?**
    """
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
    """
    # Note - The example input will not work for this endpoint

    The final machine responsible for moving the sand down to Island Island has a module attached named `rx`.
    The machine turns on when a **single low pulse** is sent to `rx`.

    Reset all modules to their default states.
    Waiting for all pulses to be fully handled after each button press, **what is the fewest number of button presses required to deliver a single low pulse to the module named `rx`?**
    """
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

    rx_caller = module_map["kh"]
    assert isinstance(rx_caller, Conjunction)

    triggers: dict[str, int] = {_input: math.inf for _input in rx_caller.inputs.keys()}

    button_presses = 0
    events: list[Event] = []

    while button_presses < 1 or not matches_initial_state():
        events.append(Event(to_module="broadcaster", from_module="button", state="Low"))
        button_presses += 1

        while events:
            event = events.pop(0)

            if event.to_module not in module_map:
                continue

            event_module = module_map[event.to_module]

            new_events = event_module.pulse(event.from_module, event.state)
            events += new_events

            if event_module.key in triggers and event_module.output == "High":
                triggers[event_module.key] = min(
                    triggers[event_module.key], button_presses
                )

        if all([value != math.inf for value in triggers.values()]):
            break

    return math.lcm(*triggers.values())
