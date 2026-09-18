# STELA

## Purpose

Build STELA—the Systems Traceability and Engineering Language for Analysis—a small, text-first, scriptable model-based systems engineering language with a Python implementation and API. The language should cover requirements, system structure, interfaces, behavior, analysis, traceability, and verification without attempting full SysML compatibility.

## Development Principles

- Specify semantics before expanding syntax.
- Keep the core language intentionally small and composable.
- Parse source into a shared semantic intermediate representation used by the CLI, Python API, validators, execution engine, and exporters.
- Prefer deterministic, reproducible execution and explicit simulated time.
- Treat stable element identity, traceability, units, validation, and verification as core capabilities.
- Generate diagrams and reports as views of the model; do not maintain them as independent sources of truth.
- Keep arbitrary Python execution outside the trusted core runtime. Add Python behavior through explicit, documented extension points.
- Preserve source locations so diagnostics can identify the relevant file and construct.

## Repository Conventions

- Use Python with type annotations for the reference implementation.
- Put implementation code under `src/`, tests under `tests/`, examples under `examples/`, and design decisions under `docs/`.
- Add tests for parser behavior, semantic validation, execution behavior, and every fixed defect.
- Prefer small modules with clear boundaries between parsing, semantic analysis, model storage, execution, and presentation.
- Record important architectural choices as short decision records in `docs/decisions/`.
- Do not introduce a dependency without documenting why it is needed.

## Initial Quality Bar

The first vertical slice should parse a small model, validate it, execute one scenario, report an intentionally introduced engineering error, trace a requirement through design and verification, and generate both a machine-readable report and a diagram.
