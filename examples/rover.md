# Rover Emergency-Braking Example

The rover model is STELA's first executable vertical slice. It demonstrates how a requirement, system architecture, behavior, and verification scenario form one traceable model.

The source model is [rover.mbse](rover.mbse). It retains the prototype `.mbse` extension until the interpreter and examples complete their migration to the `.stela` convention.

## Engineering question

Can a rover traveling at 2 m/s stop within 2 m when its available deceleration is 1.5 m/s²?

The example represents this as a connected engineering argument:

```text
REQ-001: stopping distance <= 2 m
    ↓ satisfied by
Rover architecture
    ↓ exercised by
emergency_stop action
    ↓ verified by
braking_test scenario
    ↓ produces
stopping distance = 1.33 m → PASS
```

## Complete model

```text
model Rover

requirement safe_braking:
    id: REQ-001
    shall emergency_stop.stopping_distance <= 2 m
    verify_by test

component Controller:
    port motor_command: Command out

component Motor:
    port command: Command in
    port power: Power in

component Battery:
    port power: Power out

component Rover:
    property speed: m/s = 0
    property deceleration: m/s^2 = 1.5
    part controller: Controller
    part motor: Motor
    part battery: Battery
    connect controller.motor_command -> motor.command
    connect battery.power -> motor.power
    satisfies REQ-001

action emergency_stop:
    input speed: m/s
    input deceleration: m/s^2
    output stopping_distance: m
    set stopping_distance = speed * speed / (2 * deceleration)

scenario braking_test:
    set rover.speed = 2 m/s
    perform emergency_stop with speed = rover.speed, deceleration = rover.deceleration
    assert emergency_stop.stopping_distance <= 2 m
    verifies REQ-001
```

## Model declaration

```text
model Rover
```

The file defines one model named `Rover`. The component with the same name serves as the top-level system in this prototype.

## Requirement

```text
requirement safe_braking:
    id: REQ-001
    shall emergency_stop.stopping_distance <= 2 m
    verify_by test
```

The symbolic name is `safe_braking`; the stable engineering identifier is `REQ-001`.

The `shall` expression defines the required outcome. The dot expression:

```text
emergency_stop.stopping_distance
```

selects the `stopping_distance` output produced by the `emergency_stop` action.

`verify_by test` records the intended verification method. In this early example, the executable scenario acts as a model-level test. A flight project would distinguish model analysis, software tests, hardware tests, and final qualification evidence more rigorously.

## Component types and ports

```text
component Controller:
    port motor_command: Command out

component Motor:
    port command: Command in
    port power: Power in

component Battery:
    port power: Power out
```

These declarations define three reusable component types.

- The controller provides commands.
- The motor receives commands and electrical power.
- The battery provides electrical power.

The interface type appears between the colon and direction:

```text
port motor_command: Command out
```

`Command` is the interface type and `out` is the direction.

## Rover composition

```text
component Rover:
    property speed: m/s = 0
    property deceleration: m/s^2 = 1.5
    part controller: Controller
    part motor: Motor
    part battery: Battery
```

The rover has two engineering properties:

- `speed`, measured in meters per second
- `deceleration`, measured in meters per second squared

The `part` declarations install named instances of the component types. For example:

```text
part controller: Controller
```

means that the rover contains an instance named `controller` whose type is `Controller`.

## Connections and the dot operator

```text
connect controller.motor_command -> motor.command
connect battery.power -> motor.power
```

The dot operator selects a member of a particular part:

```text
controller.motor_command
```

means the `motor_command` port belonging to the `controller` instance.

The arrow gives the transfer direction. STELA validates that:

- Each part exists.
- Each selected port exists on its component type.
- The left port has direction `out`.
- The right port has direction `in`.
- Both ports use the same interface type.

Changing `motor.command` from `Command` to `Torque`, for example, produces an incompatible-interface diagnostic.

## Satisfaction claim

```text
satisfies REQ-001
```

This states that the rover design claims to satisfy the braking requirement. It does not prove the claim. Evidence comes from a verification scenario.

## Emergency-stop action

```text
action emergency_stop:
    input speed: m/s
    input deceleration: m/s^2
    output stopping_distance: m
    set stopping_distance = speed * speed / (2 * deceleration)
```

The action accepts speed and deceleration and calculates stopping distance using constant-acceleration kinematics:

```text
d = v² / (2a)
```

For the scenario values:

```text
v = 2.0 m/s
a = 1.5 m/s²
```

the result is:

```text
d = 2² / (2 × 1.5)
  = 4 / 3
  = 1.33 m
```

This simplified equation assumes:

- Constant deceleration
- Level terrain
- No controller or actuator delay
- No wheel slip
- No aerodynamic contribution
- An instantaneous transition to the modeled deceleration

Those assumptions should become explicit model elements as STELA's analysis vocabulary develops.

## Verification scenario

```text
scenario braking_test:
    set rover.speed = 2 m/s
    perform emergency_stop with speed = rover.speed, deceleration = rover.deceleration
    assert emergency_stop.stopping_distance <= 2 m
    verifies REQ-001
```

The scenario proceeds in four steps:

1. Establish the rover speed as 2 m/s.
2. Perform the emergency-stop action using rover properties as inputs.
3. Assert that the calculated stopping distance is no more than 2 m.
4. Link the resulting evidence to `REQ-001`.

The action result is selected using:

```text
emergency_stop.stopping_distance
```

This means the `stopping_distance` output produced by the action performance in the current scenario.

## Running the example

From the repository root, validate the model:

```bash
PYTHONPATH=src python3 -m mbselang check examples/rover.mbse
```

Expected result:

```text
OK: Rover (0 warning(s))
```

Run the braking scenario:

```bash
PYTHONPATH=src python3 -m mbselang run examples/rover.mbse braking_test
```

Expected result:

```text
PASS line 37: emergency_stop.stopping_distance <= 2 m
PASS requirement REQ-001
```

Inspect requirement traceability:

```bash
PYTHONPATH=src python3 -m mbselang trace examples/rover.mbse REQ-001
```

Expected relationship summary:

```text
REQ-001
├── satisfied by Rover
└── verified by braking_test
```

Generate the architecture view:

```bash
PYTHONPATH=src python3 -m mbselang render examples/rover.mbse
```

The resulting Mermaid definition connects the controller and battery to the motor.

## Expected braking profile

Under constant deceleration:

- Velocity decreases linearly from 2.0 m/s to zero.
- Distance increases nonlinearly to 1.33 m.
- Acceleration remains at −1.5 m/s² until the rover stops.
- Stopping time is approximately 1.33 seconds.

The repository includes a static visualization at [braking-profile.png](../visualizations/braking-profile.png).

## Errors the example can expose

The current validator detects several classes of problem:

### Unknown component type

```text
part motor: MissingMotorType
```

### Unknown port

```text
connect controller.missing_port -> motor.command
```

### Incorrect connection direction

```text
connect motor.command -> controller.motor_command
```

### Incompatible interfaces

```text
port motor_command: Command out
port command: Torque in
```

### Scenario unit mismatch

```text
set rover.speed = 2 km
```

### Missing action argument

```text
perform emergency_stop with speed = rover.speed
```

## What this example demonstrates

The rover example establishes the minimum useful STELA workflow:

| Capability | Demonstrated by |
|---|---|
| Requirement definition | `REQ-001` |
| Stable traceability ID | `id: REQ-001` |
| Structural decomposition | Controller, motor, and battery parts |
| Typed interfaces | `Command` and `Power` ports |
| Directed connections | `connect ... -> ...` |
| Typed properties | Speed and deceleration |
| Executable behavior | `emergency_stop` |
| Scenario setup | `set rover.speed = 2 m/s` |
| Verification assertion | Stopping distance ≤ 2 m |
| Satisfaction relationship | Rover satisfies `REQ-001` |
| Verification relationship | `braking_test` verifies `REQ-001` |
| Generated architecture | Mermaid renderer |

## Natural next extensions

A more realistic rover model could add:

- A stakeholder safety need and derived braking objective
- Rover mass and terrain slope
- Tire–surface friction and wheel slip
- Controller and actuator latency
- Battery voltage and motor torque limits
- Nominal, wet-terrain, degraded-brake, and maximum-payload scenarios
- Uncertainty bounds and Monte Carlo analysis
- Explicit assumptions and environmental conditions
- Time-series action execution rather than only closed-form stopping distance
- Hardware test evidence attached to the verification record

The deliberately small example remains useful because each future capability can be added without obscuring the original end-to-end trace.

