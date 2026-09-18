# Expected Science Trace

```text
DOC-SCI-001  Water Vapor Observations of Temperate Exoplanets
└── NEED-001  Determine whether atmospheric water is present
    └── OBJ-001  Estimate water-vapor abundance
        └── PROP-001  Atmospheric water abundance
            └── OBS-001  Observe the 2.7 um absorption band
                └── MEAS-001  Water-band measurement
                    ├── MR-001  Cover 2.6 through 2.9 um
                    │   └── INST-001  Spectrometer wavelength range
                    │       └── Spectrometer
                    ├── MR-002  Resolving power >= 1000
                    │   └── INST-002  Instrument resolving power
                    │       └── Spectrometer
                    └── MR-003  Signal-to-noise >= 10
                        ├── INST-003  Detector read noise <= 8 electron
                        │   └── Detector
                        ├── SYS-001   Pointing jitter <= 10 mas
                        └── OPS-001   Observation duration >= 3 h
```

Expected gaps:

- End-of-life detector degradation is not modeled.
- Retrieval false-positive performance is not yet a requirement.
- `synthetic_science_retrieval` requires planned action implementations.

