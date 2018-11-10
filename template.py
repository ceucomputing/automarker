import io
import sys

_in = io.StringIO()
_out = io.StringIO()
_input = input


def input(prompt=None):
    return _input()


def _test(*args):
    _stdin = sys.stdin
    _stdout = sys.stdout
    _in.seek(0)
    _in.truncate(0)
    _in.write('\n'.join((str(arg) for arg in args)) + '\n')
    _in.seek(0)
    _out.seek(0)
    _out.truncate(0)
    sys.stdin = _in
    sys.stdout = _out
    exec(_code, locals(), globals())
    sys.stdin = _stdin
    sys.stdout = _stdout
    return _out.getvalue()


_code = r'''
'''
