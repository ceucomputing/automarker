from unittest import mock
from os import path
import io

BASE_SCOPE = {
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': __loader__,
    '__spec__': None,
    '__annotations__': {},
    '__cached__': None
}


class Executor:

    def __init__(self, filename, bytecode, test_input):
        self._bytecode = bytecode
        self._in = io.StringIO(test_input)
        self._out = io.StringIO()
        self._scope = BASE_SCOPE.copy()
        self._scope['__file__'] = filename
        self._scope['__builtins__'] = __builtins__.__dict__.copy()
        self._scope['__builtins__']['input'] = self._input
        self._scope['__builtins__']['print'] = self._print

    def execute(self):
        exec(self._bytecode, self._scope, self._scope)
        return self._out.getvalue()

    def _input(self, prompt=None):
        with mock.patch('sys.stdin', new=self._in):
            return input()

    def _print(self, *args, **kwargs):
        with mock.patch('sys.stdout', new=self._out):
            return print(*args, **kwargs)


class TestCase:

    def __init__(self, test_input, expected_output):
        self.test_input = test_input
        self.expected_output = expected_output

    def __repr__(self):
        return repr({
            'test_input': self.test_input,
            'expected_output': self.expected_output
        })


class TestResult:

    def __init__(self, filename, test_case, success, output):
        self.filename = filename
        self.test_case = test_case
        self.success = success
        self.output = output

    def __repr__(self):
        return repr({
            'filename': self.filename,
            'test_case': self.test_case,
            'success': self.success,
            'output': self.output
        })


class Tester:

    def __init__(self, test_cases):
        self.test_cases = test_cases

    def test(self, filename):
        with open(filename) as f:
            source = f.read()
        bytecode = compile(source, filename, 'exec')
        results = []
        for test_case in self.test_cases:
            executor = Executor(filename, bytecode, test_case.test_input)
            try:
                output = executor.execute()
                results.append(TestResult(filename, test_case, output.strip(
                ) == test_case.expected_output.strip(), output))
            except Exception as e:
                results.append(TestResult(filename, test_case, False, str(e)))
        return results


test_cases = [
    TestCase('4\n12', '48\n'),
    TestCase('8\n2\n', '16\n'),
    TestCase('EEEE\n', '2\n'),
]
tester = Tester(test_cases)
results = tester.test('test/test_submission.py')
print(results)
