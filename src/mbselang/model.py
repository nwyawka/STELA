from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Diagnostic:
    severity: str
    message: str
    line: int | None = None


@dataclass
class Requirement:
    name: str
    line: int
    identifier: str = ""
    shall: str = ""
    verify_by: str = ""


@dataclass
class Port:
    name: str
    interface: str
    direction: str
    line: int


@dataclass
class Property:
    name: str
    unit: str
    value: float
    line: int


@dataclass
class Part:
    name: str
    component_type: str
    line: int


@dataclass
class Connection:
    source: str
    target: str
    line: int


@dataclass
class Component:
    name: str
    line: int
    ports: dict[str, Port] = field(default_factory=dict)
    properties: dict[str, Property] = field(default_factory=dict)
    parts: dict[str, Part] = field(default_factory=dict)
    connections: list[Connection] = field(default_factory=list)
    satisfies: list[str] = field(default_factory=list)


@dataclass
class Parameter:
    name: str
    unit: str
    line: int


@dataclass
class Assignment:
    target: str
    expression: str
    line: int


@dataclass
class Action:
    name: str
    line: int
    inputs: dict[str, Parameter] = field(default_factory=dict)
    outputs: dict[str, Parameter] = field(default_factory=dict)
    assignments: list[Assignment] = field(default_factory=list)


@dataclass
class SetValue:
    target: str
    expression: str
    unit: str | None
    line: int


@dataclass
class Perform:
    action: str
    arguments: dict[str, str]
    line: int


@dataclass
class Assertion:
    expression: str
    line: int


ScenarioStep = SetValue | Perform | Assertion


@dataclass
class Scenario:
    name: str
    line: int
    steps: list[ScenarioStep] = field(default_factory=list)
    verifies: list[str] = field(default_factory=list)


@dataclass
class Model:
    name: str
    source: Path | None = None
    requirements: dict[str, Requirement] = field(default_factory=dict)
    components: dict[str, Component] = field(default_factory=dict)
    actions: dict[str, Action] = field(default_factory=dict)
    scenarios: dict[str, Scenario] = field(default_factory=dict)

    def requirements_by_id(self) -> dict[str, Requirement]:
        return {r.identifier: r for r in self.requirements.values() if r.identifier}

