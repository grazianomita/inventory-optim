import logging
import pandas as pd
import warnings

from datetime import datetime
from inventory_optim.data_model.parser import CustomParser
from inventory_optim.data_model.constraints import read_constraints_file
from inventory_optim.data_model.checker import Checker
from inventory_optim.optim_model.builder import ModelBuilder
from inventory_optim.export.exporter import Exporter
from inventory_optim.monitoring.logger import create_logger
from inventory_optim.monitoring.time_runner import global_timer, TimeRunner

warnings.filterwarnings("ignore", category=FutureWarning)


def main():
    global_timer.start()
    args = CustomParser.parse_args()
    stats = {
        'date': datetime.now().strftime("%Y%m%dT%H:%M"),
        'args': args
    }
    # Instantiate optimization model
    mb = ModelBuilder(args['time_limit'])
    logger = create_logger(logging.INFO)
    # Define the optimization model and run
    data = TimeRunner.run_and_log(stats, lambda: pd.read_csv(args['data']), [], 'reading_data(s)', 'reading data', logger)
    json_problem = TimeRunner.run_and_log(stats, read_constraints_file, [args['constraints']], 'read_constraint_file(s)', 'reading constraint file', logger)
    TimeRunner.run_and_log(stats, mb.create_variables, [data, args['var_incr'], args['var_decr'], args['var_col']], 'create_variables(s)', 'creating opt variables', logger)
    TimeRunner.run_and_log(stats, mb.build_model, [data, json_problem['constraints'], args['optim_col'], args['optim_obj']], 'build_model(s)', 'building opt model', logger)
    if args['check']:
        TimeRunner.run_and_log(stats, Checker.check_constraints, [data, json_problem['constraints'], args['var_col']], 'check_constraints(s)', 'checking constraints and variable boundaries', logger)
    is_ok, values = TimeRunner.run_and_log(stats, mb.solve, [], 'solving_time(s)', 'solving the opt problem', logger)
    stats['global_time(s)'] = global_timer.get_current_time()
    assert is_ok
    Exporter.export_solution(args['export_solution'], data, values)
    if args['export_statistics']:
        mb.populate_statistics(stats)
        Exporter.export_statistics(stats, args['export_statistics'])


if __name__ == '__main__':
    main()
