import pandas as pd

from inventory_optim.data_model.constraints import Constraint
from inventory_optim.optim_model.builder import get_constraint_scope


class Checker:
    @staticmethod
    def check_constraint_validity(df: pd.DataFrame, constraint: Constraint, var_name: str) -> None:
        """
        Check constraint validity by comparing the constraint with the feasible values according to the
        variable boundaries defined by the user.

        :param df: pandas dataframe containing features and variables to be optimized
        :param constraint: constraint to be checked
        :param var_name: name of the column in the pandas dataframe used as optimization variable
        :return: None
        """
        scope = get_constraint_scope(df, constraint)
        max_value = (df.iloc[scope]['increase'] * df.iloc[scope][var_name]).sum()
        min_value = (df.iloc[scope]['decrease'] * df.iloc[scope][var_name]).sum()
        assert float(constraint['ub']) >= min_value, f"variable boundaries incompatible with constraint {constraint}"
        assert float(constraint['lb']) <= max_value, f"variable boundaries incompatible with constraint {constraint}"

    @staticmethod
    def check_constraints(df: pd.DataFrame, constraints: list[Constraint],  var_name: str) -> None:
        """
        Check all the list of constraints.
        Checks are performed according to the check_constraint_validity function.

        :param df: pandas dataframe containing features and variables to be optimized
        :param constraints: list of constraints
        :param var_name: name of the column in the pandas dataframe used as optimization variable
        :return: None
        """
        for constraint in constraints:
            Checker.check_constraint_validity(df, constraint, var_name)
