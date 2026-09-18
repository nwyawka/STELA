from __future__ import annotations

import re
from pathlib import Path

from .model import (
    Action,
    Assertion,
    Assignment,
    Component,
    Connection,
    Model,
    Parameter,
    Part,
    Perform,
    Port,
    Property,
    Requirement,
    Scenario,
    SetValue,
)


class ParseError(ValueError):
    def __init__(self, message: str, line: int):
        super().__init__(f"line {line}: {message}")
        self.line = line


_NAME = r"[A-Za-z_][A-Za-z0-9_]*"


def load(path: str | Path) -> Model:
    source = Path(path)
    return parse(source.read_text(encoding="utf-8"), source=source)


def parse(text: str, source: Path | None = None) -> Model:
    model: Model | None = None
    current: Requirement | Component | Action | Scenario | None = None

    for line_number, raw in enumerate(text.splitlines(), 1):
        without_comment = raw.split("#", 1)[0].rstrip()
        if not without_comment.strip():
            continue
        leading = without_comment[: len(without_comment) - len(without_comment.lstrip())]
        if " " in leading and "\t" in leading:
            raise ParseError("do not mix spaces and tabs in indentation", line_number)
        if leading and leading not in {"    ", "\t"}:
            raise ParseError("members must use exactly four spaces or one tab", line_number)
        indent = 0 if not leading else 1
        content = without_comment.strip()

        if indent == 0:
            current = None
            match = re.fullmatch(rf"model\s+({_NAME})", content)
            if match:
                if model is not None:
                    raise ParseError("only one model declaration is allowed", line_number)
                model = Model(match.group(1), source)
                continue
            if model is None:
                raise ParseError("the first declaration must be a model", line_number)
            match = re.fullmatch(rf"requirement\s+({_NAME}):", content)
            if match:
                current = Requirement(match.group(1), line_number)
                _add_unique(model.requirements, current.name, current, line_number)
                continue
            match = re.fullmatch(rf"component\s+({_NAME}):", content)
            if match:
                current = Component(match.group(1), line_number)
                _add_unique(model.components, current.name, current, line_number)
                continue
            match = re.fullmatch(rf"action\s+({_NAME}):", content)
            if match:
                current = Action(match.group(1), line_number)
                _add_unique(model.actions, current.name, current, line_number)
                continue
            match = re.fullmatch(rf"scenario\s+({_NAME}):", content)
            if match:
                current = Scenario(match.group(1), line_number)
                _add_unique(model.scenarios, current.name, current, line_number)
                continue
            raise ParseError(f"unknown top-level declaration: {content}", line_number)

        if indent != 1 or current is None or model is None:
            raise ParseError("members must be indented by four spaces or one tab", line_number)
        _parse_member(current, content, line_number)

    if model is None:
        raise ParseError("missing model declaration", 1)
    return model


def _add_unique(collection: dict, name: str, value: object, line: int) -> None:
    if name in collection:
        raise ParseError(f"duplicate declaration {name!r}", line)
    collection[name] = value


def _parse_member(owner: object, content: str, line: int) -> None:
    if isinstance(owner, Requirement):
        if content.startswith("id:"):
            owner.identifier = content[3:].strip()
        elif content.startswith("shall "):
            owner.shall = content[6:].strip()
        elif content.startswith("verify_by "):
            owner.verify_by = content[10:].strip()
        else:
            raise ParseError(f"unknown requirement member: {content}", line)
        return

    if isinstance(owner, Component):
        match = re.fullmatch(rf"port\s+({_NAME}):\s*({_NAME})\s+(in|out)", content)
        if match:
            port = Port(match.group(1), match.group(2), match.group(3), line)
            _add_unique(owner.ports, port.name, port, line)
            return
        match = re.fullmatch(rf"property\s+({_NAME}):\s*(\S+)\s*=\s*([-+]?\d+(?:\.\d+)?)", content)
        if match:
            prop = Property(match.group(1), match.group(2), float(match.group(3)), line)
            _add_unique(owner.properties, prop.name, prop, line)
            return
        match = re.fullmatch(rf"part\s+({_NAME}):\s*({_NAME})", content)
        if match:
            part = Part(match.group(1), match.group(2), line)
            _add_unique(owner.parts, part.name, part, line)
            return
        match = re.fullmatch(r"connect\s+(\S+)\s*->\s*(\S+)", content)
        if match:
            owner.connections.append(Connection(match.group(1), match.group(2), line))
            return
        if content.startswith("satisfies "):
            owner.satisfies.append(content[10:].strip())
            return
        raise ParseError(f"unknown component member: {content}", line)

    if isinstance(owner, Action):
        match = re.fullmatch(rf"(input|output)\s+({_NAME}):\s*(\S+)", content)
        if match:
            parameter = Parameter(match.group(2), match.group(3), line)
            collection = owner.inputs if match.group(1) == "input" else owner.outputs
            _add_unique(collection, parameter.name, parameter, line)
            return
        match = re.fullmatch(rf"set\s+({_NAME})\s*=\s*(.+)", content)
        if match:
            owner.assignments.append(Assignment(match.group(1), match.group(2), line))
            return
        raise ParseError(f"unknown action member: {content}", line)

    if isinstance(owner, Scenario):
        match = re.fullmatch(r"set\s+([A-Za-z_][\w.]*)\s*=\s*(.+)", content)
        if match:
            expression, unit = _split_value_unit(match.group(2))
            owner.steps.append(SetValue(match.group(1), expression, unit, line))
            return
        match = re.fullmatch(rf"perform\s+({_NAME})(?:\s+with\s+(.+))?", content)
        if match:
            arguments: dict[str, str] = {}
            if match.group(2):
                for item in match.group(2).split(","):
                    if "=" not in item:
                        raise ParseError("perform arguments use name = expression", line)
                    name, expression = item.split("=", 1)
                    arguments[name.strip()] = expression.strip()
            owner.steps.append(Perform(match.group(1), arguments, line))
            return
        if content.startswith("assert "):
            owner.steps.append(Assertion(content[7:].strip(), line))
            return
        if content.startswith("verifies "):
            owner.verifies.append(content[9:].strip())
            return
        raise ParseError(f"unknown scenario member: {content}", line)


def _split_value_unit(value: str) -> tuple[str, str | None]:
    match = re.fullmatch(r"([-+]?\d+(?:\.\d+)?)\s+([^\s]+)", value.strip())
    if match:
        return match.group(1), match.group(2)
    return value.strip(), None
