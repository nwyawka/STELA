# Language Charter

## Identity

**STELA — Systems Traceability and Engineering Language for Analysis**

*From intent to evidence.*

The intended command is `stela`, the source-file extension is `.stela`, and the future graphical environment will be called STELA Studio.

## Purpose

STELA helps engineers describe and test small system models using readable, version-controlled text and Python tooling.

## Initial user

The first user is a systems or software engineer who needs lightweight requirements traceability, architecture checks, and executable verification scenarios without adopting a large modeling platform.

## Goals

- Make useful models readable without specialized tooling.
- Connect requirements, structure, behavior, and verification in one model.
- Detect common engineering errors, including incompatible interfaces and units.
- Execute deterministic scenarios without arbitrary source-code execution.
- Offer the same semantic model to the CLI, Python API, future GUI, and exporters.
- Generate views and reports from the model as the source of truth.

## Non-goals for the first release

- SysML conformance or complete SysML import/export.
- General-purpose programming.
- Continuous-time simulation or numerical optimization.
- Arbitrary Python execution inside model files.
- A graphical editor. A GUI is planned after the core semantics stabilize.

## Proving workflow

The rover model must demonstrate measurable requirements, component decomposition, typed interfaces, an executable braking calculation, a verification scenario, requirement traceability, error detection, and an architecture diagram.

## Vertical-slice acceptance criteria

The implementation can:

1. Parse `examples/rover.mbse`.
2. Validate names, connections, port directions, interface types, references, and units.
3. Execute `braking_test` deterministically.
4. Report assertion and requirement pass/fail results.
5. Trace `REQ-001` to a satisfying component and verifying scenario.
6. Render the architecture as Mermaid text.
