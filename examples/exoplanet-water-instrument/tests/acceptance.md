# Acceptance Criteria

The STELA 0.2 science-traceability implementation is complete enough for this example when it can:

1. Parse `instrument.stela` without errors.
2. Resolve every referenced document, dataset, ID, part, property, and port.
3. Preserve source-document section provenance for the need and measurement requirements.
4. Produce the trace chain from `DOC-SCI-001` through `OBJ-001` and the instrument requirements.
5. Report the three intentionally recorded open gaps.
6. Validate all port directions and interface types.
7. Load and schema-check all four datasets.
8. Execute `nominal_transit_observation` deterministically.
9. Calculate signal-to-noise as 12.0.
10. Verify `MR-001`, `MR-002`, `MR-003`, `SYS-001`, and `OPS-001` in the nominal scenario.
11. Verify `INST-003` using the calibration dataset.
12. Link `synthetic_science_retrieval` to validation of `OBJ-001`.
13. Export science trace, requirements, architecture, coverage, and scenario-result artifacts.

