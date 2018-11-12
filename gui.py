import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import simpledialog as sd
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from unittest import mock
from functools import reduce
from os import path
import textwrap as tw
import glob
import io
import re
import os

# The following module code is adapted from https://github.com/foutaise/texttable/ under the MIT license.
# Copyright (C) 2003-2018 Gerome Fournier <jef(at)foutaise.org>


class ArraySizeError(Exception):
    """Exception raised when specified rows don't fit the required size
    """

    def __init__(self, msg):
        self.msg = msg
        Exception.__init__(self, msg, '')

    def __str__(self):
        return self.msg


class FallbackToText(Exception):
    """Used for failed conversion to float"""
    pass


class Texttable:

    BORDER = 1
    HEADER = 1 << 1
    HLINES = 1 << 2
    VLINES = 1 << 3

    def __init__(self, max_width=80):
        """Constructor

        - max_width is an integer, specifying the maximum width of the table
        - if set to 0, size is unlimited, therefore cells won't be wrapped
        """

        self.set_max_width(max_width)
        self._precision = 3

        self._deco = Texttable.VLINES | Texttable.HLINES | Texttable.BORDER | \
            Texttable.HEADER
        self.set_chars(['-', '|', '+', '='])
        self.reset()

    def reset(self):
        """Reset the instance

        - reset rows and header
        """

        self._hline_string = None
        self._row_size = None
        self._header = []
        self._rows = []
        return self

    def set_max_width(self, max_width):
        """Set the maximum width of the table

        - max_width is an integer, specifying the maximum width of the table
        - if set to 0, size is unlimited, therefore cells won't be wrapped
        """
        self._max_width = max_width if max_width > 0 else False
        return self

    def set_chars(self, array):
        """Set the characters used to draw lines between rows and columns

        - the array should contain 4 fields:

            [horizontal, vertical, corner, header]

        - default is set to:

            ['-', '|', '+', '=']
        """

        if len(array) != 4:
            raise ArraySizeError("array should contain 4 characters")
        array = [x[:1] for x in [str(s) for s in array]]
        (self._char_horiz, self._char_vert,
            self._char_corner, self._char_header) = array
        return self

    def set_deco(self, deco):
        """Set the table decoration

        - 'deco' can be a combinaison of:

            Texttable.BORDER: Border around the table
            Texttable.HEADER: Horizontal line below the header
            Texttable.HLINES: Horizontal lines between rows
            Texttable.VLINES: Vertical lines between columns

           All of them are enabled by default

        - example:

            Texttable.BORDER | Texttable.HEADER
        """

        self._deco = deco
        return self

    def set_header_align(self, array):
        """Set the desired header alignment

        - the elements of the array should be either "l", "c" or "r":

            * "l": column flushed left
            * "c": column centered
            * "r": column flushed right
        """

        self._check_row_size(array)
        self._header_align = array
        return self

    def set_cols_align(self, array):
        """Set the desired columns alignment

        - the elements of the array should be either "l", "c" or "r":

            * "l": column flushed left
            * "c": column centered
            * "r": column flushed right
        """

        self._check_row_size(array)
        self._align = array
        return self

    def set_cols_valign(self, array):
        """Set the desired columns vertical alignment

        - the elements of the array should be either "t", "m" or "b":

            * "t": column aligned on the top of the cell
            * "m": column aligned on the middle of the cell
            * "b": column aligned on the bottom of the cell
        """

        self._check_row_size(array)
        self._valign = array
        return self

    def set_cols_dtype(self, array):
        """Set the desired columns datatype for the cols.

        - the elements of the array should be either a callable or any of
          "a", "t", "f", "e" or "i":

            * "a": automatic (try to use the most appropriate datatype)
            * "t": treat as text
            * "f": treat as float in decimal format
            * "e": treat as float in exponential format
            * "i": treat as int
            * a callable: should return formatted string for any value given

        - by default, automatic datatyping is used for each column
        """

        self._check_row_size(array)
        self._dtype = array
        return self

    def set_cols_width(self, array):
        """Set the desired columns width

        - the elements of the array should be integers, specifying the
          width of each column. For example:

                [10, 20, 5]
        """

        self._check_row_size(array)
        try:
            array = list(map(int, array))
            if reduce(min, array) <= 0:
                raise ValueError
        except ValueError:
            raise
        self._width = array
        return self

    def set_precision(self, width):
        """Set the desired precision for float/exponential formats

        - width must be an integer >= 0

        - default value is set to 3
        """

        if not type(width) is int or width < 0:
            raise ValueError('width must be an integer greater then 0')
        self._precision = width
        return self

    def header(self, array):
        """Specify the header of the table
        """

        self._check_row_size(array)
        self._header = list(map(str, array))
        return self

    def add_row(self, array):
        """Add a row in the rows stack

        - cells can contain newlines and tabs
        """

        self._check_row_size(array)

        if not hasattr(self, "_dtype"):
            self._dtype = ["a"] * self._row_size

        cells = []
        for i, x in enumerate(array):
            cells.append(self._str(i, x))
        self._rows.append(cells)
        return self

    def add_rows(self, rows, header=True):
        """Add several rows in the rows stack

        - The 'rows' argument can be either an iterator returning arrays,
          or a by-dimensional array
        - 'header' specifies if the first row should be used as the header
          of the table
        """

        # nb: don't use 'iter' on by-dimensional arrays, to get a
        #     usable code for python 2.1
        if header:
            if hasattr(rows, '__iter__') and hasattr(rows, 'next'):
                self.header(rows.next())
            else:
                self.header(rows[0])
                rows = rows[1:]
        for row in rows:
            self.add_row(row)
        return self

    def draw(self):
        """Draw the table

        - the table is returned as a whole string
        """

        if not self._header and not self._rows:
            return
        self._compute_cols_width()
        self._check_align()
        out = ""
        if self._has_border():
            out += self._hline()
        if self._header:
            out += self._draw_line(self._header, isheader=True)
            if self._has_header():
                out += self._hline_header()
        length = 0
        for row in self._rows:
            length += 1
            out += self._draw_line(row)
            if self._has_hlines() and length < len(self._rows):
                out += self._hline()
        if self._has_border():
            out += self._hline()
        return out[:-1]

    @classmethod
    def _to_float(cls, x):
        if x is None:
            raise FallbackToText()
        try:
            return float(x)
        except (TypeError, ValueError):
            raise FallbackToText()

    @classmethod
    def _fmt_int(cls, x, **kw):
        """Integer formatting class-method.

        - x will be float-converted and then used.
        """
        return str(int(round(cls._to_float(x))))

    @classmethod
    def _fmt_float(cls, x, **kw):
        """Float formatting class-method.

        - x parameter is ignored. Instead kw-argument f being x float-converted
          will be used.

        - precision will be taken from `n` kw-argument.
        """
        n = kw.get('n')
        return '%.*f' % (n, cls._to_float(x))

    @classmethod
    def _fmt_exp(cls, x, **kw):
        """Exponential formatting class-method.

        - x parameter is ignored. Instead kw-argument f being x float-converted
          will be used.

        - precision will be taken from `n` kw-argument.
        """
        n = kw.get('n')
        return '%.*e' % (n, cls._to_float(x))

    @classmethod
    def _fmt_text(cls, x, **kw):
        """String formatting class-method."""
        return str(x)

    @classmethod
    def _fmt_auto(cls, x, **kw):
        """auto formatting class-method."""
        f = cls._to_float(x)
        if abs(f) > 1e8:
            fn = cls._fmt_exp
        else:
            if f - round(f) == 0:
                fn = cls._fmt_int
            else:
                fn = cls._fmt_float
        return fn(x, **kw)

    def _str(self, i, x):
        """Handles string formatting of cell data

            i - index of the cell datatype in self._dtype
            x - cell data to format
        """
        FMT = {
            'a': self._fmt_auto,
            'i': self._fmt_int,
            'f': self._fmt_float,
            'e': self._fmt_exp,
            't': self._fmt_text,
        }

        n = self._precision
        dtype = self._dtype[i]
        try:
            if callable(dtype):
                return dtype(x)
            else:
                return FMT[dtype](x, n=n)
        except FallbackToText:
            return self._fmt_text(x)

    def _check_row_size(self, array):
        """Check that the specified array fits the previous rows size
        """

        if not self._row_size:
            self._row_size = len(array)
        elif self._row_size != len(array):
            raise ArraySizeError("array should contain %d elements"
                                 % self._row_size)

    def _has_vlines(self):
        """Return a boolean, if vlines are required or not
        """

        return self._deco & Texttable.VLINES > 0

    def _has_hlines(self):
        """Return a boolean, if hlines are required or not
        """

        return self._deco & Texttable.HLINES > 0

    def _has_border(self):
        """Return a boolean, if border is required or not
        """

        return self._deco & Texttable.BORDER > 0

    def _has_header(self):
        """Return a boolean, if header line is required or not
        """

        return self._deco & Texttable.HEADER > 0

    def _hline_header(self):
        """Print header's horizontal line
        """

        return self._build_hline(True)

    def _hline(self):
        """Print an horizontal line
        """

        if not self._hline_string:
            self._hline_string = self._build_hline()
        return self._hline_string

    def _build_hline(self, is_header=False):
        """Return a string used to separated rows or separate header from
        rows
        """
        horiz = self._char_horiz
        if (is_header):
            horiz = self._char_header
        # compute cell separator
        s = "%s%s%s" % (horiz, [horiz, self._char_corner][self._has_vlines()],
                        horiz)
        # build the line
        l = s.join([horiz * n for n in self._width])
        # add border if needed
        if self._has_border():
            l = "%s%s%s%s%s\n" % (self._char_corner, horiz, l, horiz,
                                  self._char_corner)
        else:
            l += "\n"
        return l

    def _len_cell(self, cell):
        """Return the width of the cell

        Special characters are taken into account to return the width of the
        cell, such like newlines and tabs
        """

        cell_lines = cell.split('\n')
        maxi = 0
        for line in cell_lines:
            length = 0
            parts = line.split('\t')
            for part, i in zip(parts, list(range(1, len(parts) + 1))):
                length = length + len(part)
                if i < len(parts):
                    length = (length//8 + 1) * 8
            maxi = max(maxi, length)
        return maxi

    def _compute_cols_width(self):
        """Return an array with the width of each column

        If a specific width has been specified, exit. If the total of the
        columns width exceed the table desired width, another width will be
        computed to fit, and cells will be wrapped.
        """

        if hasattr(self, "_width"):
            return
        maxi = []
        if self._header:
            maxi = [self._len_cell(x) for x in self._header]
        for row in self._rows:
            for cell, i in zip(row, list(range(len(row)))):
                try:
                    maxi[i] = max(maxi[i], self._len_cell(cell))
                except (TypeError, IndexError):
                    maxi.append(self._len_cell(cell))

        ncols = len(maxi)
        content_width = sum(maxi)
        deco_width = 3*(ncols-1) + [0, 4][self._has_border()]
        if self._max_width and (content_width + deco_width) > self._max_width:
            """ content too wide to fit the expected max_width
            let's recompute maximum cell width for each cell
            """
            if self._max_width < (ncols + deco_width):
                raise ValueError('max_width too low to render data')
            available_width = self._max_width - deco_width
            newmaxi = [0] * ncols
            i = 0
            while available_width > 0:
                if newmaxi[i] < maxi[i]:
                    newmaxi[i] += 1
                    available_width -= 1
                i = (i + 1) % ncols
            maxi = newmaxi
        self._width = maxi

    def _check_align(self):
        """Check if alignment has been specified, set default one if not
        """

        if not hasattr(self, "_header_align"):
            self._header_align = ["c"] * self._row_size
        if not hasattr(self, "_align"):
            self._align = ["l"] * self._row_size
        if not hasattr(self, "_valign"):
            self._valign = ["t"] * self._row_size

    def _draw_line(self, line, isheader=False):
        """Draw a line

        Loop over a single cell length, over all the cells
        """

        line = self._splitit(line, isheader)
        space = " "
        out = ""
        for i in range(len(line[0])):
            if self._has_border():
                out += "%s " % self._char_vert
            length = 0
            for cell, width, align in zip(line, self._width, self._align):
                length += 1
                cell_line = cell[i]
                fill = width - len(cell_line)
                if isheader:
                    align = self._header_align[length - 1]
                if align == "r":
                    out += fill * space + cell_line
                elif align == "c":
                    out += (int(fill/2) * space + cell_line
                            + int(fill/2 + fill % 2) * space)
                else:
                    out += cell_line + fill * space
                if length < len(line):
                    out += " %s " % [space,
                                     self._char_vert][self._has_vlines()]
            out += "%s\n" % ['', space + self._char_vert][self._has_border()]
        return out

    def _splitit(self, line, isheader):
        """Split each element of line to fit the column width

        Each element is turned into a list, result of the wrapping of the
        string to the desired width
        """

        line_wrapped = []
        for cell, width in zip(line, self._width):
            array = []
            for c in cell.split('\n'):
                if c.strip() == "":
                    array.append("")
                else:
                    array.extend(tw.wrap(c, width))
            line_wrapped.append(array)
        max_cell_lines = reduce(max, list(map(len, line_wrapped)))
        for cell, valign in zip(line_wrapped, self._valign):
            if isheader:
                valign = "t"
            if valign == "m":
                missing = max_cell_lines - len(cell)
                cell[:0] = [""] * int(missing / 2)
                cell.extend([""] * int(missing / 2 + missing % 2))
            elif valign == "b":
                cell[:0] = [""] * (max_cell_lines - len(cell))
            else:
                cell.extend([""] * (max_cell_lines - len(cell)))
        return line_wrapped


BASE_SCOPE = {
    '__name__': '__main__',
    '__doc__': None,
    '__package__': None,
    '__loader__': __loader__,
    '__spec__': None,
    '__annotations__': {},
    '__cached__': None
}

DEFAULT_PREFIX = '###'
PADX = 6
PADY = 6
READONLY_BG = 'light gray'

INSTRUCTIONS = '''This automarker automatically runs test cases on multiple Python programs and generates a summary report. To use:

(1) Click 'Change Prefix...' to set the prefix if needed.
(2) Click 'Load...' and select a .txt file containing test cases.
(3) Click 'Choose Folder...' and locate the Python programs.
(4) Check 'Use subfolders' if the programs are in subfolders.
(5) Click 'Generate Report and Save Report As...' and save the report as a .txt file.

Test cases must be stored in a text file with a .txt extension. Each test case has an input section followed by an output section. Each section must begin with a header line that starts with a configurable prefix ({0} by default). The header line is only used to detect the start of a section and is otherwise ignored. The text file can contain multiple test cases by alternating between input and output sections.

For a test case, each line in the input section corresponds to a line of text that the automarker will provide when the input() function is encountered. Similarly, each line in the output section corresponds to a line of text that the program is expected to generate using the print() function. The test case is failed if the actual output generated by the program does not match the expected output exactly.'''.format(DEFAULT_PREFIX)

EXAMPLE = '''The .txt file on the left has 3 test cases for an integer addition problem. Using this file, the automarker will simulate 3 test runs for each Python program. On the right, you can see the 3 simulated test runs for a program that passes 2 out of the 3 test cases.'''

SAMPLE = '''{0} Test Case 1: Input
1
1
{0} Test Case 1: Output
2
{0} Test Case 2: Input
1
-1
{0} Test Case 3: Output
0
{0} Test Case 3: Input
1
one
{0} Test Case 3: Output
Error'''.format(DEFAULT_PREFIX)

RUN1 = '''Enter x: 1
Enter y: 1
2'''

RUN2 = '''Enter x: 1
Enter y: -1
Error'''

RUN3 = '''Enter x: 1
Enter y: one
Error'''

TEST_CASES_STATUS = '{0} test case(s) loaded'
TEST_CASES_STATUS_NONE = 'No test cases loaded'
TEST_CASES_TITLE = 'Test Case {0} out of {1}'

SUBMISSIONS_FOLDER_NONE = 'No folder chosen'
SUBMISSIONS_STATUS = '{0} submission(s) found'
SUBMISSIONS_STATUS_NONE = 'No submissions found'

REPORT_STATUS = 'Ready to run {0} test case(s) on {1} submission(s)'
REPORT_STATUS_NONE = 'Not ready'


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
                results.append(TestResult(filename, test_case, output.rstrip(
                ) == test_case.expected_output.rstrip(), output))
            except Exception as e:
                results.append(TestResult(filename, test_case, False, str(e)))
        return results


class AutoMarker:

    def __init__(self):
        self.test_cases_raw = None
        self.test_cases = None
        self.prefix = DEFAULT_PREFIX
        self.folder = None
        self.subfolders = False
        self.files = None

    def is_ready(self):
        return self.test_cases and self.files

    def set_test_cases_raw(self, test_cases_raw):
        self.test_cases_raw = test_cases_raw
        return self._parse()

    def set_prefix(self, prefix):
        self.prefix = prefix
        return self._parse()

    def _parse(self):
        if not self.test_cases_raw:
            self.test_cases = None
            return False
        sections = re.split(r'^' + re.escape(self.prefix) +
                            r'[^\n]*\n', self.test_cases_raw, flags=re.MULTILINE)
        if len(sections) < 3 or len(sections) % 2 == 0:
            self.test_cases_raw = None
            self.test_cases = None
            return False
        self.test_cases = []
        for i in range(1, len(sections), 2):
            self.test_cases.append(TestCase(sections[i], sections[i + 1]))
        return True

    def set_folder(self, folder):
        self.folder = folder
        return self._search()

    def set_subfolders(self, subfolders):
        self.subfolders = subfolders
        return self._search()

    def refresh(self):
        return self._search()

    def _search(self):
        if not self.folder:
            self.files = None
            return False
        pattern = self.folder
        if self.subfolders:
            pattern = path.join(pattern, '**')
        pattern = path.join(pattern, '*.py')
        self.files = glob.glob(pattern, recursive=True)
        return True

    def generate_report(self, f):
        tester = Tester(self.test_cases)
        results = [tester.test(filename) for filename in self.files]
        table = Texttable()
        table.header(['File name'] +
                     list(range(1, len(self.test_cases) + 1)) + ['Score'])
        perfects = 0
        for file_results in results:
            successes = [1 if result.success else 0 for result in file_results]
            score = sum(successes)
            if score == len(file_results):
                perfects += 1
            table.add_row([file_results[0].filename] + successes + [score])
        f.write(table.draw() + '\n\n')
        for file_results in results:
            f.write(file_results[0].filename + '\n')
            table = Texttable()
            table.header(['Failed Test Case', 'Input',
                          'Expected Output', 'Actual Output'])
            rows = 0
            for i in range(len(file_results)):
                result = file_results[i]
                if result.success:
                    continue
                table.add_row([i + 1, result.test_case.test_input,
                               result.test_case.expected_output, result.output])
                rows += 1
            if rows == 0:
                continue
            f.write(table.draw() + '\n\n')
        return perfects

class Gui:

    def __init__(self, automarker):
        self.automarker = automarker
        self.current_test_case = None
        self.current_submission = None
        self.make_widgets()
        self.layout_widgets()
        self.sync_test_cases()
        self.sync_submissions()
        self.sync_report()

    def make_widgets(self):
        self.root = tk.Tk()
        self.root.title('automarker')

        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)

        self.main = ttk.Frame(self.root)

        self.instructions = ttk.Labelframe(self.main, text='Instructions')
        self.instructions_text = st.ScrolledText(
            self.instructions, wrap='word', background=READONLY_BG, width=60)
        self.instructions_text.insert('0.1', INSTRUCTIONS)
        self.instructions_text.config(state='disabled')

        self.example = ttk.Labelframe(self.instructions, text='Example')
        self.example_text = st.ScrolledText(
            self.example, wrap='word', background=READONLY_BG, width=60, height=5)
        self.example_text.insert('0.1', EXAMPLE)
        self.example_text.config(state='disabled')
        self.example_sample = tk.Text(
            self.example, wrap='word', background=READONLY_BG, width=20, height=15)
        self.example_sample.insert('0.1', SAMPLE)
        self.example_sample.config(state='disabled')
        self.example_run1 = tk.Text(
            self.example, wrap='word', background=READONLY_BG, width=20, height=3)
        self.example_run1.insert('0.1', RUN1)
        self.example_run1.config(state='disabled')
        self.example_run2 = tk.Text(
            self.example, wrap='word', background=READONLY_BG, width=20, height=3)
        self.example_run2.insert('0.1', RUN2)
        self.example_run2.config(state='disabled')
        self.example_run3 = tk.Text(
            self.example, wrap='word', background=READONLY_BG, width=20, height=3)
        self.example_run3.insert('0.1', RUN3)
        self.example_run3.config(state='disabled')
        self.example_run1_result = ttk.Label(self.example, text="PASS")
        self.example_run2_result = ttk.Label(self.example, text="FAIL")
        self.example_run3_result = ttk.Label(self.example, text="PASS")

        self.test_cases = ttk.Labelframe(self.main, text='Test Cases')

        self.test_cases_header = ttk.Frame(self.test_cases)
        self.test_cases_load = ttk.Button(
            self.test_cases_header, text='Load...', command=self.load_test_cases)
        self.test_cases_status = ttk.Label(
            self.test_cases_header, text=TEST_CASES_STATUS_NONE)
        self.test_cases_change = ttk.Button(
            self.test_cases_header, text='Change Prefix...', command=self.change_prefix)
        self.test_cases_prefix = ttk.Label(
            self.test_cases_header, text=DEFAULT_PREFIX)

        self.test_cases_nav = ttk.Frame(self.test_cases)
        self.test_cases_prev = ttk.Button(
            self.test_cases_nav, text="<", command=self.prev_test_case)
        self.test_cases_prev.config(state='disabled')
        self.test_cases_title = ttk.Label(
            self.test_cases_nav, text=TEST_CASES_TITLE.format('-', '-'), anchor='center')
        self.test_cases_next = ttk.Button(
            self.test_cases_nav, text=">", command=self.next_test_case)
        self.test_cases_next.config(state='disabled')

        self.test_cases_viewer = ttk.Frame(self.test_cases)
        self.test_cases_input_label = ttk.Label(
            self.test_cases_viewer, text='Input')
        self.test_cases_output_label = ttk.Label(
            self.test_cases_viewer, text='Expected Output')
        self.test_cases_input = st.ScrolledText(
            self.test_cases_viewer, wrap='word', background=READONLY_BG, width=30, height=10)
        self.test_cases_input.config(state='disabled')
        self.test_cases_output = st.ScrolledText(
            self.test_cases_viewer, wrap='word', background=READONLY_BG, width=30, height=10)
        self.test_cases_output.config(state='disabled')

        self.submissions = ttk.Labelframe(self.main, text="Python Submissions")

        self.submissions_header = ttk.Frame(self.submissions)
        self.submissions_choose = ttk.Button(
            self.submissions_header, text='Choose Folder...', command=self.choose_folder)
        self.submissions_folder = ttk.Label(
            self.submissions_header, text=SUBMISSIONS_FOLDER_NONE)
        self.submissions_subfolders_var = tk.StringVar()
        self.submissions_subfolders = ttk.Checkbutton(
            self.submissions_header, text='Include subfolders', variable=self.submissions_subfolders_var, onvalue='True', offvalue='False', command=self.toggle_subfolders)
        self.submissions_refresh = ttk.Button(
            self.submissions_header, text='Search Again', command=self.refresh_files)
        self.submissions_refresh.config(state='disabled')
        self.submissions_status = ttk.Label(
            self.submissions_header, text=SUBMISSIONS_STATUS_NONE)

        self.submissions_preview = ttk.Frame(self.submissions)

        self.submissions_files_label = ttk.Label(
            self.submissions_preview, text='File Name')
        self.submissions_contents_label = ttk.Label(
            self.submissions_preview, text='Contents')

        self.submissions_files = ttk.Frame(self.submissions_preview)
        self.submissions_files_var = tk.StringVar()
        self.submissions_files_list = tk.Listbox(
            self.submissions_files, listvariable=self.submissions_files_var)
        self.submissions_files_list.bind('<<ListboxSelect>>', self.select_file)
        self.submissions_files_scrollbarx = ttk.Scrollbar(
            self.submissions_files, orient='horizontal', command=self.submissions_files_list.xview)
        self.submissions_files_list.config(
            xscrollcommand=self.submissions_files_scrollbarx.set)
        self.submissions_files_scrollbary = ttk.Scrollbar(
            self.submissions_files, orient='vertical', command=self.submissions_files_list.yview)
        self.submissions_files_list.config(
            yscrollcommand=self.submissions_files_scrollbary.set)

        self.submissions_contents = st.ScrolledText(
            self.submissions_preview, wrap='none', background=READONLY_BG, width=30, height=10)
        self.submissions_contents.config(state='disabled')

        self.report = ttk.Frame(self.main)
        self.report_generate = ttk.Button(
            self.report, text='Run Test Cases and Save Report As...', command=self.generate_report)
        self.report_generate.config(state='disabled')
        self.report_status = ttk.Label(self.report, text=REPORT_STATUS_NONE)

    def layout_widgets(self):
        common_kwargs = {
            'sticky': 'nsew', 'padx': PADX, 'pady': PADY
        }

        self.example_text.grid(column=0, columnspan=3, row=0, **common_kwargs)
        self.example_sample.grid(column=0, row=1, rowspan=3, **common_kwargs)
        self.example_run1.grid(column=1, row=1, **common_kwargs)
        self.example_run2.grid(column=1, row=2, **common_kwargs)
        self.example_run3.grid(column=1, row=3, **common_kwargs)
        self.example_run1_result.grid(column=2, row=1, **common_kwargs)
        self.example_run2_result.grid(column=2, row=2, **common_kwargs)
        self.example_run3_result.grid(column=2, row=3, **common_kwargs)
        self.example.columnconfigure(0, weight=4, minsize=200)
        self.example.columnconfigure(1, weight=3, minsize=150)
        self.example.columnconfigure(2, weight=0)
        self.example.rowconfigure(0, weight=0)
        self.example.rowconfigure(1, weight=0)
        self.example.rowconfigure(2, weight=0)
        self.example.rowconfigure(3, weight=0)

        self.instructions_text.grid(column=0, row=0, **common_kwargs)
        self.example.grid(column=0, row=1, ipadx=PADX,
                          ipady=PADY, **common_kwargs)
        self.instructions.columnconfigure(0, weight=1)
        self.instructions.rowconfigure(0, weight=1)
        self.instructions.rowconfigure(1, weight=0)

        self.test_cases_load.grid(column=0, row=0, **common_kwargs)
        self.test_cases_status.grid(column=1, row=0, **common_kwargs)
        self.test_cases_change.grid(column=2, row=0, **common_kwargs)
        self.test_cases_prefix.grid(column=3, row=0, **common_kwargs)
        self.test_cases_header.columnconfigure(0, weight=0)
        self.test_cases_header.columnconfigure(1, weight=1)
        self.test_cases_header.columnconfigure(2, weight=0)
        self.test_cases_header.columnconfigure(3, weight=0)
        self.test_cases_header.rowconfigure(0, weight=0)

        self.test_cases_prev.grid(column=0, row=0, **common_kwargs)
        self.test_cases_title.grid(column=1, row=0, **common_kwargs)
        self.test_cases_next.grid(column=2, row=0, **common_kwargs)
        self.test_cases_nav.columnconfigure(0, weight=0)
        self.test_cases_nav.columnconfigure(1, weight=1)
        self.test_cases_nav.columnconfigure(2, weight=0)
        self.test_cases_nav.rowconfigure(0, weight=0)

        self.test_cases_input_label.grid(column=0, row=0, **common_kwargs)
        self.test_cases_output_label.grid(column=1, row=0, **common_kwargs)
        self.test_cases_input.grid(column=0, row=1, **common_kwargs)
        self.test_cases_output.grid(column=1, row=1, **common_kwargs)
        self.test_cases_viewer.columnconfigure(0, weight=1, uniform='viewer')
        self.test_cases_viewer.columnconfigure(1, weight=1, uniform='viewer')
        self.test_cases_viewer.rowconfigure(0, weight=0)
        self.test_cases_viewer.rowconfigure(1, weight=1)

        self.test_cases_header.grid(column=0, row=0, sticky='nsew')
        self.test_cases_nav.grid(column=0, row=1, sticky='nsew')
        self.test_cases_viewer.grid(column=0, row=2, sticky='nsew')
        self.test_cases.columnconfigure(0, weight=1)
        self.test_cases.rowconfigure(0, weight=0)
        self.test_cases.rowconfigure(1, weight=0)
        self.test_cases.rowconfigure(2, weight=1)

        self.submissions_choose.grid(column=0, row=0, **common_kwargs)
        self.submissions_folder.grid(column=1, row=0, **common_kwargs)
        self.submissions_subfolders.grid(column=2, row=0, **common_kwargs)
        self.submissions_refresh.grid(column=0, row=1, **common_kwargs)
        self.submissions_status.grid(
            column=1, columnspan=2, row=1, **common_kwargs)
        self.submissions_header.columnconfigure(0, weight=0)
        self.submissions_header.columnconfigure(1, weight=1)
        self.submissions_header.columnconfigure(2, weight=0)
        self.submissions_header.rowconfigure(0, weight=0)
        self.submissions_header.rowconfigure(1, weight=0)

        self.submissions_files_list.grid(column=0, row=0, sticky='nsew')
        self.submissions_files_scrollbary.grid(column=1, row=0, sticky='nsew')
        self.submissions_files_scrollbarx.grid(column=0, row=1, sticky='nsew')
        self.submissions_files.columnconfigure(0, weight=1)
        self.submissions_files.columnconfigure(1, weight=0)
        self.submissions_files.rowconfigure(0, weight=1)
        self.submissions_files.rowconfigure(1, weight=0)

        self.submissions_files_label.grid(column=0, row=0, **common_kwargs)
        self.submissions_contents_label.grid(column=1, row=0, **common_kwargs)
        self.submissions_files.grid(column=0, row=1, **common_kwargs)
        self.submissions_contents.grid(column=1, row=1, **common_kwargs)
        self.submissions_preview.columnconfigure(0, weight=1, uniform='files')
        self.submissions_preview.columnconfigure(1, weight=1, uniform='files')
        self.submissions_preview.rowconfigure(0, weight=0)
        self.submissions_preview.rowconfigure(1, weight=1)

        self.submissions_header.grid(column=0, row=0, sticky='nsew')
        self.submissions_preview.grid(column=0, row=1, sticky='nsew')
        self.submissions.columnconfigure(0, weight=1)
        self.submissions.rowconfigure(0, weight=0)
        self.submissions.rowconfigure(1, weight=1)

        self.report_generate.grid(column=0, row=0, **common_kwargs)
        self.report_status.grid(column=1, row=0, **common_kwargs)
        self.report.columnconfigure(0, weight=0)
        self.report.columnconfigure(1, weight=1)
        self.report.rowconfigure(0, weight=0)

        self.instructions.grid(column=0, row=0, rowspan=3,
                               ipadx=PADX, ipady=PADY, **common_kwargs)
        self.test_cases.grid(column=1, row=0, ipadx=PADX,
                             ipady=PADY, **common_kwargs)
        self.submissions.grid(column=1, row=1, ipadx=PADX,
                              ipady=PADY, **common_kwargs)
        self.report.grid(column=1, row=2, ipadx=PADX,
                         ipady=PADY, **common_kwargs)
        self.main.columnconfigure(0, weight=1, uniform='mainx')
        self.main.columnconfigure(1, weight=1, uniform='mainx')
        self.main.rowconfigure(0, weight=1, uniform='mainy')
        self.main.rowconfigure(1, weight=1, uniform='mainy')
        self.main.rowconfigure(2, weight=0)

        self.main.grid(column=0, row=0, sticky='nsew', ipadx=PADX, ipady=PADY)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

    def run(self):
        self.root.mainloop()

    def load_test_cases(self):
        filename = fd.askopenfilename(filetypes=(
            ('Text Files', '.txt'), ('All Files', '*')))
        if not filename:
            return
        filename = path.abspath(filename)
        try:
            with open(filename) as f:
                test_cases_raw = f.read()
        except OSError as e:
            mb.showerror('Error', 'Error loading test cases:\n\n' + str(e))
            return
        if self.automarker.set_test_cases_raw(test_cases_raw):
            mb.showinfo('Success', '{} test case(s) successfully loaded.'.format(
                len(self.automarker.test_cases)))
            self.current_test_case = 0
        else:
            mb.showerror(
                'Error', 'Invalid test cases. Check that the prefix is set correctly and try again.')
            self.current_test_case = None
        self.sync_test_cases()
        self.sync_report()

    def change_prefix(self):
        prefix = sd.askstring(
            "Change Prefix", "Enter new prefix:", initialvalue=self.automarker.prefix)
        if not prefix:
            return
        had_test_cases = bool(self.automarker.test_cases)
        if not self.automarker.set_prefix(prefix) and had_test_cases:
            mb.showwarning(
                'Warning', 'Existing test cases are incompatible with new prefix and have been cleared.\n\nClick \'Load...\' to load new test cases.')
        self.sync_test_cases()
        self.sync_report()

    def prev_test_case(self):
        self.current_test_case = max(0, self.current_test_case - 1)
        self.sync_test_cases()

    def next_test_case(self):
        self.current_test_case = min(
            len(self.automarker.test_cases) - 1, self.current_test_case + 1)
        self.sync_test_cases()

    def choose_folder(self):
        folder = path.abspath(fd.askdirectory())
        if not folder:
            return
        self.automarker.set_folder(folder)
        self.sync_submissions()
        self.sync_report()

    def toggle_subfolders(self):
        self.automarker.set_subfolders(
            self.submissions_subfolders_var.get() == 'True')
        self.sync_submissions()
        self.sync_report()

    def refresh_files(self):
        self.automarker.refresh()
        self.sync_submissions()
        self.sync_report()

    def select_file(self, event):
        selection = self.submissions_files_list.curselection()
        if not selection:
            self._set_readonly_text(self.submissions_contents, '')
            return
        filename = self.automarker.files[selection[0]]
        try:
            with open(filename) as f:
                contents = f.read()
        except OSError as e:
            mb.showerror('Error', 'Error loading submission:\n\n' + str(e))
            self.refresh_files()
            return
        self._set_readonly_text(self.submissions_contents, contents)

    def generate_report(self):
        f = fd.asksaveasfile(filetypes=(
            ('Text Files', '.txt'), ('All Files', '*')))
        perfects = self.automarker.generate_report(f)
        f.close()
        mb.showinfo('Success', '{} out of {} submissions passed all test cases.'.format(perfects, len(self.automarker.files)))
        if hasattr(os, 'startfile'):
            os.startfile(f.name)

    def _set_readonly_text(self, widget, text):
        widget.config(state='normal')
        widget.replace('1.0', 'end', text)
        widget.config(state='disabled')

    def sync_test_cases(self):
        self.test_cases_prefix.config(text=self.automarker.prefix)
        if not self.automarker.test_cases:
            self.test_cases_status.config(text=TEST_CASES_STATUS_NONE)
            self.test_cases_prev.config(state='disabled')
            self.test_cases_title.config(
                text=TEST_CASES_TITLE.format('-', '-'))
            self.test_cases_next.config(state='disabled')
            self._set_readonly_text(self.test_cases_input, '')
            self._set_readonly_text(self.test_cases_output, '')
            return
        length = len(self.automarker.test_cases)
        if self.current_test_case is None:
            self.current_test_case = 0
        if self.current_test_case >= length:
            self.current_test_case = length - 1
        current = self.automarker.test_cases[self.current_test_case]
        self.test_cases_status.config(text=TEST_CASES_STATUS.format(length))
        self.test_cases_prev.config(
            state='normal' if self.current_test_case > 0 else 'disabled')
        self.test_cases_title.config(text=TEST_CASES_TITLE.format(
            self.current_test_case + 1, length))
        self.test_cases_next.config(
            state='normal' if self.current_test_case < length - 1 else 'disabled')
        self._set_readonly_text(self.test_cases_input, current.test_input)
        self._set_readonly_text(self.test_cases_output,
                                current.expected_output)

    def sync_submissions(self):
        self.submissions_folder.config(
            text=self.automarker.folder if self.automarker.folder else SUBMISSIONS_FOLDER_NONE)
        self.submissions_refresh.config(
            state='normal' if self.automarker.folder else 'disabled')
        if not self.automarker.files:
            self.submissions_status.config(text=SUBMISSIONS_STATUS_NONE)
            self.submissions_files_var.set([])
            self.submissions_files_list.config(state='disabled')
            self._set_readonly_text(self.submissions_contents, '')
            return
        self.submissions_status.config(
            text=SUBMISSIONS_STATUS.format(len(self.automarker.files)))
        self.submissions_files_list.config(state='normal')
        self.submissions_files_var.set(self.automarker.files)
        self.submissions_files_list.select_clear(0, 'end')
        self._set_readonly_text(self.submissions_contents, '')

    def sync_report(self):
        if not self.automarker.is_ready():
            self.report_generate.config(state='disabled')
            self.report_status.config(text=REPORT_STATUS_NONE)
            return
        self.report_generate.config(state='normal')
        self.report_status.config(text=REPORT_STATUS.format(
            len(self.automarker.test_cases), len(self.automarker.files)))


app = AutoMarker()
gui = Gui(app)
gui.run()
