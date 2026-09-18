# STELA User Manual

Version 0.2 design draft

**STELA — Systems Traceability and Engineering Language for Analysis**

*From intent to evidence.*

## 1. Introduction

STELA is a text-first language for describing why a system is needed, what it must accomplish, how it is constructed, how it behaves, and what evidence demonstrates that it works.

The language is designed to preserve one connected engineering story:

```text
source document
    -> stakeholder or science need
    -> objective
    -> property and observable
    -> measurement requirement
    -> instrument and system requirements
    -> components and interfaces
    -> actions and scenarios
    -> verification and validation evidence
```

The same model is intended to support the command-line tools, Python API, generated diagrams, reports, and a future graphical interface.

### 1.1 Implementation status

The current 0.1 interpreter implements:

- `model`
- `requirement`
- `component`
- `property`
- `port`
- `part`
- `connect`
- `satisfies`
- `action`
- `input`
- `output`
- `set`
- `scenario`
- `perform`
- `assert`
- `verifies`
- `verify_by`

This manual also defines the planned science-traceability vocabulary for version 0.2:

- `document`
- `need`
- `objective`
- `observable`
- `measurement`
- `addresses`
- `measures`
- `observes`
- `derives`
- `allocated`
- `validates`
- `source`
- `rationale`
- `assumption`
- `condition`
- `given`
- `status`
- `confidence`

Examples containing planned words describe the target language and will become executable as those features are implemented.

## 2. Files and formatting

A STELA source file conventionally uses the `.stela` extension.

```text
model Example
```

The prototype interpreter accepts any filename and currently includes a legacy `examples/rover.mbse` file. That example will move to `.stela` when the implementation package and CLI are renamed.

### 2.1 Indentation

Members of a declaration are indented using either exactly four spaces or one tab:

```text
requirement example:
    id: REQ-001
    shall value >= 10
    verify_by test
```

The same declaration using tabs is valid. Spaces and tabs may not be mixed on the same line.

### 2.2 Comments

A `#` begins a comment:

```text
# Detector operating point at beginning of life.
property operating_temperature: K = 42
```

### 2.3 Names

Symbolic names begin with a letter or underscore and may contain letters, digits, and underscores:

```text
detector
water_band_measurement
REQ_001
```

Human-readable text belongs in quoted statements and descriptions rather than symbolic names.

### 2.4 Identifiers and names

A name identifies an element within the model:

```text
requirement spectral_resolution:
```

An `id` is its stable engineering identifier:

```text
    id: INST-002
```

Renaming `spectral_resolution` should not change `INST-002`. Reports and external traceability should use the stable ID.

## 3. The dot operator

The dot (`.`) is the qualification or member-access operator. It identifies something contained by, produced by, or belonging to another named element.

```text
telescope.photon_output
```

This means:

1. Find the part named `telescope` in the current scope.
2. Determine that its component type is `Telescope`.
3. Find `photon_output` on that component.

Given:

```text
component Telescope:
    port photon_output: PhotonStream out

component Instrument:
    part telescope: Telescope
```

the expression `telescope.photon_output` references the output port on the `telescope` instance, not every possible `Telescope`.

### 3.1 Properties

```text
spectrometer.resolving_power
detector.operating_temperature
observatory.pointing_jitter
```

Each expression selects a property from a particular part or system instance.

### 3.2 Ports

```text
connect telescope.photon_output -> spectrometer.photon_input
```

The connection runs from the `photon_output` port of the `telescope` part to the `photon_input` port of the `spectrometer` part.

The validator checks that:

- `telescope` and `spectrometer` exist in the current component.
- Both named ports exist on their component types.
- The source port is `out`.
- The target port is `in`.
- Their interface types are compatible.

### 3.3 Action results

```text
emergency_stop.stopping_distance
```

This selects the `stopping_distance` output produced by the most recent performance of `emergency_stop` in the scenario.

### 3.4 Longer paths

The target language will allow longer qualified paths:

```text
observatory.instrument.detector.operating_temperature
```

Resolution proceeds from left to right:

```text
observatory
    .instrument
        .detector
            .operating_temperature
```

Every segment must exist and be visible in the current scope. The dot operator does not execute Python and does not provide access to arbitrary Python attributes.

### 3.5 Type names versus instance names

Uppercase names conventionally identify component types:

```text
component Spectrometer:
```

Lowercase names conventionally identify instances:

```text
part spectrometer: Spectrometer
```

`Spectrometer.resolving_power` describes a member of the type when type-level references are permitted. `spectrometer.resolving_power` selects the value on a particular installed part.

## 4. Core declarations

### 4.1 `model`

`model` names the model contained in the file.

```text
model ExoplanetWaterInstrument
```

A file contains one model declaration. All other top-level declarations belong to that model.

### 4.2 `document` (planned)

`document` records a source artifact from which needs, objectives, assumptions, or requirements were obtained.

```text
document science_case:
    id: DOC-SCI-001
    title: "Water vapor observations of exoplanet atmospheres"
    file: "science/exoplanet-science-case.pdf"
    version: "Draft 3"
    owner: "Science Team"
```

A document is evidence and provenance. Its prose is not automatically treated as an approved requirement.

### 4.3 `need` (planned)

`need` records what a stakeholder wants to learn, achieve, prevent, or enable.

```text
need characterize_water:
    id: NEED-001
    statement: "Determine whether water vapor is present in nearby temperate exoplanet atmospheres."
    source: DOC-SCI-001 page 14
    stakeholder: "Exoplanet Science Team"
    priority: primary
```

A need:

- May be qualitative.
- Does not use `shall`.
- May need clarification.
- Does not, by itself, impose a verified engineering commitment.

### 4.4 `objective` (planned)

`objective` states a specific outcome that addresses a need.

```text
objective measure_water_abundance:
    id: OBJ-001
    statement: "Estimate atmospheric water-vapor abundance for selected temperate exoplanets."
    addresses NEED-001
    success: "Constrain abundance to within one order of magnitude."
```

An objective should describe an observable or assessable outcome. Multiple objectives may address one need, and one objective may address multiple needs.

### 4.5 Scientific `property` (planned context)

At the science level, a property is the physical, chemical, or biological characteristic the investigation wants to determine.

```text
property atmospheric_water_abundance:
    id: PROP-001
    quantity: volume_mixing_ratio
    subject: exoplanet_atmosphere
```

Inside a component, `property` instead declares a typed engineering value:

```text
component Detector:
    property read_noise: electron = 6
    property operating_temperature: K = 42
```

The containing scope tells the parser which form is intended.

### 4.6 `observable` (planned)

`observable` describes what can actually be detected or calculated from acquired data.

```text
observable water_absorption_band:
    id: OBS-001
    measures PROP-001
    phenomenon: spectral_absorption
    wavelength: 2.7 um
    method: transmission_spectroscopy
```

The distinction is important: atmospheric abundance is a desired scientific property, while spectral absorption is the observable used to infer it.

### 4.7 `measurement` (planned)

`measurement` groups requirements associated with measuring an observable.

```text
measurement water_band_measurement:
    id: MEAS-001
    derives OBJ-001
    observes OBS-001
```

Measurement requirements normally specify some combination of range, accuracy, precision, uncertainty, spatial resolution, spectral resolution, cadence, coverage, and confidence.

### 4.8 `requirement`

`requirement` records an objective, testable commitment.

```text
requirement detector_noise:
    id: INST-003
    shall detector.read_noise <= 8 electron
    condition: "at operating_temperature <= 45 K"
    rationale: "Needed to achieve measurement signal-to-noise."
    derives MR-003
    verify_by test
```

The minimal currently executable form is:

```text
requirement safe_braking:
    id: REQ-001
    shall emergency_stop.stopping_distance <= 2 m
    verify_by test
```

### Requirement fields

- `id:` supplies the stable identifier.
- `shall` defines the condition that must be true.
- `verify_by` defines the planned verification method.
- `condition:` defines the state or environment in which the requirement applies.
- `rationale:` explains why the threshold or behavior is necessary.
- `assumption:` records a premise on which the requirement depends.
- `source:` identifies its documentary origin.
- `derives` identifies an upstream need, objective, measurement, or requirement.

## 5. System structure

### 5.1 `component`

`component` defines a reusable kind of system element.

```text
component Spectrometer:
    property wavelength_min: um = 2.5
    property wavelength_max: um = 3.0
    property resolving_power: 1 = 1200
    port photon_input: PhotonStream in
    port spectral_output: SpectralPhotonStream out
    satisfies INST-001
    satisfies INST-002
```

### 5.2 Component `property`

A component property has a name, unit, and initial or design value:

```text
property resolving_power: 1 = 1200
```

The unit `1` represents a dimensionless value.

```text
property operating_temperature: K = 42
property read_noise: electron = 6
property mass: kg = 18.5
```

### 5.3 `port`

A port is a typed interaction point:

```text
port photon_input: PhotonStream in
port spectral_output: SpectralPhotonStream out
```

The last word gives its direction:

- `in` receives the interface type.
- `out` provides the interface type.

Interface types such as `PhotonStream` describe what crosses the boundary. Future versions may define their fields explicitly.

### 5.4 `part`

`part` installs an instance of a component type inside another component:

```text
component Instrument:
    part telescope: Telescope
    part spectrometer: Spectrometer
    part detector: Detector
```

Here, `Telescope` is the reusable type and `telescope` is the particular instance inside `Instrument`.

### 5.5 `connect`

`connect` establishes a directed connection between ports:

```text
connect telescope.photon_output -> spectrometer.photon_input
connect spectrometer.spectral_output -> detector.photon_input
connect detector.samples -> electronics.sample_input
```

The arrow points in the direction of transfer.

## 6. Behavior

### 6.1 `action`

`action` defines executable behavior with typed inputs and outputs:

```text
action calculate_signal_to_noise:
    input signal_electrons: electron
    input noise_electrons: electron
    output signal_to_noise: 1
    set signal_to_noise = signal_electrons / noise_electrons
```

### 6.2 `input`

`input` declares a value required by an action:

```text
input noise_electrons: electron
```

Every input must be supplied when the action is performed.

### 6.3 `output`

`output` declares a value produced by an action:

```text
output signal_to_noise: 1
```

Every output must be assigned before the action completes.

### 6.4 `set`

In an action, `set` assigns an output:

```text
set signal_to_noise = signal_electrons / noise_electrons
```

In a scenario, `set` establishes a value in the modeled system:

```text
set detector.operating_temperature = 42 K
```

The current expression engine supports numeric literals, names, dotted names, parentheses, addition, subtraction, multiplication, division, and comparisons. It does not execute arbitrary Python.

## 7. Scenarios

### 7.1 `scenario`

A scenario describes a particular operational, analytical, test, environmental, or failure case.

```text
scenario nominal_transit_observation:
    given target.star_magnitude = 8.5
    given target.transit_duration = 3 h
    set detector.operating_temperature = 42 K
    perform observe_transit
    assert spectrum.signal_to_noise >= 10
    verifies MR-003
    validates OBJ-001
```

Useful scenario families include:

- Nominal science observations
- Limiting or worst-case observations
- Calibration
- Environmental qualification
- Integration and acceptance testing
- Degraded and failure behavior
- End-of-life performance

### 7.2 `given` (planned)

`given` declares a scenario condition supplied by the target, environment, mission, or test configuration:

```text
given target.star_magnitude = 8.5
given observatory.pointing_jitter = 8 mas
```

`given` differs from `set` in intent: `given` is an assumed scenario condition, while `set` changes a modeled value as part of setup or execution.

### 7.3 `perform`

`perform` executes an action:

```text
perform calculate_signal_to_noise with signal_electrons = 1200, noise_electrons = 100
```

The action output can then be referenced using the dot operator:

```text
assert calculate_signal_to_noise.signal_to_noise >= 10
```

The planned action vocabulary will also allow ordered action performance without explicit input arguments when flows or bindings already supply them:

```text
perform acquire_target
perform calibrate_detector
perform observe_transit
perform process_spectrum
```

### 7.4 `assert`

`assert` defines a condition that must be true during scenario execution:

```text
assert spectrum.signal_to_noise >= 10
assert detector.operating_temperature <= 45 K
```

An assertion produces pass/fail evidence. It does not by itself establish which requirement is verified; use `verifies` for that trace.

## 8. Traceability relationships

Traceability relationships are directional statements. The word appears on the element that makes the relationship.

### 8.1 `addresses` (planned)

An objective addresses a stakeholder or science need:

```text
objective measure_water_abundance:
    addresses NEED-001
```

### 8.2 `measures` (planned)

An observable measures or supports inference of a scientific property:

```text
observable water_absorption_band:
    measures PROP-001
```

### 8.3 `observes` (planned)

A measurement definition observes a particular observable:

```text
measurement water_band_measurement:
    observes OBS-001
```

### 8.4 `derives` (planned)

`derives` identifies the upstream element that caused a downstream requirement or measurement to exist:

```text
requirement detector_noise:
    derives MR-003
```

Derivation is not decomposition by containment. It records engineering rationale and flowdown.

### 8.5 `allocated` (planned)

`allocated` assigns responsibility to an element:

```text
component Detector:
    allocated INST-003
```

Allocation does not claim that the design meets the requirement. It says the component owns all or part of the responsibility.

### 8.6 `satisfies`

`satisfies` records a design claim:

```text
component Detector:
    satisfies INST-003
```

It means the detector design claims to fulfill the requirement. This is not verification evidence.

### 8.7 `verifies`

`verifies` links a scenario or verification case to a requirement:

```text
scenario detector_noise_test:
    assert measured.read_noise <= 8 electron
    verifies INST-003
```

Verification asks whether the implementation conforms to its requirement.

### 8.8 `validates` (planned)

`validates` links a scenario to a need or objective:

```text
scenario synthetic_science_retrieval:
    validates OBJ-001
```

Validation asks whether the complete system can achieve the intended scientific or stakeholder outcome.

## 9. Verification methods

`verify_by` accepts these methods:

### `test`

Measure the implemented item or a representative article under controlled conditions.

```text
verify_by test
```

### `analysis`

Use calculations, models, simulation, or accumulated test data.

```text
verify_by analysis
```

### `inspection`

Examine the item, its construction, records, or configuration.

```text
verify_by inspection
```

### `demonstration`

Operate the item and observe successful behavior without necessarily collecting the detailed quantitative data of a test.

```text
verify_by demonstration
```

## 10. Supporting prowords

The following planned words add context and governance.

### `source:`

Records where an element originated:

```text
source: DOC-SCI-001 page 14
```

### `rationale:`

Explains why an element or threshold exists:

```text
rationale: "A signal-to-noise ratio of 10 separates the water and no-water hypotheses."
```

### `assumption:`

Records a premise that has not necessarily been guaranteed:

```text
assumption: "Target star magnitude <= 9"
```

Assumptions should be queryable because invalid assumptions can invalidate derived requirements and analyses.

### `condition:`

Defines when or where a requirement applies:

```text
condition: "at operating_temperature <= 45 K"
```

### `status:`

Records lifecycle state:

```text
status: draft
status: review
status: approved
status: retired
```

### `confidence:`

Records extraction or analytical confidence, especially for machine-generated candidates:

```text
confidence: 0.91
```

Confidence does not replace approval.

### `candidate` (planned)

Marks an imported or machine-suggested element that has not been accepted into the authoritative model:

```text
candidate need candidate_001:
    statement: "Characterize atmospheric water."
    source: DOC-SCI-001 page 14
    confidence: 0.91
    status: review
```

### Metadata field reference

The science extensions use these descriptive fields. They are prowords within the applicable declaration, not independent top-level elements.

| Field | Meaning |
|---|---|
| `id:` | Stable identifier used for traceability |
| `title:` | Human-readable document or artifact title |
| `file:` | Path or external location of a source artifact |
| `version:` | Version of the source or modeled item |
| `owner:` | Person, team, or organization responsible for the item |
| `statement:` | Human-readable wording of a need or objective |
| `stakeholder:` | Person or group whose need is represented |
| `priority:` | Relative importance such as `primary`, `secondary`, or `desirable` |
| `success:` | Criterion for determining whether an objective was achieved |
| `quantity:` | Kind of scientific or engineering quantity represented |
| `subject:` | Entity or phenomenon possessing a scientific property |
| `phenomenon:` | Detectable physical, chemical, or biological effect |
| `wavelength:` | Wavelength associated with an observable |
| `method:` | Scientific or measurement technique |

### Direction and literal prowords

- `in` declares a receiving port or action input.
- `out` declares a providing port or action output.
- `true` and `false` are Boolean values used by assertions and expressions.
- `primary`, `secondary`, `desirable`, `draft`, `review`, `approved`, and `retired` are conventional enumeration values rather than universal reserved words.

## 11. Worked example: exoplanet water instrument

The following target-language example shows the complete flow. Science-traceability constructs are planned for version 0.2; the component, action, connection, and core scenario forms establish how they integrate with the current language.

```text
model ExoplanetWaterInstrument

document science_case:
    id: DOC-SCI-001
    title: "Water vapor observations of exoplanet atmospheres"
    file: "science/exoplanet-science-case.pdf"
    version: "Draft 3"
    owner: "Science Team"

need characterize_water:
    id: NEED-001
    statement: "Determine whether water vapor is present in nearby temperate exoplanet atmospheres."
    source: DOC-SCI-001 page 14
    stakeholder: "Exoplanet Science Team"
    priority: primary
    status: approved

objective measure_water_abundance:
    id: OBJ-001
    statement: "Estimate atmospheric water-vapor abundance for selected temperate exoplanets."
    addresses NEED-001
    success: "Constrain abundance to within one order of magnitude."

property atmospheric_water_abundance:
    id: PROP-001
    quantity: volume_mixing_ratio
    subject: exoplanet_atmosphere

observable water_absorption_band:
    id: OBS-001
    measures PROP-001
    phenomenon: spectral_absorption
    wavelength: 2.7 um
    method: transmission_spectroscopy

measurement water_band_measurement:
    id: MEAS-001
    derives OBJ-001
    observes OBS-001

requirement wavelength_coverage:
    id: MR-001
    shall spectrum.wavelength_min <= 2.6 um
    shall spectrum.wavelength_max >= 2.9 um
    derives MEAS-001
    rationale: "The water absorption feature spans this wavelength interval."
    verify_by analysis

requirement spectral_resolution:
    id: MR-002
    shall spectrum.resolving_power >= 1000
    derives MEAS-001
    rationale: "Required to distinguish the water feature from adjacent spectral structure."
    verify_by analysis

requirement signal_to_noise:
    id: MR-003
    shall spectrum.signal_to_noise >= 10
    condition: "per spectral resolution element"
    assumption: "Target star magnitude <= 9"
    derives MEAS-001
    verify_by analysis

requirement detector_wavelength_range:
    id: INST-001
    shall spectrometer.wavelength_min <= 2.6 um
    shall spectrometer.wavelength_max >= 2.9 um
    derives MR-001
    verify_by test

requirement instrument_resolving_power:
    id: INST-002
    shall spectrometer.resolving_power >= 1000
    condition: "across 2.6..2.9 um"
    derives MR-002
    verify_by test

requirement detector_noise:
    id: INST-003
    shall detector.read_noise <= 8 electron
    condition: "at detector.operating_temperature <= 45 K"
    derives MR-003
    verify_by test

component Telescope:
    port photon_output: PhotonStream out

component Spectrometer:
    property wavelength_min: um = 2.5
    property wavelength_max: um = 3.0
    property resolving_power: 1 = 1200
    port photon_input: PhotonStream in
    port spectral_output: SpectralPhotonStream out
    allocated INST-001
    allocated INST-002
    satisfies INST-001
    satisfies INST-002

component Detector:
    property read_noise: electron = 6
    property operating_temperature: K = 42
    port photon_input: SpectralPhotonStream in
    port samples: DetectorSamples out
    allocated INST-003
    satisfies INST-003

component Electronics:
    port sample_input: DetectorSamples in
    port science_data: ScienceData out

component ThermalControl:
    property detector_setpoint: K = 42

component CalibrationSource:
    port calibration_photons: PhotonStream out

component Instrument:
    part telescope: Telescope
    part spectrometer: Spectrometer
    part detector: Detector
    part electronics: Electronics
    part thermal_control: ThermalControl
    part calibration_source: CalibrationSource

    connect telescope.photon_output -> spectrometer.photon_input
    connect spectrometer.spectral_output -> detector.photon_input
    connect detector.samples -> electronics.sample_input

    allocated MR-001
    allocated MR-002
    allocated MR-003

action calculate_signal_to_noise:
    input signal_electrons: electron
    input noise_electrons: electron
    output signal_to_noise: 1
    set signal_to_noise = signal_electrons / noise_electrons

scenario nominal_transit_observation:
    given target.star_magnitude = 8.5
    given target.transit_duration = 3 h
    given observatory.pointing_jitter = 8 mas
    set detector.operating_temperature = 42 K

    perform acquire_target
    perform calibrate_detector
    perform observe_transit
    perform process_spectrum
    perform estimate_water_abundance

    assert spectrum.signal_to_noise >= 10
    assert spectrum.wavelength_min <= 2.6 um
    assert spectrum.wavelength_max >= 2.9 um
    assert spectrum.resolving_power >= 1000

    verifies MR-001
    verifies MR-002
    verifies MR-003
    validates OBJ-001

scenario detector_noise_test:
    given chamber.temperature = 42 K
    perform measure_read_noise
    assert measured.read_noise <= 8 electron
    verifies INST-003

scenario synthetic_science_retrieval:
    given synthetic_atmosphere.water_abundance = 0.001
    perform simulate_observation
    perform process_spectrum
    perform estimate_water_abundance
    assert retrieval.water_detected == true
    validates OBJ-001
```

## 12. Reading the worked example

The trace begins with a qualitative statement:

```text
NEED-001: Determine whether water vapor is present.
```

`OBJ-001` converts it into a scientific outcome. `PROP-001` identifies the desired physical property. `OBS-001` identifies the measurable spectral phenomenon. `MEAS-001` groups the measurement definition.

The measurement requirements then quantify necessary performance:

```text
MR-001  Wavelength coverage
MR-002  Spectral resolving power
MR-003  Signal-to-noise ratio
```

Those requirements derive implementable instrument requirements:

```text
MR-001 -> INST-001 -> Spectrometer
MR-002 -> INST-002 -> Spectrometer
MR-003 -> INST-003 -> Detector
```

The architecture connects the photon and data paths:

```text
telescope.photon_output
    -> spectrometer.photon_input

spectrometer.spectral_output
    -> detector.photon_input

detector.samples
    -> electronics.sample_input
```

Finally, engineering scenarios verify requirements while a science-retrieval scenario validates the science objective.

## 13. Trace and coverage queries

Currently implemented:

```bash
PYTHONPATH=src python3 -m mbselang check examples/rover.mbse
PYTHONPATH=src python3 -m mbselang run examples/rover.mbse braking_test
PYTHONPATH=src python3 -m mbselang trace examples/rover.mbse REQ-001
PYTHONPATH=src python3 -m mbselang render examples/rover.mbse
```

Planned STELA science and requirement queries:

```bash
stela requirements instrument.stela
stela requirements instrument.stela Detector
stela requirements instrument.stela Instrument --recursive
stela requirements instrument.stela --unallocated
stela requirements instrument.stela --unsatisfied
stela requirements instrument.stela --unverified
stela science-trace instrument.stela
stela science-trace instrument.stela NEED-001 --tree
stela science-trace instrument.stela --gaps
```

Expected trace-tree form:

```text
NEED-001  Determine whether atmospheric water is present
└── OBJ-001  Estimate water-vapor abundance
    └── OBS-001  Measure the 2.7 um absorption band
        ├── MR-001  Cover 2.6–2.9 um
        │   └── INST-001  Spectrometer wavelength range
        ├── MR-002  Resolving power >= 1000
        │   └── INST-002  Spectrometer resolving power
        └── MR-003  Signal-to-noise >= 10
            └── INST-003  Detector read noise
```

Expected gap reporting:

```text
GAP  OBJ-002 has no observable
GAP  MR-006 has no derived instrument requirement
GAP  INST-009 is not allocated to a component
GAP  INST-011 has no verification scenario
GAP  NEED-003 has no validation scenario
```

## 14. Document ingestion workflow (planned)

A future document-ingestion command will create reviewable candidates rather than silently approving requirements:

```bash
stela ingest science-case.pdf --as science-draft
```

The intended workflow is:

1. Register the source document and version.
2. Extract candidate needs, objectives, assumptions, quantities, and constraints.
3. Preserve page-level provenance.
4. Have scientists accept, reject, merge, or revise candidate needs.
5. Define objectives and observables collaboratively.
6. Negotiate quantitative measurement requirements.
7. Derive instrument and mission requirements.
8. Allocate requirements to components and operations.
9. Construct verification and science-validation scenarios.
10. Generate the Science Traceability Matrix and identify gaps.

Machine assistance may propose elements and relationships. Approval remains an accountable human decision.

## 15. Keyword summary

| Proword | Purpose | Status |
|---|---|---|
| `model` | Name the model | Implemented |
| `document` | Register a source artifact | Planned |
| `need` | Record a qualitative stakeholder or science need | Planned |
| `objective` | Define an outcome addressing a need | Planned |
| `property` | Define a scientific property or component value | Partial |
| `observable` | Define a measurable phenomenon | Planned |
| `measurement` | Group a measurement definition | Planned |
| `requirement` | Define a testable commitment | Implemented |
| `component` | Define a reusable system element type | Implemented |
| `part` | Instantiate a component inside another | Implemented |
| `port` | Define a typed directional interaction point | Implemented |
| `connect` | Connect a source port to a destination port | Implemented |
| `action` | Define executable behavior | Implemented |
| `input` | Declare an action input | Implemented |
| `output` | Declare an action output | Implemented |
| `set` | Assign an action output or scenario value | Implemented |
| `scenario` | Define an operational, analytical, or test case | Implemented |
| `given` | Declare a scenario condition | Planned |
| `perform` | Execute an action | Implemented |
| `assert` | Evaluate a pass/fail condition | Implemented |
| `addresses` | Link an objective to a need | Planned |
| `measures` | Link an observable to a scientific property | Planned |
| `observes` | Link a measurement to an observable | Planned |
| `derives` | Link a downstream element to its source | Planned |
| `allocated` | Assign responsibility for a requirement | Planned |
| `satisfies` | Record a design satisfaction claim | Implemented |
| `verifies` | Link verification evidence to a requirement | Implemented |
| `validates` | Link evidence to a need or objective | Planned |
| `verify_by` | Select the planned verification method | Implemented |
| `source:` | Record provenance | Planned |
| `rationale:` | Explain why an element exists | Planned |
| `assumption:` | Record a premise | Planned |
| `condition:` | Define applicability conditions | Planned |
| `status:` | Record lifecycle state | Planned |
| `confidence:` | Record extraction or analytical confidence | Planned |
| `candidate` | Mark an unapproved proposed element | Planned |

## 16. Recommended modeling practice

- Preserve the scientist's original language in `need` and `objective` statements.
- Introduce `shall` only when a measurable commitment has been negotiated.
- Keep scientific properties distinct from instrument observables.
- Give every authoritative element a stable ID.
- Record sources, rationale, assumptions, and conditions close to the affected element.
- Use `allocated` for responsibility, `satisfies` for design claims, `verifies` for requirement evidence, and `validates` for stakeholder or science outcomes.
- Build nominal, limiting, calibration, degraded, and end-of-life scenarios.
- Generate diagrams and traceability matrices from the model rather than maintaining separate copies.
- Treat automatically extracted content as a candidate until a responsible person approves it.
