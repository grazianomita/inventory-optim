import pytest

from inventory_optim.data_model.parser import CustomParser


@pytest.fixture
def valid_args():
    return ['--constraints', 'constraints.json', '--data', 'data.csv', '--optim-col', 'opt_col_name', '--var-col', 'var_col_name']


@pytest.fixture
def invalid_args():
    return ['--constraints', 'constraints.json', '--optim-col', 'column_name']  # Missing required argument


def test_parse_args_valid(valid_args, monkeypatch):
    monkeypatch.setattr('sys.argv', ['script_name'] + valid_args)
    parsed_args = CustomParser.parse_args()
    assert parsed_args['constraints'] == 'constraints.json'
    assert parsed_args['data'] == 'data.csv'
    assert parsed_args['optim_col'] == 'opt_col_name'
    assert parsed_args['var_col'] == 'var_col_name'
    assert parsed_args['time_limit'] == 60
    assert parsed_args['optim_obj'] == 'max'  # default value
    assert 'var_incr' in parsed_args
    assert 'var_decr' in parsed_args
    assert 'export_statistics' in parsed_args
    assert 'export_solution' in parsed_args


def test_parse_args_invalid(invalid_args, monkeypatch):
    with pytest.raises(SystemExit):
        monkeypatch.setattr('sys.argv', ['script_name'] + invalid_args)
        CustomParser.parse_args()  # This should raise SystemExit due to missing required argument
