# Manual Retrieval Review

## Strategy A

### T01: Vì sao nhiều số thập phân không thể biểu diễn chính xác bằng float nhị phân?

**Expected answer:** Vì phần lớn phân số thập phân không thể biểu diễn chính xác bằng phân số nhị phân hữu hạn.

**Gold evidence:**

> most decimal fractions cannot be represented exactly as
binary fractions.  A consequence is that, in general, the decimal
floating-point numbers you enter are only approximated by the binary
floating-point numbers actually stored in the machine.

The problem is easier to understand at first in base 10.  Consider the
fraction 1/3.  You can

**Required filter:** `None`

#### Rank 1

- Chunk: `python_datastructures_p009_fixed_001`
- Source: `datastructures.txt`
- Page: `9`
- Section: `datastructures`
- Distance: `0.7271`

```text
   >>> import math
   >>> raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8]
   >>> filtered_data = []
   >>> for value in raw_data:
   ...     if not math.isnan(value):
   ...         filtered_data.append(value)
   ...
   >>> filtered_data
   [56.2, 51.7, 55.3, 52.5, 47.8]

5.7. More on Conditions
=======================

The conditions used in "while" and "if" statements can contain any
operators, not just comparisons.

The comparison operators "in" and "not in" are membersh
```

#### Rank 2

- Chunk: `python_floatingpoint_p003_fixed_004`
- Source: `floatingpoint.txt`
- Page: `3`
- Section: `floatingpoint`
- Distance: `0.7808`

```text
888337719 / 1125899906842624
   True

The "float.hex()" method expresses a float in hexadecimal (base 16),
again giving the exact value stored by your computer:

   >>> x.hex()
   '0x1.921f9f01b866ep+1'

This precise hexadecimal representation can be used to reconstruct the
float value exactly:

   >>> x == float.fromhex('0x1.921f9f01b866ep+1')
   True

Since the representation is exact, it is useful for reliably porting
values across different versions of Python (platform independence) and
exch
```

#### Rank 3

- Chunk: `python_floatingpoint_p001_fixed_004`
- Source: `floatingpoint.txt`
- Page: `1`
- Section: `floatingpoint`
- Distance: `0.7824`

```text
011001100110011001100110011001100110011...

Stop at any finite number of bits, and you get an approximation.  On
most machines today, floats are approximated using a binary fraction
with the numerator using the first 53 bits starting with the most
significant bit and with the denominator as a power of two.  In the
case of 1/10, the binary fraction is "3602879701896397 / 2 ** 55"
which is close to but not exactly equal to the true value of 1/10.

Many users are not aware of the approximation beca
```

---

### T02: Khác biệt giữa del theo chỉ số và pop() của list là gì?

**Expected answer:** del xóa phần tử theo chỉ số mà không trả về giá trị; pop() trả về giá trị đã xóa.

**Gold evidence:**

> There is a way to remove an item from a list given its index instead
of its value: the "del" statement.  This differs from the "pop()"
method which returns a value.  The "del" statement can also be used to
remove slices from a list or clear the entire list (which we did
earlier by assignment of an empty list to the slice).  For example:

**Required filter:** `None`

#### Rank 1

- Chunk: `python_datastructures_p001_fixed_007`
- Source: `datastructures.txt`
- Page: `1`
- Section: `datastructures`
- Distance: `0.7445`

```text
le', 'banana', 'banana', 'grape', 'kiwi', 'orange', 'pear']
   >>> fruits.pop()
   'pear'


```

#### Rank 2

- Chunk: `python_datastructures_p007_fixed_005`
- Source: `datastructures.txt`
- Page: `7`
- Section: `datastructures`
- Distance: `0.8080`

```text
lue) if the key is not in the
dictionary.

Performing "list(d)" on a dictionary returns a list of all the keys
used in the dictionary, in insertion order (if you want it sorted,
just use "sorted(d)" instead). To check whether a single key is in the
dictionary, use the "in" keyword.

Here is a small example using a dictionary:

   >>> tel = {'jack': 4098, 'sape': 4139}
   >>> tel['guido'] = 4127
   >>> tel
   {'jack': 4098, 'sape': 4139, 'guido': 4127}
   >>> tel['jack']
   4098
   >>> tel['irv']
```

#### Rank 3

- Chunk: `python_stdlib2_p005_fixed_001`
- Source: `stdlib2.txt`
- Page: `5`
- Section: `stdlib2`
- Distance: `0.8214`

```text
In addition to alternative list implementations, the library also
offers other tools such as the "bisect" module with functions for
manipulating sorted lists:

   >>> import bisect
   >>> scores = [(100, 'perl'), (200, 'tcl'), (400, 'lua'), (500, 'python')]
   >>> bisect.insort(scores, (300, 'ruby'))
   >>> scores
   [(100, 'perl'), (200, 'tcl'), (300, 'ruby'), (400, 'lua'), (500, 'python')]

The "heapq" module provides functions for implementing heaps based on
regular lists.  The lowest valued 
```

---

### T03: Module datetime có hỗ trợ đối tượng nhận biết múi giờ không?

**Expected answer:** Có, datetime hỗ trợ đối tượng timezone-aware.

**Gold evidence:**

> The "datetime" module supplies classes for manipulating dates and
times in both simple and complex ways. While date and time arithmetic
is supported, the focus of the implementation is on efficient member
extraction for output formatting and manipulation.  The module also
supports objects that are timezone aware.

   >>> # dates are easil

**Required filter:** `None`

#### Rank 1

- Chunk: `python_stdlib_p003_fixed_001`
- Source: `stdlib.txt`
- Page: `3`
- Section: `stdlib`
- Distance: `0.6060`

```text
The "datetime" module supplies classes for manipulating dates and
times in both simple and complex ways. While date and time arithmetic
is supported, the focus of the implementation is on efficient member
extraction for output formatting and manipulation.  The module also
supports objects that are timezone aware.

   >>> # dates are easily constructed and formatted
   >>> import datetime as dt
   >>> now = dt.date.today()
   >>> now
   datetime.date(2003, 12, 2)
   >>> now.strftime("%m-%d-%y. %d
```

#### Rank 2

- Chunk: `python_stdlib_p002_fixed_007`
- Source: `stdlib.txt`
- Page: `2`
- Section: `stdlib`
- Distance: `0.6278`

```text
 example needs a mailserver running on
localhost.)

10.8. Dates and times
=====================


```

#### Rank 3

- Chunk: `python_stdlib_p003_fixed_002`
- Source: `stdlib.txt`
- Page: `3`
- Section: `stdlib`
- Distance: `0.6424`

```text
ate(2003, 12, 2)
   >>> now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B.")
   '12-02-03. 02 Dec 2003 is a Tuesday on the 02 day of December.'

   >>> # dates support calendar arithmetic
   >>> birthday = dt.date(1964, 7, 31)
   >>> age = now - birthday
   >>> age.days
   14368

10.9. Data compression
======================

Common data archiving and compression formats are directly supported
by modules including: "zlib", "gzip", "bz2", "lzma", "zipfile" and
"tarfile".

   >>> import
```

---

### T04: Trong interactive shell mới, phím F3 dùng để làm gì?

**Expected answer:** F3 bật paste mode và nhấn lại để trở về prompt thường.

**Gold evidence:**

> "F3"
enters "paste mode", which makes pasting larger blocks of code easier.
Press "F3" to return to the regular prompt.

When using the new interactive shell, exit the shell by typing "exit"
or "quit". Adding call parentheses after those commands is not
required.

If the new interactive shell is not desired, it can be disabled via
the "PY

**Required filter:** `None`

#### Rank 1

- Chunk: `python_appendix_p001_fixed_002`
- Source: `appendix.txt`
- Page: `1`
- Section: `appendix`
- Distance: `0.7307`

```text
dditional functionality. "F1" enters the
interactive help browser "pydoc". "F2" allows for browsing command-
line history with neither output nor the *>>>* and *...* prompts. "F3"
enters "paste mode", which makes pasting larger blocks of code easier.
Press "F3" to return to the regular prompt.

When using the new interactive shell, exit the shell by typing "exit"
or "quit". Adding call parentheses after those commands is not
required.

If the new interactive shell is not desired, it can be disab
```

#### Rank 2

- Chunk: `python_interactive_p001_fixed_005`
- Source: `interactive.txt`
- Page: `1`
- Section: `interactive`
- Distance: `0.7520`

```text
alternative enhanced interactive interpreter that has been around
for quite some time is IPython, which features tab completion, object
exploration and advanced history management.  It can also be
thoroughly customized and embedded into other applications.  Another
similar enhanced interactive environment is bpython.
```

#### Rank 3

- Chunk: `python_modules_p005_fixed_001`
- Source: `modules.txt`
- Page: `5`
- Section: `modules`
- Distance: `0.7559`

```text
   >>> import fibo, sys
   >>> dir(fibo)
   ['__name__', 'fib', 'fib2']
   >>> dir(sys)
   ['__breakpointhook__', '__displayhook__', '__doc__', '__excepthook__',
    '__interactivehook__', '__loader__', '__name__', '__package__', '__spec__',
    '__stderr__', '__stdin__', '__stdout__', '__unraisablehook__',
    '_clear_type_cache', '_current_frames', '_debugmallocstats', '_framework',
    '_getframe', '_git', '_home', '_xoptions', 'abiflags', 'addaudithook',
    'api_version', 'argv', 'audit', '
```

---

### T05: Theo tài liệu, threading giúp ứng dụng phản hồi người dùng tốt hơn như thế nào?

**Expected answer:** Cho phép tác vụ chạy nền trong khi ứng dụng vẫn nhận đầu vào và tiếp tục công việc khác.

**Gold evidence:**

> Threading is a technique for decoupling tasks which are not
sequentially dependent.  Threads can be used to improve the
responsiveness of applications that accept user input while other
tasks run in the background.  A related use case is running I/O in
parallel with computations in another thread.

The following code shows how the high le

**Required filter:** `{'section': 'stdlib2'}`

#### Rank 1

- Chunk: `python_stdlib2_p002_fixed_007`
- Source: `stdlib2.txt`
- Page: `2`
- Section: `stdlib2`
- Distance: `0.7881`

```text
omp_size, uncomp_size)

       start += extra_size + comp_size     # skip to the next header

11.4. Multi-threading
=====================


```

#### Rank 2

- Chunk: `python_appetite_p001_fixed_009`
- Source: `appetite.txt`
- Page: `1`
- Section: `appetite`
- Distance: `0.8058`

```text
nguage is named after the BBC show "Monty Python's
Flying Circus" and has nothing to do with reptiles.  Making references
to Monty Python skits in documentation is not only allowed, it is
encouraged!

Now that you are all excited about Python, you'll want to examine it
in some more detail.  Since the best way to learn a language is to use
it, the tutorial invites you to play with the Python interpreter as
you read.

In the next chapter, the mechanics of using the interpreter are
explained.  This
```

#### Rank 3

- Chunk: `python_stdlib2_p003_fixed_004`
- Source: `stdlib2.txt`
- Page: `3`
- Section: `stdlib2`
- Distance: `0.8085`

```text
nd semaphores.

While those tools are powerful, minor design errors can result in
problems that are difficult to reproduce.  So, the preferred approach
to task coordination is to concentrate all access to a resource in a
single thread and then use the "queue" module to feed that thread with
requests from other threads. Applications using "Queue" objects for
inter-thread communication and coordination are easier to design, more
readable, and more reliable.

11.5. Logging
=============

The "loggi
```

---

## Strategy B

### T01: Vì sao nhiều số thập phân không thể biểu diễn chính xác bằng float nhị phân?

**Expected answer:** Vì phần lớn phân số thập phân không thể biểu diễn chính xác bằng phân số nhị phân hữu hạn.

**Gold evidence:**

> most decimal fractions cannot be represented exactly as
binary fractions.  A consequence is that, in general, the decimal
floating-point numbers you enter are only approximated by the binary
floating-point numbers actually stored in the machine.

The problem is easier to understand at first in base 10.  Consider the
fraction 1/3.  You can

**Required filter:** `None`

#### Rank 1

- Chunk: `python_datastructures_p009_paragraph_001`
- Source: `datastructures.txt`
- Page: `9`
- Section: `datastructures`
- Distance: `0.7229`

```text
   >>> import math
   >>> raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8]
   >>> filtered_data = []
   >>> for value in raw_data:
   ...     if not math.isnan(value):
   ...         filtered_data.append(value)
   ...
   >>> filtered_data
   [56.2, 51.7, 55.3, 52.5, 47.8]

5.7. More on Conditions
=======================

The conditions used in "while" and "if" statements can contain any
operators, not just comparisons.


```

#### Rank 2

- Chunk: `python_floatingpoint_p001_paragraph_001`
- Source: `floatingpoint.txt`
- Page: `1`
- Section: `floatingpoint`
- Distance: `0.7453`

```text
15. Floating-Point Arithmetic:  Issues and Limitations
******************************************************


```

#### Rank 3

- Chunk: `python_introduction_p002_paragraph_001`
- Source: `introduction.txt`
- Page: `2`
- Section: `introduction`
- Distance: `0.7616`

```text
   >>> n  # try to access an undefined variable
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   NameError: name 'n' is not defined

There is full support for floating point; operators with mixed type
operands convert the integer operand to floating point:

   >>> 4 * 3.75 - 1
   14.0


```

---

### T02: Khác biệt giữa del theo chỉ số và pop() của list là gì?

**Expected answer:** del xóa phần tử theo chỉ số mà không trả về giá trị; pop() trả về giá trị đã xóa.

**Gold evidence:**

> There is a way to remove an item from a list given its index instead
of its value: the "del" statement.  This differs from the "pop()"
method which returns a value.  The "del" statement can also be used to
remove slices from a list or clear the entire list (which we did
earlier by assignment of an empty list to the slice).  For example:

**Required filter:** `None`

#### Rank 1

- Chunk: `python_datastructures_p007_paragraph_009`
- Source: `datastructures.txt`
- Page: `7`
- Section: `datastructures`
- Distance: `0.7443`

```text
   ['guido', 'irv', 'jack']
   >>> 'guido' in tel
   True
   >>> 'jack' not in tel
   False


```

#### Rank 2

- Chunk: `python_datastructures_p007_paragraph_008`
- Source: `datastructures.txt`
- Page: `7`
- Section: `datastructures`
- Distance: `0.7576`

```text
   >>> tel = {'jack': 4098, 'sape': 4139}
   >>> tel['guido'] = 4127
   >>> tel
   {'jack': 4098, 'sape': 4139, 'guido': 4127}
   >>> tel['jack']
   4098
   >>> tel['irv']
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   KeyError: 'irv'
   >>> print(tel.get('irv'))
   None
   >>> del tel['sape']
   >>> tel['irv'] = 4127
   >>> tel
   {'jack': 4098, 'guido': 4127, 'irv': 4127}
   >>> list(tel)
   ['jack', 'guido', 'irv']
   >>> sorted(tel)

```

#### Rank 3

- Chunk: `python_datastructures_p001_paragraph_007`
- Source: `datastructures.txt`
- Page: `1`
- Section: `datastructures`
- Distance: `0.7886`

```text
   >>> fruits.sort()
   >>> fruits
   ['apple', 'apple', 'banana', 'banana', 'grape', 'kiwi', 'orange', 'pear']
   >>> fruits.pop()
   'pear'


```

---

### T03: Module datetime có hỗ trợ đối tượng nhận biết múi giờ không?

**Expected answer:** Có, datetime hỗ trợ đối tượng timezone-aware.

**Gold evidence:**

> The "datetime" module supplies classes for manipulating dates and
times in both simple and complex ways. While date and time arithmetic
is supported, the focus of the implementation is on efficient member
extraction for output formatting and manipulation.  The module also
supports objects that are timezone aware.

   >>> # dates are easil

**Required filter:** `None`

#### Rank 1

- Chunk: `python_stdlib_p003_paragraph_001`
- Source: `stdlib.txt`
- Page: `3`
- Section: `stdlib`
- Distance: `0.5394`

```text
The "datetime" module supplies classes for manipulating dates and
times in both simple and complex ways. While date and time arithmetic
is supported, the focus of the implementation is on efficient member
extraction for output formatting and manipulation.  The module also
supports objects that are timezone aware.


```

#### Rank 2

- Chunk: `python_stdlib_p003_paragraph_002`
- Source: `stdlib.txt`
- Page: `3`
- Section: `stdlib`
- Distance: `0.6688`

```text
   >>> # dates are easily constructed and formatted
   >>> import datetime as dt
   >>> now = dt.date.today()
   >>> now
   datetime.date(2003, 12, 2)
   >>> now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B.")
   '12-02-03. 02 Dec 2003 is a Tuesday on the 02 day of December.'

   >>> # dates support calendar arithmetic
   >>> birthday = dt.date(1964, 7, 31)
   >>> age = now - birthday
   >>> age.days
   14368

10.9. Data compression
======================


```

#### Rank 3

- Chunk: `python_modules_p001_paragraph_001`
- Source: `modules.txt`
- Page: `1`
- Section: `modules`
- Distance: `0.7016`

```text
6. Modules
**********


```

---

### T04: Trong interactive shell mới, phím F3 dùng để làm gì?

**Expected answer:** F3 bật paste mode và nhấn lại để trở về prompt thường.

**Gold evidence:**

> "F3"
enters "paste mode", which makes pasting larger blocks of code easier.
Press "F3" to return to the regular prompt.

When using the new interactive shell, exit the shell by typing "exit"
or "quit". Adding call parentheses after those commands is not
required.

If the new interactive shell is not desired, it can be disabled via
the "PY

**Required filter:** `None`

#### Rank 1

- Chunk: `python_interactive_p001_paragraph_005`
- Source: `interactive.txt`
- Page: `1`
- Section: `interactive`
- Distance: `0.6980`

```text
14.2. Alternatives to the Interactive Interpreter
=================================================


```

#### Rank 2

- Chunk: `python_index_p002_paragraph_008`
- Source: `index.txt`
- Page: `2`
- Section: `index`
- Distance: `0.7447`

```text
  * 11.8. Decimal floating-point arithmetic

* 12. Virtual Environments and Packages

  * 12.1. Introduction

  * 12.2. Creating Virtual Environments

  * 12.3. Managing Packages with pip

* 13. What Now?

* 14. Interactive Input Editing and History Substitution

  * 14.1. Tab Completion and History Editing

  * 14.2. Alternatives to the Interactive Interpreter

* 15. Floating-Point Arithmetic:  Issues and Limitations

  * 15.1. Representation Error

* 16. Appendix

  * 16.1. Interactive Mode


```

#### Rank 3

- Chunk: `python_interactive_p001_paragraph_007`
- Source: `interactive.txt`
- Page: `1`
- Section: `interactive`
- Distance: `0.7551`

```text
One alternative enhanced interactive interpreter that has been around
for quite some time is IPython, which features tab completion, object
exploration and advanced history management.  It can also be
thoroughly customized and embedded into other applications.  Another
similar enhanced interactive environment is bpython.
```

---

### T05: Theo tài liệu, threading giúp ứng dụng phản hồi người dùng tốt hơn như thế nào?

**Expected answer:** Cho phép tác vụ chạy nền trong khi ứng dụng vẫn nhận đầu vào và tiếp tục công việc khác.

**Gold evidence:**

> Threading is a technique for decoupling tasks which are not
sequentially dependent.  Threads can be used to improve the
responsiveness of applications that accept user input while other
tasks run in the background.  A related use case is running I/O in
parallel with computations in another thread.

The following code shows how the high le

**Required filter:** `{'section': 'stdlib2'}`

#### Rank 1

- Chunk: `python_stdlib2_p001_paragraph_008`
- Source: `stdlib2.txt`
- Page: `1`
- Section: `stdlib2`
- Distance: `0.8214`

```text
   >>> from string import Template
   >>> t = Template('${village}folk send $$10 to $cause.')
   >>> t.substitute(village='Nottingham', cause='the ditch fund')
   'Nottinghamfolk send $10 to the ditch fund.'


```

#### Rank 2

- Chunk: `python_controlflow_p010_paragraph_005`
- Source: `controlflow.txt`
- Page: `10`
- Section: `controlflow`
- Distance: `0.8364`

```text
The third function "kwd_only_arg" only allows keyword arguments as
indicated by a "*" in the function definition:

   >>> kwd_only_arg(3)
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   TypeError: kwd_only_arg() takes 0 positional arguments but 1 was given

   >>> kwd_only_arg(arg=3)
   3

And the last uses all three calling conventions in the same function
definition:


```

#### Rank 3

- Chunk: `python_errors_p005_paragraph_004`
- Source: `errors.txt`
- Page: `5`
- Section: `errors`
- Distance: `0.8418`

```text
   >>> try:
   ...     raise KeyboardInterrupt
   ... finally:
   ...     print('Goodbye, world!')
   ...
   Goodbye, world!
   Traceback (most recent call last):
     File "<stdin>", line 2, in <module>
       raise KeyboardInterrupt
   KeyboardInterrupt


```

---

## Strategy C

### T01: Vì sao nhiều số thập phân không thể biểu diễn chính xác bằng float nhị phân?

**Expected answer:** Vì phần lớn phân số thập phân không thể biểu diễn chính xác bằng phân số nhị phân hữu hạn.

**Gold evidence:**

> most decimal fractions cannot be represented exactly as
binary fractions.  A consequence is that, in general, the decimal
floating-point numbers you enter are only approximated by the binary
floating-point numbers actually stored in the machine.

The problem is easier to understand at first in base 10.  Consider the
fraction 1/3.  You can

**Required filter:** `None`

#### Rank 1

- Chunk: `python_datastructures_p009_paragraph_001`
- Source: `datastructures.txt`
- Page: `9`
- Section: `datastructures`
- Distance: `0.7229`

```text
   >>> import math
   >>> raw_data = [56.2, float('NaN'), 51.7, 55.3, 52.5, float('NaN'), 47.8]
   >>> filtered_data = []
   >>> for value in raw_data:
   ...     if not math.isnan(value):
   ...         filtered_data.append(value)
   ...
   >>> filtered_data
   [56.2, 51.7, 55.3, 52.5, 47.8]

5.7. More on Conditions
=======================

The conditions used in "while" and "if" statements can contain any
operators, not just comparisons.


```

#### Rank 2

- Chunk: `python_floatingpoint_p001_paragraph_001`
- Source: `floatingpoint.txt`
- Page: `1`
- Section: `floatingpoint`
- Distance: `0.7453`

```text
15. Floating-Point Arithmetic:  Issues and Limitations
******************************************************


```

#### Rank 3

- Chunk: `python_introduction_p002_paragraph_001`
- Source: `introduction.txt`
- Page: `2`
- Section: `introduction`
- Distance: `0.7616`

```text
   >>> n  # try to access an undefined variable
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   NameError: name 'n' is not defined

There is full support for floating point; operators with mixed type
operands convert the integer operand to floating point:

   >>> 4 * 3.75 - 1
   14.0


```

---

### T02: Khác biệt giữa del theo chỉ số và pop() của list là gì?

**Expected answer:** del xóa phần tử theo chỉ số mà không trả về giá trị; pop() trả về giá trị đã xóa.

**Gold evidence:**

> There is a way to remove an item from a list given its index instead
of its value: the "del" statement.  This differs from the "pop()"
method which returns a value.  The "del" statement can also be used to
remove slices from a list or clear the entire list (which we did
earlier by assignment of an empty list to the slice).  For example:

**Required filter:** `None`

#### Rank 1

- Chunk: `python_datastructures_p007_paragraph_009`
- Source: `datastructures.txt`
- Page: `7`
- Section: `datastructures`
- Distance: `0.7443`

```text
   ['guido', 'irv', 'jack']
   >>> 'guido' in tel
   True
   >>> 'jack' not in tel
   False


```

#### Rank 2

- Chunk: `python_datastructures_p007_paragraph_008`
- Source: `datastructures.txt`
- Page: `7`
- Section: `datastructures`
- Distance: `0.7576`

```text
   >>> tel = {'jack': 4098, 'sape': 4139}
   >>> tel['guido'] = 4127
   >>> tel
   {'jack': 4098, 'sape': 4139, 'guido': 4127}
   >>> tel['jack']
   4098
   >>> tel['irv']
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   KeyError: 'irv'
   >>> print(tel.get('irv'))
   None
   >>> del tel['sape']
   >>> tel['irv'] = 4127
   >>> tel
   {'jack': 4098, 'guido': 4127, 'irv': 4127}
   >>> list(tel)
   ['jack', 'guido', 'irv']
   >>> sorted(tel)

```

#### Rank 3

- Chunk: `python_datastructures_p001_paragraph_007`
- Source: `datastructures.txt`
- Page: `1`
- Section: `datastructures`
- Distance: `0.7886`

```text
   >>> fruits.sort()
   >>> fruits
   ['apple', 'apple', 'banana', 'banana', 'grape', 'kiwi', 'orange', 'pear']
   >>> fruits.pop()
   'pear'


```

---

### T03: Module datetime có hỗ trợ đối tượng nhận biết múi giờ không?

**Expected answer:** Có, datetime hỗ trợ đối tượng timezone-aware.

**Gold evidence:**

> The "datetime" module supplies classes for manipulating dates and
times in both simple and complex ways. While date and time arithmetic
is supported, the focus of the implementation is on efficient member
extraction for output formatting and manipulation.  The module also
supports objects that are timezone aware.

   >>> # dates are easil

**Required filter:** `None`

#### Rank 1

- Chunk: `python_stdlib_p003_paragraph_001`
- Source: `stdlib.txt`
- Page: `3`
- Section: `stdlib`
- Distance: `0.5394`

```text
The "datetime" module supplies classes for manipulating dates and
times in both simple and complex ways. While date and time arithmetic
is supported, the focus of the implementation is on efficient member
extraction for output formatting and manipulation.  The module also
supports objects that are timezone aware.


```

#### Rank 2

- Chunk: `python_stdlib_p003_paragraph_002`
- Source: `stdlib.txt`
- Page: `3`
- Section: `stdlib`
- Distance: `0.6688`

```text
   >>> # dates are easily constructed and formatted
   >>> import datetime as dt
   >>> now = dt.date.today()
   >>> now
   datetime.date(2003, 12, 2)
   >>> now.strftime("%m-%d-%y. %d %b %Y is a %A on the %d day of %B.")
   '12-02-03. 02 Dec 2003 is a Tuesday on the 02 day of December.'

   >>> # dates support calendar arithmetic
   >>> birthday = dt.date(1964, 7, 31)
   >>> age = now - birthday
   >>> age.days
   14368

10.9. Data compression
======================


```

#### Rank 3

- Chunk: `python_modules_p001_paragraph_001`
- Source: `modules.txt`
- Page: `1`
- Section: `modules`
- Distance: `0.7016`

```text
6. Modules
**********


```

---

### T04: Trong interactive shell mới, phím F3 dùng để làm gì?

**Expected answer:** F3 bật paste mode và nhấn lại để trở về prompt thường.

**Gold evidence:**

> "F3"
enters "paste mode", which makes pasting larger blocks of code easier.
Press "F3" to return to the regular prompt.

When using the new interactive shell, exit the shell by typing "exit"
or "quit". Adding call parentheses after those commands is not
required.

If the new interactive shell is not desired, it can be disabled via
the "PY

**Required filter:** `None`

#### Rank 1

- Chunk: `python_interactive_p001_paragraph_005`
- Source: `interactive.txt`
- Page: `1`
- Section: `interactive`
- Distance: `0.6980`

```text
14.2. Alternatives to the Interactive Interpreter
=================================================


```

#### Rank 2

- Chunk: `python_index_p002_paragraph_008`
- Source: `index.txt`
- Page: `2`
- Section: `index`
- Distance: `0.7447`

```text
  * 11.8. Decimal floating-point arithmetic

* 12. Virtual Environments and Packages

  * 12.1. Introduction

  * 12.2. Creating Virtual Environments

  * 12.3. Managing Packages with pip

* 13. What Now?

* 14. Interactive Input Editing and History Substitution

  * 14.1. Tab Completion and History Editing

  * 14.2. Alternatives to the Interactive Interpreter

* 15. Floating-Point Arithmetic:  Issues and Limitations

  * 15.1. Representation Error

* 16. Appendix

  * 16.1. Interactive Mode


```

#### Rank 3

- Chunk: `python_interactive_p001_paragraph_007`
- Source: `interactive.txt`
- Page: `1`
- Section: `interactive`
- Distance: `0.7551`

```text
One alternative enhanced interactive interpreter that has been around
for quite some time is IPython, which features tab completion, object
exploration and advanced history management.  It can also be
thoroughly customized and embedded into other applications.  Another
similar enhanced interactive environment is bpython.
```

---

### T05: Theo tài liệu, threading giúp ứng dụng phản hồi người dùng tốt hơn như thế nào?

**Expected answer:** Cho phép tác vụ chạy nền trong khi ứng dụng vẫn nhận đầu vào và tiếp tục công việc khác.

**Gold evidence:**

> Threading is a technique for decoupling tasks which are not
sequentially dependent.  Threads can be used to improve the
responsiveness of applications that accept user input while other
tasks run in the background.  A related use case is running I/O in
parallel with computations in another thread.

The following code shows how the high le

**Required filter:** `{'section': 'stdlib2'}`

#### Rank 1

- Chunk: `python_stdlib2_p001_paragraph_008`
- Source: `stdlib2.txt`
- Page: `1`
- Section: `stdlib2`
- Distance: `0.8214`

```text
   >>> from string import Template
   >>> t = Template('${village}folk send $$10 to $cause.')
   >>> t.substitute(village='Nottingham', cause='the ditch fund')
   'Nottinghamfolk send $10 to the ditch fund.'


```

#### Rank 2

- Chunk: `python_stdlib2_p002_paragraph_008`
- Source: `stdlib2.txt`
- Page: `2`
- Section: `stdlib2`
- Distance: `0.8420`

```text
       start += extra_size + comp_size     # skip to the next header

11.4. Multi-threading
=====================


```

#### Rank 3

- Chunk: `python_stdlib2_p003_paragraph_001`
- Source: `stdlib2.txt`
- Page: `3`
- Section: `stdlib2`
- Distance: `0.8618`

```text
Threading is a technique for decoupling tasks which are not
sequentially dependent.  Threads can be used to improve the
responsiveness of applications that accept user input while other
tasks run in the background.  A related use case is running I/O in
parallel with computations in another thread.

The following code shows how the high level "threading" module can run
tasks in background while the main program continues to run:

   import threading, zipfile


```

---

