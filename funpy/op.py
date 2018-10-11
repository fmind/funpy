"""Operator library."""


import builtins
import fractions
import math
import operator
import statistics

# TYPES {{{
from typing import Any, Container, Sized

# }}}
# NUMBERS {{{
abs = operator.abs

neg = operator.neg
pos = operator.pos

add = operator.add
sub = operator.sub

mul = operator.mul
matmul = operator.matmul

mod = operator.mod
div = fractions.Fraction

truediv = operator.truediv
floordiv = operator.floordiv


def dec(x: int) -> int:
    """Return x - 1.

    >>> dec(-1)
    -2
    >>> dec(0)
    -1
    >>> dec(1)
    0
    """
    return x - 1


def inc(x: int) -> int:
    """Return x + 1.

    >>> inc(-1)
    0
    >>> inc(0)
    1
    >>> inc(1)
    2
    """
    return x + 1


def isneg(x: int) -> bool:
    """Return True if x is negative.

    >>> isneg(-1)
    True
    >>> isneg(0)
    False
    >>> isneg(1)
    False
    """
    return x < 0


def iszero(x: int) -> bool:
    """Return True if x is zero.

    >>> iszero(-1)
    False
    >>> iszero(0)
    True
    >>> iszero(1)
    False
    """
    return x == 0


def ispos(x: int) -> bool:
    """Return True if x is positive.

    >>> ispos(-1)
    False
    >>> ispos(0)
    False
    >>> ispos(1)
    True
    """
    return x > 0


def isodd(x: int) -> bool:
    """Return True if x is odd.

    >>> isodd(2)
    False
    >>> isodd(3)
    True
    """
    return x % 2 == 1


def iseven(x: int) -> bool:
    """Return True if x is even.

    >>> iseven(2)
    True
    >>> iseven(3)
    False
    """
    return x % 2 == 0


# }}}
# OBJECTS {{{
hasat = builtins.hasattr

isa = builtins.isinstance
issub = builtins.issubclass

getat = operator.attrgetter
getit = operator.itemgetter
getme = operator.methodcaller


def issome(x: Any) -> bool:
    """Return True if x is not None.
    >>> issome(0)
    True
    >>> issome(1)
    True
    >>> issome(None)
    False
    """
    return x is not None


def isnone(x: Any) -> bool:
    """Return True if x is None.
    >>> isnone(0)
    False
    >>> isnone(1)
    False
    >>> isnone(None)
    True
    """
    return x is None


# }}}
# BOOLEANS {{{
is_ = operator.is_
not_ = operator.not_
isnot = operator.is_not
istrue = operator.truth

or_ = operator.or_
and_ = operator.and_


def isfalse(x: Any) -> bool:
    """Return True if x is false.

    >>> isfalse(0)
    True
    >>> isfalse(1)
    False
    >>> isfalse(None)
    True
    >>> isfalse(True)
    False
    >>> isfalse(False)
    True
    """
    return not istrue(x)


# }}}
# BITWISES {{{
inv = operator.inv
xor = operator.xor

lshift = operator.lshift
rshift = operator.rshift
# }}}
# SEQUENCES {{{
isin = operator.contains

count = operator.countOf
index = operator.indexOf

addseq = operator.concat


def notin(l: Container, x: Any) -> bool:
    """Return True if x is not in l.

    >>> notin({1, 2, 3}, 0)
    True
    >>> notin({1, 2, 3}, 1)
    False
    """
    return x not in l


def isempty(l: Sized) -> bool:
    """Return True if l is empty.

    >>> isempty([])
    True
    >>> isempty([0])
    False
    """
    return len(l) == 0


def notempty(l: Sized) -> bool:
    """Return True if l is not empty.

    >>> notempty([])
    False
    >>> notempty([0])
    True
    """
    return len(l) > 0


# }}}
# STATISTICS {{{
mode = statistics.mode
means = statistics.mean
median = statistics.median

stdev = statistics.stdev
variance = statistics.variance
# }}}
# MATHEMATICS {{{
e = math.e
pi = math.pi
tau = math.tau
nan = math.nan
inf = math.inf

sqrt = math.sqrt
pow = builtins.pow

exp = math.exp
log = math.log
log2 = math.log2
log10 = math.log10

cos = math.cos
sin = math.sin
tan = math.tan
hypot = math.hypot

gcd = math.gcd
ceil = math.ceil
floor = math.floor
round = builtins.round

degrees = math.degrees
radians = math.radians

isinf = math.isinf
isnan = math.isnan
isclose = math.isclose
isfinite = math.isfinite

factorial = math.factorial
# }}}
# COMPARATORS {{{
lt = operator.lt
le = operator.le
eq = operator.eq
ne = operator.ne
ge = operator.ge
gt = operator.gt
# }}}
