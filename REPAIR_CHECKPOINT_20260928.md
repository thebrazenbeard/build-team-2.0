# Build Team 2.0 Repair Checkpoint — 2026-09-28

Canonical base:

`thebrazenbeard/build-team-2.0@05640213e09ab164e3a950cce5a3f3e4adeb6704`

This repository is intentionally a non-canonical predecessor/compatibility
source. The canonical active BT2 engineering/runtime repository is
`thebrazenbeard/bt2`.

The current repository repair boundary is:

- preserve versioned role-training source packages;
- preserve checkpoint schemas/helpers and Protocol V2 regression material;
- keep historical provider bindings as provenance only;
- do not reconstruct the retired Agents-SDK/application shape that is no
  longer present in this repository;
- do not treat legacy training/checkpoint records as current runtime or effect
  authority.

The six immutable role source commits referenced by the training registry were
read back successfully on 2026-09-28.

This checkpoint exists to run the repository's current hosted integrity suite
against the repaired canonical tree. A passing qualification establishes source
integrity for this legacy repository only; it does not establish current BT2
runtime/provider state.
