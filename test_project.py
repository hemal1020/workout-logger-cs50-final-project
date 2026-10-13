import pytest
from project import validate_entry, save_workout, load_workouts, personal_record, weekly_volume, delete_workout, exercise_progress

def test_validate_entry():
    result = validate_entry("  Bench Press ", "3", "8", "60")
    assert result["exercise"] == "bench press"
    assert result["sets"] == 3
    assert result["reps"] == 8
    assert result["weight"] == 60.0
    assert validate_entry("push-up", "3", "15", "0")["weight"] == 0.0

    with pytest.raises(ValueError):
        validate_entry("", "3", "8", "60")

    with pytest.raises(ValueError):
        validate_entry("squat", "abc", "8", "60")    # sets is text

    with pytest.raises(ValueError):
        validate_entry("squat", "3.5", "8", "60")    # sets is not a whole number

    with pytest.raises(ValueError):
        validate_entry("squat", "3", "0", "60")      # reps is zero

    with pytest.raises(ValueError):
        validate_entry("squat", "3", "8", "-5")      # negative weight


def test_save_workout(tmp_path):
    filename = tmp_path / "test.csv"
    entry = validate_entry("squat", "3", "5", "100")
    save_workout(entry, filename)

    lines = filename.read_text().splitlines()
    assert lines[0] == "date,exercise,sets,reps,weight"
    assert "squat,3,5,100.0" in lines[1]


def test_load_workouts(tmp_path):
    filename = tmp_path / "test.csv"
    assert load_workouts(filename) == []

    save_workout(validate_entry("squat", "3", "5", "100"), filename)
    save_workout(validate_entry("bench press", "4", "8", "60"), filename)

    workouts = load_workouts(filename)
    assert len(workouts) == 2
    assert workouts[0]["exercise"] == "squat"
    assert workouts[0]["sets"] == 3
    assert workouts[1]["weight"] == 60.0


def test_personal_record():
    workouts = [
        {"exercise": "squat", "weight": 100.0},
        {"exercise": "squat", "weight": 120.0},
        {"exercise": "bench press", "weight": 60.0},
    ]
    assert personal_record(workouts, "squat") == 120.0
    assert personal_record(workouts, "  Bench Press ") == 60.0
    assert personal_record(workouts, "deadlift") is None
    assert personal_record([], "squat") is None


def test_weekly_volume():
    workouts = [
        {"date": "2026-10-05", "sets": 3, "reps": 5, "weight": 100.0},
        {"date": "2026-10-06", "sets": 4, "reps": 8, "weight": 60.0},
        {"date": "2026-10-13", "sets": 2, "reps": 10, "weight": 50.0},
    ]
    assert weekly_volume(workouts) == {
        "2026-W41": 1500.0 + 1920.0,
        "2026-W42": 1000.0,
    }
    assert weekly_volume([]) == {}


def test_delete_workout(tmp_path):
    filename = tmp_path / "test.csv"
    save_workout(validate_entry("squat", "3", "5", "100"), filename)
    save_workout(validate_entry("bench press", "4", "8", "60"), filename)
    save_workout(validate_entry("deadlift", "1", "5", "120"), filename)

    delete_workout(1, filename)
    remaining = load_workouts(filename)
    assert [w["exercise"] for w in remaining] == ["squat", "deadlift"]

    with pytest.raises(ValueError):
        delete_workout(5, filename)
    with pytest.raises(ValueError):
        delete_workout(-1, filename)

def test_exercise_progress():
    workouts = [
        {"date": "2026-10-06", "exercise": "squat", "weight": 100.0},
        {"date": "2026-10-06", "exercise": "squat", "weight": 110.0},
        {"date": "2026-09-29", "exercise": "squat", "weight": 90.0},
        {"date": "2026-10-01", "exercise": "bench press", "weight": 60.0},
    ]
    assert exercise_progress(workouts, "squat") == [
        ("2026-09-29", 90.0),
        ("2026-10-06", 110.0),
    ]
    assert exercise_progress(workouts, "  Bench Press ") == [("2026-10-01", 60.0)]
    assert exercise_progress(workouts, "deadlift") == []
    assert exercise_progress([], "squat") == []   
