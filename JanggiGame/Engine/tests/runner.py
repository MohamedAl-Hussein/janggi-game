import unittest
from unittest import TestResult

from integration import test_gameplay
from unit import test_janggi_game
from unit import test_obstacle_detection_strategy
from unit import test_path_generation_strategy


def run_tests(*args, **kwargs) -> TestResult:
    """
    Run test suite for one or more test modules.

    :args: One or more modules to test.
    :keyword verbosity: Test result verbosity, default is 0.
    :return: Test results.
    """

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    for module in list(args):
        suite.addTests(loader.loadTestsFromModule(module))

    runner = unittest.TextTestRunner(verbosity=kwargs.get("verbosity", 0))
    result = runner.run(suite)

    return result


if __name__ == "__main__":
    modules = [
        test_janggi_game,
        test_obstacle_detection_strategy,
        test_path_generation_strategy,
        test_gameplay
    ]

    run_tests(*modules)
