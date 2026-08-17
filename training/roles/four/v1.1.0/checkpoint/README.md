# Four checkpoint contracts

These files support recovery and training verification. They do not create currentness, authority, continuity, or side effects.

- `OPERATIONAL_CHECKPOINT.schema.json` defines the portable structure for Four work checkpoints.
- `BASE_READY_RECEIPT.schema.json` defines the portable structure for a qualification receipt.
- `../tools/four_checkpoint.py` is a stdlib-only mechanical validator/template emitter.

The schemas are declarative training source. A chat may inspect and satisfy them without executing code. When Python execution is available, the helper provides a second mechanical check. Passing it proves only that the supplied JSON satisfies these structural and semantic invariants. It does not prove that referenced provider state is current or that any mutation is authorized.
