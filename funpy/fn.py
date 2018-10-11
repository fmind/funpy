"""Function library."""

import copy as Copy
import functools

# TYPES {{{
from typing import Callable, Iterable, TypeVar, Union

Predicate = Callable[..., bool]

X = TypeVar("X")
Y = TypeVar("Y")
Z = TypeVar("Z")

# }}}
# COPIERS {{{
def copy(x: X, deep: bool = False) -> X:
    """Return a copy of x.

    >>> a = [1, 2, 3]
    >>> a == copy(a, True)
    True
    >>> a == copy(a, False)
    True
    """
    return Copy.deepcopy(x) if deep else Copy.copy(x)


def copies(x: X, n: int = 2, deep: bool = False) -> Iterable[X]:
    """Return n copy of x.

    >>> a = [1, 2, 3]
    >>> b, c = copies(a)
    >>> a == b == c
    True
    """
    assert n > 0, "n must be greater than 0"

    for _ in range(n):
        yield copy(x, deep)


# }}}
# WRAPPERS {{{
wraps = functools.wraps

partial = functools.partial

partialme = functools.partialmethod


def flip(f: Callable[..., Y]) -> Callable[..., Y]:
    """"Flip f arguments.

    >>> flip(print)(1, 2, 3, sep=',')
    3,2,1
    """

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        return f(*reversed(args), **kwargs)

    return wrapped


def partialfp(f: Callable[..., Y], *args, **kwargs) -> Callable[..., Y]:
    """Flip and partial f.

    >>> partialfp(print, 0, 1, sep=',')(2, 3)
    3,2,1,0
    """
    return partial(flip(f), *args, **kwargs)


# }}}
# LOW-ORDER {{{
def ident(x: X) -> X:
    """Return x unchanged.

    >>> ident(0) is 0
    True
    >>> ident(1) is 1
    True
    >>> ident(None) is None
    True
    """
    return x


def constantly(x: X) -> Callable[..., X]:
    """Constantly returns x through a function.

    >>> constantly(0)(1, 2, x=3)
    0
    """

    def constant(*_, **__):
        return x

    return constant


# }}}
# HIGH-ORDER {{{
def compose(f: Callable[[Z], Y], g: Callable[..., Z]) -> Callable[..., Y]:
    """Compose two functions left to right.

    >>> compose(range, list)(3)
    [0, 1, 2]
    """

    def composed(*args, **kwargs):
        return g(f(*args, **kwargs))

    return composed


def comp(*fs: Callable) -> Callable:
    """Compose functions from left to right.

    >>> comp()(2)
    2
    >>> comp(float)(2)
    2.0
    >>> comp(range, list)(2)
    [0, 1]
    >>> comp(range, list, len)(2)
    2
    """
    if not fs:
        return ident

    return functools.reduce(compose, fs)


def juxt(*fs: Callable) -> Callable[..., tuple]:
    """Juxtapose functions results.

    >>> juxt()(2)
    (2,)
    >>> juxt(float)(2)
    (2.0,)
    >>> juxt(float, str)(2)
    (2.0, '2')
    >>> juxt(float, str, bin)(2)
    (2.0, '2', '0b10')
    """
    if not fs:
        fs = (ident,)

    def juxted(*args, **kwargs):
        return tuple(f(*args, **kwargs) for f in fs)

    return juxted


# }}}
# DECORATORS {{{
memoize = functools.lru_cache

comparator = functools.cmp_to_key

totalordering = functools.total_ordering

singledispatch = functools.singledispatch


def pre(
    f: Callable[..., Y], do: Callable[[tuple, dict], None] = print
) -> Callable[..., Y]:
    """Call do before f (decorator).

    >>> pre(float)(2)
    (2,) {}
    2.0
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        do(args, kwargs)

        return f(*args, **kwargs)

    return wrapped


def post(
    f: Callable[..., Y], do: Callable[[tuple, dict, Y], None] = print
) -> Callable[..., Y]:
    """Call do after f (decorator).

    >>> post(float)(2)
    (2,) {} 2.0
    2.0
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        res = f(*args, **kwargs)

        do(args, kwargs, res)

        return res

    return wrapped


def fnil(f: Callable[..., Y], x: X) -> Callable[..., Y]:
    """Replace the first argument of f by x if None.

    >>> fnil(pow, 5)(2, 3)
    8
    >>> fnil(pow, 5)(None, 3)
    125
    """

    @wraps(f)
    def wrapped(z: X, *args, **kwargs):
        return f(x if z is None else z, *args, **kwargs)

    return wrapped


def safe(f: Callable[..., Y], x: Z = None) -> Callable[..., Union[Y, Z]]:
    """Return x if f throws an exception (decorator).

    >>> safe(abs)(2) == 2
    True
    >>> safe(abs)('a') is None
    True
    >>> safe(abs, 2)('a') == 2
    True
    """

    @wraps(f)
    def wrapped(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            return x

    return wrapped


def pure(f: Callable[..., None], deep: bool = False) -> Callable:
    """Purify the side effect of f (decorator).
    >>> l, append = [], pure(list.append)
    >>> append(append(append(l, 0), 1), 2)
    [0, 1, 2]
    >>> l
    []
    """

    @wraps(f)
    def wrapped(x, *args, **kwargs):
        x = copy(x, deep=deep)

        f(x, *args, **kwargs)

        return x

    return wrapped


def fluent(f: Callable[..., None]) -> Callable:
    """Grant a fluent interface to f (decorator).
    >>> l, append = [], fluent(list.append)
    >>> append(append(append(l, 0), 1), 2)
    [0, 1, 2]
    >>> l
    [0, 1, 2]
    """

    @wraps(f)
    def wrapped(x, *args, **kwargs):
        f(x, *args, **kwargs)

        return x

    return wrapped


def complement(p: Predicate) -> Predicate:
    """Reverse the logic of p (decorator).

    >>> complement(bool)(True)
    False
    >>> complement(bool)(False)
    True
    """

    @wraps(p)
    def wrapped(*args, **kwargs):
        return not p(*args, **kwargs)

    return wrapped


# }}}
