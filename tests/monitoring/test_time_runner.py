from inventory_optim.monitoring.time_runner import Timer, TimeRunner


def test_timer():
    timer_obj = Timer()
    timer_obj.start()
    elapsed_time = timer_obj.get_current_time()
    assert elapsed_time >= 0  # Check if elapsed time is non-negative


def test_timerunner_measure_elapsed_time():
    stats = {}
    args = [1, 2, 3]
    info_stat = "test_stat"

    def test_function(a, b, c):
        return a + b + c

    result = TimeRunner.measure_elapsed_time(stats, test_function, args, info_stat)
    assert result == sum(args)
    assert info_stat in stats
    assert stats[info_stat] >= 0
