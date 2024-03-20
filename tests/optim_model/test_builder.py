import pytest
import numpy as np
import pandas as pd

from inventory_optim.data_model.constraints import Constraint
from inventory_optim.optim_model.builder import get_constraint_scope, ModelBuilder


@pytest.fixture
def sample_dataframe():
    data = {
        'QUANTITY': [10, 20, 30],
        'CATEGORY': ["A", "B", "A"],
        'CONTRIB': [11, 10, 10]
    }
    return pd.DataFrame(data)


def test_get_constraint_scope(sample_dataframe):
    category_A_constraint = Constraint(lb=0, ub=10, features=[{'name': 'CATEGORY', 'values': ['A']}])
    assert np.array_equal(get_constraint_scope(sample_dataframe, category_A_constraint), np.array([0, 2]))
    category_B_constraint = Constraint(lb=0, ub=10, features=[{'name': 'CATEGORY', 'values': ['B']}])
    assert np.array_equal(get_constraint_scope(sample_dataframe, category_B_constraint), np.array([1]))
    empty_constraint = Constraint(lb=0, ub=10, features=[])
    assert np.array_equal(get_constraint_scope(sample_dataframe, empty_constraint), np.array([0, 1, 2]))


def test_model_builder(sample_dataframe):
    mb = ModelBuilder()
    mb.create_variables(sample_dataframe, var_incr=1, var_decr=0, var_name='QUANTITY')
    assert mb.highs_.impl_.getNumCol() == len(sample_dataframe)
    constraints = [
        Constraint(lb=0, ub=10, features=[{'name': 'CATEGORY', 'values': ['A']}]),
        Constraint(lb=0, ub=10, features=[{'name': 'CATEGORY', 'values': ['B']}]),
        Constraint(lb=0, ub=10, features=[])
    ]
    mb.build_model(sample_dataframe, constraints, obj_feature_name="CONTRIB", obj='max')
    is_ok, values = mb.solve()
    print(values)
    assert is_ok
    assert sum(values) == 10
    assert values[np.argmax(sample_dataframe['CONTRIB'])] == 10
    assert values == [10, 0, 0]
