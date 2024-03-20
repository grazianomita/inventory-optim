import json

from typing import TypedDict, List
from pathlib import Path


class Constraint(TypedDict):
    lb: float
    ub: float
    features: List[dict]


class Problem(TypedDict):
    constraints: List[Constraint]


def read_constraints_file(filepath: str) -> Problem:
    """
    Read file containing the constraints and return a Problem object with the list of constraints.

    :param filepath: path of the file containing the constraints
    :return: Problem instance
    """
    data = json.loads(Path(filepath).read_text())
    constraints = [Constraint(d) for d in data['constraints']]
    return Problem({'constraints': constraints})
