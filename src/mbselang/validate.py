from __future__ import annotations

from .expressions import comparison_unit, referenced_names
from .model import Assertion, Diagnostic, Model, Perform, SetValue


def validate(model: Model) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    requirements = model.requirements_by_id()

    for requirement in model.requirements.values():
        if not requirement.identifier:
            diagnostics.append(_error("requirement is missing an id", requirement.line))
        if not requirement.shall:
            diagnostics.append(_error(f"requirement {requirement.name!r} is missing shall", requirement.line))
        if requirement.verify_by not in {"test", "analysis", "inspection", "demonstration"}:
            diagnostics.append(_error(f"requirement {requirement.identifier or requirement.name!r} has invalid verify_by", requirement.line))

    for component in model.components.values():
        for part in component.parts.values():
            if part.component_type not in model.components:
                diagnostics.append(_error(f"unknown component type {part.component_type!r}", part.line))
        for requirement_id in component.satisfies:
            if requirement_id not in requirements:
                diagnostics.append(_error(f"unknown requirement {requirement_id!r}", component.line))
        for connection in component.connections:
            source = _resolve_port(model, component.name, connection.source)
            target = _resolve_port(model, component.name, connection.target)
            if source is None:
                diagnostics.append(_error(f"unknown connection endpoint {connection.source!r}", connection.line))
            if target is None:
                diagnostics.append(_error(f"unknown connection endpoint {connection.target!r}", connection.line))
            if source and target:
                if source.direction != "out" or target.direction != "in":
                    diagnostics.append(_error("connections must run from an out port to an in port", connection.line))
                if source.interface != target.interface:
                    diagnostics.append(_error(f"incompatible interfaces {source.interface!r} and {target.interface!r}", connection.line))

    for action in model.actions.values():
        known = set(action.inputs) | set(action.outputs)
        for assignment in action.assignments:
            if assignment.target not in action.outputs:
                diagnostics.append(_error(f"assignment target {assignment.target!r} is not an action output", assignment.line))
            for name in referenced_names(assignment.expression):
                if name not in known:
                    diagnostics.append(_error(f"unknown action value {name!r}", assignment.line))

    known_values = _initial_value_units(model)
    for scenario in model.scenarios.values():
        for requirement_id in scenario.verifies:
            if requirement_id not in requirements:
                diagnostics.append(_error(f"unknown requirement {requirement_id!r}", scenario.line))
        for step in scenario.steps:
            if isinstance(step, SetValue):
                if step.target not in known_values:
                    diagnostics.append(_error(f"unknown scenario target {step.target!r}", step.line))
                elif step.unit and known_values[step.target] != step.unit:
                    diagnostics.append(_error(f"unit mismatch for {step.target}: expected {known_values[step.target]}, got {step.unit}", step.line))
            elif isinstance(step, Perform):
                action = model.actions.get(step.action)
                if action is None:
                    diagnostics.append(_error(f"unknown action {step.action!r}", step.line))
                    continue
                missing = set(action.inputs) - set(step.arguments)
                extra = set(step.arguments) - set(action.inputs)
                if missing:
                    diagnostics.append(_error(f"missing arguments for {step.action}: {', '.join(sorted(missing))}", step.line))
                if extra:
                    diagnostics.append(_error(f"unknown arguments for {step.action}: {', '.join(sorted(extra))}", step.line))
                for output in action.outputs.values():
                    known_values[f"{action.name}.{output.name}"] = output.unit
            elif isinstance(step, Assertion):
                unit = comparison_unit(step.expression)
                left = step.expression.split(maxsplit=1)[0]
                if unit and left in known_values and known_values[left] != unit:
                    diagnostics.append(_error(f"unit mismatch in assertion: {left} is {known_values[left]}, compared with {unit}", step.line))

    verified = {identifier for scenario in model.scenarios.values() for identifier in scenario.verifies}
    for identifier, requirement in requirements.items():
        if identifier not in verified:
            diagnostics.append(Diagnostic("warning", f"requirement {identifier!r} has no verifying scenario", requirement.line))
    return diagnostics


def _initial_value_units(model: Model) -> dict[str, str]:
    values: dict[str, str] = {}
    root = model.components.get(model.name)
    if root:
        for prop in root.properties.values():
            values[f"{model.name.lower()}.{prop.name}"] = prop.unit
    return values


def _resolve_port(model: Model, component_name: str, endpoint: str):
    component = model.components[component_name]
    pieces = endpoint.split(".")
    if len(pieces) == 1:
        return component.ports.get(pieces[0])
    if len(pieces) == 2 and pieces[0] in component.parts:
        part_type = component.parts[pieces[0]].component_type
        target_type = model.components.get(part_type)
        return target_type.ports.get(pieces[1]) if target_type else None
    return None


def _error(message: str, line: int) -> Diagnostic:
    return Diagnostic("error", message, line)

