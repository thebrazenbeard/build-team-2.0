from build_team.models import ALL_FACETS, ANALYSIS_FACETS
from build_team.roster import ROSTER


def test_canonical_names_and_order() -> None:
    assert tuple(ROSTER) == ALL_FACETS
    assert ALL_FACETS == (
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Thirteen",
    )


def test_one_is_only_synthesizer() -> None:
    assert ROSTER["One"].synthesizer is True
    assert all(not ROSTER[name].synthesizer for name in ANALYSIS_FACETS)


def test_thirteen_is_skeptic() -> None:
    assert ROSTER["Thirteen"].lens == "dissent"
    assert "skeptic" in ROSTER["Thirteen"].instruction.lower()


def test_one_is_order_and_efficiency_engine() -> None:
    one = ROSTER["One"]
    assert one.lens == "order, efficiency, and integration"
    assert "organized" in one.temperament
    assert "efficiency-driven" in one.temperament
    assert "complete inventories" in one.instruction
    assert "close loops" in one.instruction
    assert "shortest reliable path" in one.instruction
    assert "duplicated effort" in one.instruction


def test_four_is_creative_genius() -> None:
    four = ROSTER["Four"]
    assert four.lens == "creative invention"
    assert "creative genius" in four.instruction
    assert "wild" in four.instruction.lower()


def test_one_owns_order_and_efficiency() -> None:
    one = ROSTER["One"]
    assert "efficiency" in one.lens
    assert "organized" in one.temperament


def test_one_is_permanent_bt2_coordinator() -> None:
    one = ROSTER["One"]
    assert one.permanent_role == "BT2 Coordinator"
    assert "permanent BT2 Coordinator" in one.instruction
    assert all(ROSTER[name].permanent_role is None for name in ANALYSIS_FACETS)


def test_bt2_is_version_designation() -> None:
    from build_team.models import BT2_MEANING, BT2_NAME, BT2_VERSION

    assert BT2_NAME == "Build Team Two"
    assert BT2_VERSION == 2
    assert "not the second of two" in BT2_MEANING


def test_seven_is_mad_scientist_experimentalist() -> None:
    seven = ROSTER["Seven"]
    assert seven.lens == "experimental science"
    assert "mad scientist" in seven.instruction.lower()
    assert "bounded experiments" in seven.instruction.lower()
    assert "prototype success" in seven.instruction.lower()
