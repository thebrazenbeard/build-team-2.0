from __future__ import annotations

from pathlib import Path

from lantern.benchmark import score_benchmark
from lantern.canonical import canonical_json_bytes

from conftest import ARTIFACT_ROOT


def test_frozen_benchmark_pass_rule_is_executable(tmp_path: Path) -> None:
    measurements = {
        "schema": "LANTERN_BENCHMARK_MEASUREMENTS_V1",
        "practice_runs": {"lantern": 1, "control": 1},
        "hard_gate_results": {
            "zero_unsupported_answers": True,
            "zero_missed_contradiction": True,
            "zero_missed_direct_review_required": True,
            "exact_export_import_reconstruction": True,
            "no_overwrite_on_conflict": True,
        },
        "lantern": {
            "capture_seconds": 20,
            "measured_runs": [
                {"operator_seconds": 10, "reconstruction_seconds": 5},
                {"operator_seconds": 11, "reconstruction_seconds": 6},
                {"operator_seconds": 9, "reconstruction_seconds": 5},
            ],
        },
        "control": {
            "capture_seconds": 25,
            "measured_runs": [
                {"operator_seconds": 12, "reconstruction_seconds": 10},
                {"operator_seconds": 13, "reconstruction_seconds": 9},
                {"operator_seconds": 11, "reconstruction_seconds": 11},
            ],
        },
    }
    measurement_path = tmp_path / "measurements.json"
    measurement_path.write_bytes(canonical_json_bytes(measurements) + b"\n")
    receipt = score_benchmark(
        contract_path=ARTIFACT_ROOT / "scoring-contract-v1.json",
        measurements_path=measurement_path,
        freeze_receipt_path=ARTIFACT_ROOT / "freeze-receipt-v1.json",
    )
    assert receipt["result"] == "PASS"
    assert receipt["gates"] == {
        "hard_gates_pass": True,
        "total_operator_time_no_greater_than_control": True,
        "median_reconstruction_reduction_met": True,
    }
