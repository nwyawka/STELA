# Exoplanet Water Instrument

This example demonstrates how STELA carries a scientific question through measurement definition, instrument architecture, and evidence.

```text
science document
  -> need
  -> objective
  -> scientific property
  -> observable
  -> measurement requirements
  -> instrument requirements
  -> components
  -> verification and validation scenarios
```

## Status

This is a STELA 0.2 design example. It deliberately uses planned science-traceability prowords that the 0.1 prototype parser does not yet implement. The currently executable example remains `../rover.mbse`.

## Contents

```text
instrument.stela                  Authoritative target-language model
inputs/science-case.md            Synthetic source science document
inputs/target-catalog.csv         Candidate observation targets
inputs/observing-conditions.yaml  Mission and environmental inputs
inputs/instrument-assumptions.yaml Engineering assumptions
inputs/calibration-data.csv       Example calibration observations
expected/science-trace.md         Expected end-to-end trace
expected/requirements.csv         Expected requirements export
expected/architecture.mmd         Expected Mermaid architecture
expected/coverage.json            Expected coverage summary
expected/nominal-observation-results.json Expected scenario result
tests/acceptance.md                Acceptance criteria
```

All input material is synthetic and created for this repository. No external science document is required.

## Intended workflow

When STELA 0.2 support is implemented, this example should run as:

```bash
stela check instrument.stela
stela science-trace instrument.stela --gaps
stela render instrument.stela --view architecture
stela run instrument.stela nominal_transit_observation
stela run instrument.stela detector_noise_test
stela run instrument.stela synthetic_science_retrieval
```

The generated artifacts should semantically match the files in `expected/`.

## Input ownership

| Input | Owner | Role |
|---|---|---|
| `science-case.md` | Exoplanet Science Team | Source of science need and objective |
| `target-catalog.csv` | Observation Planning Team | Target and scenario conditions |
| `observing-conditions.yaml` | Mission Systems Team | Observatory performance conditions |
| `instrument-assumptions.yaml` | Instrument Systems Team | Early design assumptions |
| `calibration-data.csv` | Instrument Test Team | Verification evidence input |

