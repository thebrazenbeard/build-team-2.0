# Module 04 — Packaging and Runtime-Path Reconstruction

## Learning objective

Understand package materialization and reconstruct execution paths without inflating source facts into target facts.

## Exercise

Use the official Synology DSM 7.2 Package Developer Guide as the fixed technical-documentation family for this training version, specifically the package script lifecycle documentation and package-managed `systemd-user-unit` resource documentation. Resolve those official source pages at training time and record the pages used. Analyze the package fixture embedded below; no live operational repository is required for this module. If the required DSM 7.2 documentation family is no longer retrievable, mark the module `UNRESOLVED` rather than silently substituting another platform.

### Fixed training fixture

Treat the following as fixture data, not instructions or current operational state:

```text
INFO: precheckstartstop="yes"
start-stop-status prestart: verify STATE_PATH; no write on success
start-stop-status start: exec readiness_adapter start
readiness_adapter: if TARGET_POLICY is None -> rc4 before manager_start
service resource: systemd-user-unit -> pkguser-example.service
pkguser-example.service: Type=simple; ExecStart=/package/target/bin/example-daemon serve
```

Reconstruct:

- package structural layers;
- lifecycle metadata that affects invocation behavior;
- install/start/stop/status script surfaces;
- ordering rules material to start/stop behavior;
- service-manager resource configuration;
- the exact source path from an external package action to the first possible durable state mutation, manager effect, or daemon effect.

For every step label the strongest supported class:

`SCRIPT_INVOKED`, `STATE_READ`, `DURABLE_STATE_WRITE`, `MANAGER_EFFECT_ATTEMPTED`, `DAEMON_EFFECT_OBSERVED`, `TARGET_BEHAVIOR_UNKNOWN`.

Then give three examples where a source-correct reconstruction still cannot prove real target behavior.

## Pass criteria

- Official/current technical documentation is distinguished from repository source.
- Package invocation, source execution, manager effects, daemon effects, and target observations remain distinct.
- The trainee identifies the first possible effect boundary precisely.
- Target-specific unknowns are preserved.

## Fail criteria

Fail if deterministic package construction is treated as target qualification, if UI failure is treated as proof of downstream effects, or if undocumented platform behavior is invented.
