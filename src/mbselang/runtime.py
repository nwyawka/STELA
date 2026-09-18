from __future__ import annotations

from dataclasses import dataclass, field

from .expressions import ExpressionError, Quantity, comparison_unit, evaluate
from .model import Assertion, Model, Perform, SetValue
from .validate import validate


@dataclass
class AssertionResult:
    expression: str
    passed: bool
    line: int


@dataclass
class RunResult:
    scenario: str
    passed: bool
    assertions: list[AssertionResult] = field(default_factory=list)
    values: dict[str, Quantity] = field(default_factory=dict)
    verified_requirements: list[str] = field(default_factory=list)


class RuntimeError(ValueError):
    pass


def run_scenario(model: Model, scenario_name: str) -> RunResult:
    errors = [item for item in validate(model) if item.severity == "error"]
    if errors:
        raise RuntimeError(f"model has {len(errors)} validation error(s)")
    scenario = model.scenarios.get(scenario_name)
    if scenario is None:
        raise RuntimeError(f"unknown scenario {scenario_name!r}")
    values = _initial_values(model)
    assertions: list[AssertionResult] = []

    for step in scenario.steps:
        try:
            if isinstance(step, SetValue):
                current = values.get(step.target)
                unit = step.unit or (current.unit if current else None)
                values[step.target] = Quantity(float(evaluate(step.expression, values)), unit)
            elif isinstance(step, Perform):
                action = model.actions[step.action]
                local: dict[str, Quantity] = {}
                for name, expression in step.arguments.items():
                    local[name] = Quantity(float(evaluate(expression, values)), action.inputs[name].unit)
                for assignment in action.assignments:
                    unit = action.outputs[assignment.target].unit
                    local[assignment.target] = Quantity(float(evaluate(assignment.expression, local)), unit)
                for output in action.outputs:
                    if output not in local:
                        raise RuntimeError(f"action {action.name!r} did not assign output {output!r}")
                    values[f"{action.name}.{output}"] = local[output]
            elif isinstance(step, Assertion):
                unit = comparison_unit(step.expression)
                left_name = step.expression.split(maxsplit=1)[0]
                if unit and left_name in values and values[left_name].unit != unit:
                    raise RuntimeError(f"assertion unit mismatch at line {step.line}")
                passed = bool(evaluate(step.expression, values))
                assertions.append(AssertionResult(step.expression, passed, step.line))
        except ExpressionError as exc:
            raise RuntimeError(f"line {step.line}: {exc}") from exc

    return RunResult(
        scenario.name,
        all(assertion.passed for assertion in assertions),
        assertions,
        values,
        list(scenario.verifies),
    )


def _initial_values(model: Model) -> dict[str, Quantity]:
    values: dict[str, Quantity] = {}
    root = model.components.get(model.name)
    if root:
        for prop in root.properties.values():
            values[f"{model.name.lower()}.{prop.name}"] = Quantity(prop.value, prop.unit)
    return values

