import json
import pytest

from inventory_optim.data_model.constraints import read_constraints_file


@pytest.fixture
def constraints_json(tmp_path):
    data = {
        "constraints": [
            {"lb": 0, "ub": 10, "features": [
                {"name": "feature1", "values": ["value1"]},
                {"name": "feature2", "values": ["value2"]}
            ]},
            {"lb": 5, "ub": 15, "features": [{"name": "feature3", "values": ["value3"]}]},
            {"lb": 0, "ub": 20, "features": []}
        ]
    }
    file_path = tmp_path / "constraints.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    return str(file_path)


def test_read_constraints_file_valid(constraints_json):
    problem = read_constraints_file(constraints_json)
    assert isinstance(problem, dict)
    assert "constraints" in problem
    assert isinstance(problem["constraints"], list)
    assert len(problem["constraints"]) == 3
    for constraint in problem["constraints"]:
        assert "lb" in constraint
        assert "ub" in constraint
        assert "features" in constraint
        assert isinstance(constraint["lb"], (int, float))
        assert isinstance(constraint["ub"], (int, float))
        assert isinstance(constraint["features"], list)
        for condition in constraint["features"]:
            assert "name" in condition
            assert "values" in condition


def test_read_constraints_file_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    with open(file_path, "w") as f:
        f.write("invalid JSON")
    with pytest.raises(json.JSONDecodeError):
        read_constraints_file(str(file_path))


def test_read_constraints_file_missing_keys(tmp_path):
    data = {"invalid_key": []}
    file_path = tmp_path / "missing_keys.json"
    with open(file_path, "w") as f:
        json.dump(data, f)
    with pytest.raises(KeyError):
        read_constraints_file(str(file_path))
