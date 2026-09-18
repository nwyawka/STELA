from __future__ import annotations

import argparse
import json
from pathlib import Path

from .parser import ParseError, load
from .render import render_mermaid
from .runtime import RuntimeError as ModelRuntimeError
from .runtime import run_scenario
from .trace import trace_requirement
from .validate import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="mbse", description="Validate and execute mbseLang models")
    subparsers = parser.add_subparsers(dest="command", required=True)
    for command in ("check", "run", "trace", "render"):
        sub = subparsers.add_parser(command)
        sub.add_argument("model", type=Path)
        if command == "run":
            sub.add_argument("scenario")
        elif command == "trace":
            sub.add_argument("requirement")
        elif command == "render":
            sub.add_argument("--output", "-o", type=Path)
    args = parser.parse_args(argv)

    try:
        model = load(args.model)
        if args.command == "check":
            diagnostics = validate(model)
            for diagnostic in diagnostics:
                location = f"{args.model}:{diagnostic.line}" if diagnostic.line else str(args.model)
                print(f"{location}: {diagnostic.severity}: {diagnostic.message}")
            errors = sum(item.severity == "error" for item in diagnostics)
            if errors:
                print(f"{errors} error(s)")
                return 1
            print(f"OK: {model.name} ({len(diagnostics)} warning(s))")
            return 0
        if args.command == "run":
            result = run_scenario(model, args.scenario)
            for assertion in result.assertions:
                print(f"{'PASS' if assertion.passed else 'FAIL'} line {assertion.line}: {assertion.expression}")
            for requirement in result.verified_requirements:
                print(f"{'PASS' if result.passed else 'FAIL'} requirement {requirement}")
            return 0 if result.passed else 1
        if args.command == "trace":
            print(json.dumps(trace_requirement(model, args.requirement), indent=2))
            return 0
        output = render_mermaid(model)
        if args.output:
            args.output.write_text(output, encoding="utf-8")
            print(f"Wrote {args.output}")
        else:
            print(output, end="")
        return 0
    except (OSError, ParseError, ModelRuntimeError, KeyError) as exc:
        print(f"error: {exc}")
        return 2

