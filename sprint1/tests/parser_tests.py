"""
Test suite for the python compiler.
"""


def run_tests() -> None:
    """
    Runs all tests in this file if run as main.
    """
    passed, failed = [], []
    for name, func in globals().items():
        if name.startswith('test') and callable(func):
            try:
                func()
            except Exception as err:
                failed.append(f'{name}: {str(err)}')
                continue
            passed.append(name)
    if not failed:
        print(f'All {len(passed)} tests passed.')
    else:
        print(f'Total {len(passed) + len(failed)} tests, failed {len(failed)}:')
        for test in failed:
            print(test)


if __name__ == '__main__':
    run_tests()
