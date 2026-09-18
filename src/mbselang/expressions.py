from __future__ import annotations

import ast
import operator
import re
from dataclasses import dataclass


class ExpressionError(ValueError):
    pass


@dataclass(frozen=True)
class Quantity:
    value: float
    unit: str | None = None


_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_CMPOPS = {
    ast.Lt: operator.lt,
    ast.LtE: operator.le,
    ast.Gt: operator.gt,
    ast.GtE: operator.ge,
    ast.Eq: operator.eq,
    ast.NotEq: operator.ne,
}


def evaluate(expression: str, values: dict[str, Quantity]) -> float | bool:
    normalized = _replace_dotted_names(_strip_comparison_units(expression), values)
    try:
        tree = ast.parse(normalized, mode="eval")
    except SyntaxError as exc:
        raise ExpressionError(f"invalid expression {expression!r}") from exc
    return _eval(tree.body, values)


def comparison_unit(expression: str) -> str | None:
    match = re.search(r"(?:<=|>=|==|!=|<|>)\s*[-+]?\d+(?:\.\d+)?\s+([^\s)]+)\s*$", expression)
    return match.group(1) if match else None


def referenced_names(expression: str) -> set[str]:
    return set(re.findall(r"\b[A-Za-z_][A-Za-z0-9_.]*\b", expression))


def _strip_comparison_units(expression: str) -> str:
    return re.sub(r"((?:<=|>=|==|!=|<|>)\s*[-+]?\d+(?:\.\d+)?)\s+[^\s)]+", r"\1", expression)


def _replace_dotted_names(expression: str, values: dict[str, Quantity]) -> str:
    result = expression
    for name in sorted(values, key=len, reverse=True):
        if "." in name:
            result = re.sub(rf"(?<![\w.]){re.escape(name)}(?![\w.])", name.replace(".", "__"), result)
    return result


def _eval(node: ast.AST, values: dict[str, Quantity]) -> float | bool:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float, bool)):
        return node.value
    if isinstance(node, ast.Name):
        key = node.id.replace("__", ".")
        if key not in values:
            raise ExpressionError(f"unknown value {key!r}")
        return values[key].value
    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        value = _number(_eval(node.operand, values))
        return value if isinstance(node.op, ast.UAdd) else -value
    if isinstance(node, ast.BinOp) and type(node.op) in _BINOPS:
        return _BINOPS[type(node.op)](_number(_eval(node.left, values)), _number(_eval(node.right, values)))
    if isinstance(node, ast.Compare) and len(node.ops) == 1 and len(node.comparators) == 1:
        op = _CMPOPS.get(type(node.ops[0]))
        if op is None:
            raise ExpressionError("unsupported comparison")
        return op(_number(_eval(node.left, values)), _number(_eval(node.comparators[0], values)))
    raise ExpressionError(f"unsupported expression element {type(node).__name__}")


def _number(value: float | bool) -> float:
    if isinstance(value, bool):
        raise ExpressionError("a Boolean cannot be used as a number")
    return float(value)

