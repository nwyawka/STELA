# Roadmap

## Next

- Add source spans and richer diagnostic suggestions.
- Add stable explicit identifiers to every model element.
- Add structured types, enumerations, ranges, and unit conversions.
- Add action sequencing, branching, loops, events, and concurrency.
- Add state machines with triggers, guards, effects, and simulated time.
- Add imports, packages, namespaces, and a standard library.
- Add JSON reports and semantic model serialization.
- Add requirement coverage and verification matrices.
- Add semantic model diffing and migrations.
- Add a language server, formatter, and editor integration.

## Consolidated project storage

- Define a `stela.toml` workspace manifest that identifies model modules, source artifacts, generated outputs, and the semantic database.
- Support a small number of concern-oriented model modules such as `science.stela`, `requirements.stela`, `architecture.stela`, `behavior.stela`, and `verification.stela`.
- Compile all model modules into a unified semantic graph so queries do not depend on physical file organization.
- Add a generated SQLite project database at `.stela/model.db` for elements, relationships, properties, source references, candidate statements, review decisions, assumptions, model versions, scenario runs, verification results, and evidence.
- Establish authority rules: `.stela` files own authored model definitions; registered documents and datasets own source inputs; the database owns workflow history and execution evidence; reports and diagrams are generated views.
- Add content-addressed artifact storage under `.stela/objects/` for PDFs, images, large datasets, simulation outputs, calibration products, and other evidence.
- Store artifact checksums, media types, versions, roles, sizes, and provenance in the semantic database rather than duplicating large files.
- Make science-document intake write candidates and review decisions into the project database instead of producing many small text files.
- Add consolidated commands such as `stela show`, `stela trace`, `stela requirements`, `stela assumptions`, `stela gaps`, `stela evidence`, and `stela history`.
- Treat the SQLite database as a rebuildable semantic index rather than the sole representation of human-authored model content, preserving useful Git diffs and merges.
- Define a portable, ZIP-compatible `.stelapkg` exchange format containing the manifest, model sources, semantic database, registered artifacts, evidence, and optional generated reports.
- Add `stela pack` and `stela unpack` commands with integrity and checksum verification.
- Ensure stable element IDs survive file reorganization, module splitting, and renaming.

## GUI

- Build **STELA Studio**, a GUI for model navigation, editing, architecture visualization, traceability, scenario execution, and verification results.
- Keep the GUI as a client of the same semantic model and services used by the CLI and Python API.

## Later interoperability

- CSV and requirements-tool interchange.
- SysML v2 mapping and interchange investigation.
- FMI/FMU and OpenMDAO analysis adapters.
