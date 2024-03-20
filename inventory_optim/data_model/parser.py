import argparse

from inventory_optim.optim_model.builder import OBJ_MIN, OBJ_MAX


class CustomParser:
    @staticmethod
    def parse_args() -> dict:
        """
        Parse input args.

        :return: dict of input args
        """
        parser = argparse.ArgumentParser(description='Vessel profile ')
        # Input data
        inputs = parser.add_argument_group('Input data')
        inputs.add_argument('--constraints', help='<Required> Path to json constraints file', required=True)
        inputs.add_argument('--data', help='<Required> Path to csv containing all the data', required=True)
        inputs.add_argument('--var-col', help='<Required> Name of the column in data used as optimization variable', required=True)
        inputs.add_argument('--optim-col', help='<Required> Name of the column in data used as optimization objective', required=True)
        inputs.add_argument('--optim-obj', help='Optimization objective', choices=[OBJ_MIN, OBJ_MAX], default=OBJ_MAX)
        # Options
        options = parser.add_argument_group('Options')
        options.add_argument('--time-limit', help='Time limit in seconds', required=False, type=int, default=60)
        options.add_argument('--var-incr', help='Perc of allowed var increase', required=False, type=float, default=1.5)
        options.add_argument('--var-decr', help='Perc of allowed var decrease', required=False, type=float, default=.8)
        # Output
        output = parser.add_argument_group('Output')
        output.add_argument('--export-statistics', help='File to export statistics', default="data/res_stats.json")
        output.add_argument('--export-solution', help='File to export solution', default="data/res_solution.csv")
        # Miscellaneous
        miscellaneous = parser.add_argument_group('Miscellaneous')
        miscellaneous.add_argument('--check', help='Flag to check constraints', action='store_true', default=True)
        return vars(parser.parse_args())
