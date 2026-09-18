from __future__ import annotations

from .model import Model


def trace_requirement(model: Model, identifier: str) -> dict[str, object]:
    requirement = model.requirements_by_id().get(identifier)
    if requirement is None:
        raise KeyError(identifier)
    return {
        "id": identifier,
        "name": requirement.name,
        "shall": requirement.shall,
        "verify_by": requirement.verify_by,
        "satisfied_by": [component.name for component in model.components.values() if identifier in component.satisfies],
        "verified_by": [scenario.name for scenario in model.scenarios.values() if identifier in scenario.verifies],
    }

