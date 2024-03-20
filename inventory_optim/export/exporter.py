import pandas as pd
import json
import os

from pathlib import Path


class Exporter:
    @staticmethod
    def export_statistics(statistics: dict, filepath: str) -> None:
        """
        Export solver statistics to csv file.

        :param statistics: dictionary containing the solver statistics
        :param filepath: output filepath
        :return: None
        """
        statistics_json = json.dumps(statistics, sort_keys=True, indent=4)
        file = os.path.dirname(filepath)
        if file != '' and not Path(file).exists():
            Path(file).mkdir(parents=True)
        Path(filepath).write_text(statistics_json)

    @staticmethod
    def export_solution(target_file: str, df: pd.DataFrame, values: list[float], optim_col_name='opt') -> None:
        """
        Export solution to csv file.

        :param target_file: output filepath
        :param df: pandas dataframe containing features and variables to be optimized
        :param values: solution
        :param optim_col_name: name of the column within the pandas dataframe where solution is stored
        :return: None
        """
        assert len(df) == len(values)
        df[optim_col_name] = values
        file = os.path.dirname(target_file)
        if file != '' and not Path(file).exists():
            Path(file).mkdir(parents=True)
        df.to_csv(target_file, index=False)
