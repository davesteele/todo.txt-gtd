import os

def pytest_generate_tests(metafunc):
    if 'file_case' in metafunc.fixturenames:
        cases = []
        for path in os.listdir("test/cases/"):
            if path[-3:] == ".in":
                cases.append(path[:-3])
        metafunc.parametrize('file_case', cases)
