import pytest
import pandas as pd
import json
import os

from inventory_optim.export.exporter import Exporter


@pytest.fixture
def statistics_dict():
    return {
        'iterations': 100,
        'best_solution': 0.95,
        'convergence': True
    }


@pytest.fixture
def tmp_dir(tmpdir):
    return str(tmpdir.mkdir('test_dir'))


def test_export_statistics(statistics_dict, tmp_dir):
    temp_file = os.path.join(tmp_dir, 'statistics.json')
    Exporter.export_statistics(statistics_dict, temp_file)
    assert os.path.isfile(temp_file)
    with open(temp_file, 'r') as f:
        loaded_statistics = json.load(f)
    assert loaded_statistics == statistics_dict


def test_export_solution(tmp_dir):
    temp_file = os.path.join(tmp_dir, 'solution.csv')
    df = pd.DataFrame({'F': [1, 2, 3], 'V': [10, 20, 30]})
    values = [0.1, 0.2, 0.3]
    Exporter.export_solution(temp_file, df, values, optim_col_name='OPT')
    assert os.path.isfile(temp_file)
    loaded_df = pd.read_csv(temp_file)
    assert loaded_df.equals(pd.DataFrame({'F': [1, 2, 3], 'V': [10, 20, 30], 'OPT': [0.1, 0.2, 0.3]}))
