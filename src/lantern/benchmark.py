from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

from .canonical import canonical_json_bytes, sha256_hex
from .store import ValidationError


def score_benchmark(
    *,
    contract_path: str | Path,
    measurements_path: str | Path,
    freeze_receipt_path: str | Path,
    output_path: str | Path | None = None,
) -> dict[str, Any]:
    contract_bytes = Path(contract_path).read_bytes()
    measurements_bytes = Path(measurements_path).read_bytes()
    freeze_bytes = Path(freeze_receipt_path).read_bytes()
    contract = json.loads(contract_bytes)
    measurements = json.loads(measurements_bytes)
    freeze = json.loads(freeze_bytes)
    if contract.get("schema") != "LANTERN_BENCHMARK_SCORING_CONTRACT_V1":
        raise ValidationError("Unsupported benchmark scoring contract")
    if measurements.get("schema") != "LANTERN_BENCHMARK_MEASUREMENTS_V1":
        raise ValidationError("Unsupported benchmark measurements")
    if freeze.get("schema") != "LANTERN_BENCHMARK_FREEZE_RECEIPT_V1":
        raise ValidationError("Unsupported freeze receipt")
    practice_runs = measurements.get("practice_runs")
    if practice_runs != {"lantern": 1, "control": 1}:
        raise ValidationError("Exactly one untimed practice run per workflow is required")
    lantern = _workflow_metrics(measurements, "lantern")
    control = _workflow_metrics(measurements, "control")
    hard_gate_names = list(contract.get("hard_gates", []))
    hard_gate_results = measurements.get("hard_gate_results", {})
    hard_gates_pass = all(hard_gate_results.get(name) is True for name in hard_gate_names)
    total_time_pass = lantern["total_operator_seconds"] <= control["total_operator_seconds"]
    required_reduction = int(contract.get("required_median_reconstruction_reduction_percent", 30))
    threshold_numerator = control["median_reconstruction_seconds"] * (100 - required_reduction)
    reconstruction_pass = lantern["median_reconstruction_seconds"] * 100 <= threshold_numerator
    passed = hard_gates_pass and total_time_pass and reconstruction_pass
    receipt = {
        "schema": "LANTERN_BENCHMARK_SCORING_RECEIPT_V1",
        "fixture_id": contract.get("fixture_id"),
        "frozen_artifact_set_sha256": freeze.get("artifact_set_sha256"),
        "contract_sha256": sha256_hex(contract_bytes),
        "measurements_sha256": sha256_hex(measurements_bytes),
        "freeze_receipt_sha256": sha256_hex(freeze_bytes),
        "hard_gate_results": {name: bool(hard_gate_results.get(name)) for name in hard_gate_names},
        "lantern": lantern,
        "control": control,
        "required_median_reconstruction_reduction_percent": required_reduction,
        "maximum_lantern_median_reconstruction_seconds_ratio": {
            "numerator": threshold_numerator,
            "denominator": 100,
        },
        "gates": {
            "hard_gates_pass": hard_gates_pass,
            "total_operator_time_no_greater_than_control": total_time_pass,
            "median_reconstruction_reduction_met": reconstruction_pass,
        },
        "result": "PASS" if passed else "FAIL",
    }
    if output_path is not None:
        Path(output_path).write_bytes(canonical_json_bytes(receipt) + b"\n")
    return receipt


def _workflow_metrics(measurements: dict[str, Any], name: str) -> dict[str, Any]:
    workflow = measurements.get(name)
    if not isinstance(workflow, dict):
        raise ValidationError(f"Missing workflow measurements: {name}")
    capture = workflow.get("capture_seconds")
    runs = workflow.get("measured_runs")
    if not isinstance(capture, int) or capture < 0:
        raise ValidationError(f"{name}.capture_seconds must be a non-negative integer")
    if not isinstance(runs, list) or len(runs) != 3:
        raise ValidationError(f"{name} requires exactly three measured runs")
    reconstruction: list[int] = []
    run_total = 0
    for run in runs:
        if not isinstance(run, dict):
            raise ValidationError(f"{name} run must be an object")
        operator = run.get("operator_seconds")
        reconstruct = run.get("reconstruction_seconds")
        if not isinstance(operator, int) or operator < 0:
            raise ValidationError(f"{name} operator_seconds must be a non-negative integer")
        if not isinstance(reconstruct, int) or reconstruct < 0:
            raise ValidationError(f"{name} reconstruction_seconds must be a non-negative integer")
        run_total += operator
        reconstruction.append(reconstruct)
    return {
        "capture_seconds": capture,
        "measured_operator_seconds": run_total,
        "total_operator_seconds": capture + run_total,
        "reconstruction_seconds": reconstruction,
        "median_reconstruction_seconds": statistics.median(reconstruction),
    }
