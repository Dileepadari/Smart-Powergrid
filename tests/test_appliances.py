"""The packed status encoding is the contract with the firmware, so pin it down."""

import pytest

from gridwatch.services.appliances import (
    Appliance,
    apply_control,
    classify,
    decode_health,
    decode_status,
    display_name,
    encode_status,
    overall_health,
    parse_names,
)


def test_parse_names_handles_om2m_list_spelling():
    assert parse_names("['Motor_1', 'LED_1']") == ["Motor_1", "LED_1"]
    assert parse_names("Motor_1,Motor_2") == ["Motor_1", "Motor_2"]
    assert parse_names("") == []
    assert parse_names(None) == []


def test_decode_status_round_trips():
    names = ["Motor_1", "Motor_2", "LED_1", "LED2"]
    raw = "1,2,0:1,0,1:0,1,1:1,1,0"
    triples = decode_status(raw, names)
    assert triples == [(1, 2, 0), (1, 0, 1), (0, 1, 1), (1, 1, 0)]

    appliances = [Appliance(name=n, position=i, power=p, speed=s, direction=d)
                  for i, (n, (p, s, d)) in enumerate(zip(names, triples))]
    assert encode_status(appliances) == raw


def test_decode_status_pads_missing_and_junk_values():
    assert decode_status("1,1,1", ["A", "B"]) == [(1, 1, 1), (0, 0, 0)]
    assert decode_status("x,y,z", ["A"]) == [(0, 0, 0)]
    assert decode_status(None, ["A"]) == [(0, 0, 0)]


def test_decode_health_rejects_out_of_range_scores():
    assert decode_health("3,2,1,9", ["A", "B", "C", "D"]) == [3, 2, 1, None]
    assert decode_health(None, ["A"]) == [None]


@pytest.mark.parametrize(
    "name,kind",
    [("Motor_1", "motor"), ("LED2", "led"), ("Buzzer_1", "buzzer"), ("Kettle", "generic")],
)
def test_classify(name, kind):
    assert classify(name) == kind


def test_display_name_splits_trailing_digits():
    assert display_name("LED2") == "LED 2"
    assert display_name("Motor_1") == "Motor 1"


def test_apply_control_rejects_unsupported_controls():
    buzzer = Appliance(name="Buzzer_1", position=0)
    with pytest.raises(ValueError):
        apply_control(buzzer, "speed", 1)
    with pytest.raises(ValueError):
        apply_control(Appliance(name="Motor_1", position=0), "speed", 7)

    motor = Appliance(name="Motor_1", position=0)
    apply_control(motor, "speed", 2)
    assert motor.speed == 2


def test_overall_health_ignores_unscored_appliances():
    scored = [Appliance(name="A", position=0, health=3), Appliance(name="B", position=1, health=None)]
    assert overall_health(scored) == 100
    assert overall_health([Appliance(name="A", position=0)]) is None
