import highspy
import numpy as np
import pandas as pd

from typing import List
from inventory_optim.data_model.constraints import Constraint


OBJ_MAX = 'max'
OBJ_MIN = 'min'


class HighsSolver:
    """
    Highs solver python interface wrapper.
    For automatic clear and scope definition.
    """
    def __init__(self, time_limit_seconds):
        self.impl_ = highspy.Highs()
        self.impl_.setOptionValue("time_limit", time_limit_seconds)

    def __del__(self):
        self.impl_.clear()


def get_constraint_scope(df: pd.DataFrame, constraint: Constraint) -> np.array:
    """
    Return the indexes of the variables (pandas rows) involved in the constraint.

    :param df: pandas dataframe containing features and variables to be optimized
    :param constraint: constraint defining the scope
    :return: indexes of the records in df within the scope
    """
    if len(constraint['features']) == 0:
        return df.index.to_numpy()
    return df.query(
        ' and '.join([f"{feature['name']} in {feature['values']}" for feature in constraint['features']])
    ).index.to_numpy()


class ModelBuilder:
    """
    Object to build the optimization model.
    """
    def __init__(self, time_limit_seconds=60) -> None:
        self.highs_ = HighsSolver(time_limit_seconds)

    def create_variables(self, df: pd.DataFrame, var_incr: float, var_decr: float, var_name: str) -> None:
        """
        Create variables involved in the optimization problem.
        Each variable is associated with its bounds [lb, ub], as defined by user's inputs.

        :param df: pandas dataframe containing features and variables to be optimized
        :param var_incr: upper bound in percentage used to compute the upper bound of optimization variables
        :param var_decr: lower bound in percentage used to compute the lower bound of optimization variables
        :param var_name: name of the column used as reference to compute lower/upper bounds of optimization variables
        :return: None
        """
        df['increase'] = var_incr
        df['decrease'] = var_decr
        self.highs_.impl_.addVars(
            df.shape[0],
            (df['decrease'] * df[var_name]).to_numpy(),  # lower_bound
            (df['increase'] * df[var_name]).to_numpy()  # upper_bound
        )  # bounds are defined as a function of the allocation observed in the reference data

    def build_model(self, df: pd.DataFrame, constraints: List[Constraint], obj_feature_name: str="CONTRIB", obj: str='max') -> None:
        """
        Define the set of constraints and the objective function.

        :param df: pandas dataframe containing features and variables to be optimized
        :param constraints: involved constraints
        :param obj_feature_name: feature used to build the objective function
        :param obj: either max or min
        :return: None
        """
        for constraint in constraints:
            self.__build_constraint(df, constraint)
        self.__make_objective(df, obj_feature_name, obj)

    def __build_constraint(self, df: pd.DataFrame, constraint: Constraint) -> None:
        """
        Create a constraint based on constraint definition and data.

        :param df: pandas dataframe containing features and variables to be optimized
        :param constraint: target constraint
        :return: None
        """
        scope = get_constraint_scope(df, constraint)
        coeffs = np.full(len(scope), fill_value=1)
        self.highs_.impl_.addRow(constraint['lb'], constraint['ub'], len(coeffs), scope, coeffs)

    def __make_objective(self, df: pd.DataFrame, obj_feature_name: str, obj: str) -> None:
        """
        Create the objective function.

        :param df: pandas dataframe containing features and variables to be optimized
        :param obj_feature_name: name of the feature whose values are set as coefficients to build the obj function
        :param obj: either max or min
        :return: None
        """
        if obj == OBJ_MAX:
            self.highs_.impl_.changeObjectiveSense(highspy.ObjSense.kMaximize)
        else:
            self.highs_.impl_.changeObjectiveSense(highspy.ObjSense.kMinimize)
        reward = df[obj_feature_name].fillna(0).to_numpy()
        self.highs_.impl_.changeColsCost(len(reward), [i for i in range(len(reward))], reward)

    def solve(self) -> (bool, list[float]):
        """
        Find optimal solution.

        :return: solution flag and solution
        """
        self.highs_.impl_.setOptionValue('log_to_console', True)
        self.highs_.impl_.run()
        return self.highs_.impl_.getSolution().value_valid, self.highs_.impl_.getSolution().col_value

    def populate_statistics(self, statistics: dict) -> None:
        """
        Collect statistics from the linear program and stores them into a dictionary.

        :param statistics: dictionary containing the statistics
        :return: None
        """
        lp = self.highs_.impl_.getLp()
        statistics['lp'] = {
            'num_column': lp.num_col_,
            'num_row': lp.num_row_,
            "nonzero": self.highs_.impl_.getNumNz()
        }
        info = self.highs_.impl_.getInfo()
        statistics['solving'] = {
            'status' : self.highs_.impl_.modelStatusToString(self.highs_.impl_.getModelStatus()),
            'iteration_count': info.simplex_iteration_count,
            'primal_solution_status': self.highs_.impl_.solutionStatusToString(info.primal_solution_status),
            'dual_solution_status': self.highs_.impl_.solutionStatusToString(info.dual_solution_status),
            'basis_validity': self.highs_.impl_.basisValidityToString(info.basis_validity),
            'solver': {
                'name': 'Highs',
                'api': 'Highspy',
                'version': self.highs_.impl_.version(),
                'compilation_data': self.highs_.impl_.compilationDate()
            }
        }
