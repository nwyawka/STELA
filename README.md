# STELA

**STELA — Systems Traceability and Engineering Language for Analysis**

*From intent to evidence.*

STELA is a small, text-first, executable model-based systems engineering language. The initial vertical slice supports requirements, components, typed ports, connections, actions, scenarios, assertions, traceability, and Mermaid architecture views.

The public naming convention is the `stela` command, `.stela` source files, and `stela` Python package. The prototype currently retains its original `mbse` command, `mbselang` package, and `.mbse` example while the implementation migration is pending.

## Try it

No installation is required:

```bash
PYTHONPATH=src python3 -m mbselang check examples/rover/rover.mbse
PYTHONPATH=src python3 -m mbselang run examples/rover/rover.mbse braking_test
PYTHONPATH=src python3 -m mbselang trace examples/rover/rover.mbse REQ-001
PYTHONPATH=src python3 -m mbselang render examples/rover/rover.mbse
```

Run the zero-dependency test suite with:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

For the prototype's local `mbse` command, install the package in editable mode:

```bash
python3 -m pip install -e .
mbse check examples/rover/rover.mbse
```

See [the user manual](docs/user-manual.md), [language charter](docs/language-charter.md), [syntax reference](docs/language-reference.md), and [roadmap](TODO.md).

## Examples

- [Rover braking example](examples/rover/README.md): self-contained executable example with its model, guide, and expected braking visualizations.
- [Exoplanet water instrument](examples/exoplanet-water-instrument/README.md): self-contained STELA 0.2 design example with science-source inputs, datasets, expected traceability, architecture, results, and acceptance criteria.
