"""Iterator library"""

import builtins
import functools
import itertools

# TYPES {{{
from typing import Any, Callable, Container, Iterable, Iterator, Optional, Tuple

from funpy import fn, op

# }}}
# INITS {{{
slice = itertools.islice
# }}}
# MAPPING {{{
map = builtins.map

starmap = itertools.starmap

enumerate = builtins.enumerate

accumulate = itertools.accumulate


def mapcat(f: Callable, *ls: Iterable) -> Iterator:
    """Apply f on ls and concat it.

    >>> list(mapcat(lambda a, b: (a, b), (0, 1, 2), (3, 4, 5)))
    [0, 3, 1, 4, 2, 5]
    """
    return itertools.chain.from_iterable(map(f, *ls))


def mapevery(f: Callable, n: int, *ls: Iterable) -> Iterator:
    """Apply f on every n value of l.

    >>> list(mapevery(pow, 2, (0, 1, 2, 3), (4, 5, 6, 7)))
    [0, (1, 5), 64, (3, 7)]
    """
    assert n > 0, "n must be greater than 0"

    for i, x in enumerate(zip(*ls)):
        if i % n == 0:
            yield f(*x)
        else:
            yield tuple(x)


def replace(l: Iterable, m: dict, d: Any = None) -> Iterator:
    """Map l item with l or yield d.

    >>> mapping = {'a': 1, 'b': 2}
    >>> list(replace(('a',  'b', 'c', 'b', 'd'), mapping))
    [1, 2, None, 2, None]
    """
    for x in l:
        yield m.get(x, d)


# }}}
# ORDERING {{{
sorted = builtins.sorted

reversed = builtins.reversed
# }}}
# GROUPING {{{
groupby = itertools.groupby


def slide(l: Iterable, n: int) -> Iterator[tuple]:
    """Create slides of size n from l.

    >>> list(slide(range(5), 3))
    [(0, 1, 2), (1, 2, 3), (2, 3, 4)]
    >>> list(slide(range(2), 3))
    []
    """

    def window(x):
        i, slided = x

        return drop(slided, i)

    slides = tee(l, n)
    windows = map(window, enumerate(slides))

    return zip(*windows)


def split(l: Iterable, n: int) -> Tuple[Iterator, Iterator]:
    """Split l based on n.

    >>> list(map(list, split(range(5), 2)))
    [[0, 1], [2, 3, 4]]
    >>> list(map(list, split(range(1), 2)))
    [[0], []]
    """
    left, right = tee(l)

    return take(left, n), drop(right, n)


def splitby(l: Iterable, p: fn.Predicate = bool) -> Tuple[Iterator, Iterator]:
    """Split l based on p.

    >>> list(map(list, splitby(range(5), op.iseven)))
    [[1, 3], [0, 2, 4]]
    >>> list(map(list, splitby(range(1), op.iseven)))
    [[], [0]]
    """
    left, right = tee(l)

    return remove(p, left), filter(p, right)


def chunk(l: Iterable, n: int) -> Iterator[tuple]:
    """Create chunks of size n from l.

    >>> list(map(list, chunk(range(8), 3)))
    [[0, 1, 2], [3, 4, 5]]
    >>> list(map(list, chunk(range(2), 3)))
    []
    """
    assert n > 0, "n must be greater than 0"

    chunking: list = []

    for i, x in enumerate(l, 1):
        chunking.append(x)

        if i % n == 0:
            yield tuple(chunking)
            chunking.clear()


def chunkby(l: Iterable, p: fn.Predicate = bool) -> Iterator[tuple]:
    """Create chunks from n based on consecutive value of p.

    >>> list(map(list, chunkby((0, 2, 1, 3, 0, 1), op.iseven)))
    [[0, 2], [1, 3], [0], [1]]
    """
    for _, items in groupby(l, p):
        yield tuple(items)


def chunkall(l: Iterable, n: int) -> Iterator[tuple]:
    """Create chunks of size n at least from l.

    >>> list(map(list, chunkall(range(2), 3)))
    [[0, 1]]
    >>> list(map(list, chunkall(range(8), 3)))
    [[0, 1, 2], [3, 4, 5], [6, 7]]
    >>> list(map(list, chunkall(range(9), 3)))
    [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
    """
    assert n > 0, "n must be greater than 0"

    chunking: list = []

    for i, x in enumerate(l, 1):
        chunking.append(x)

        if i % n == 0:
            yield tuple(chunking)
            chunking.clear()

    if op.notempty(chunking):
        yield tuple(chunking)


def grouped(l: Iterable, f: Callable = fn.ident) -> Iterator[Tuple[Any, tuple]]:
    """Group items of l based on f.

    >>> list(grouped((1, 2, 3, 1, 2, 3, 1, 2)))
    [(1, (1, 1, 1)), (2, (2, 2, 2)), (3, (3, 3))]
    >>> list(grouped(({'a': 1}, {'a': 2}, {'a': 1}), op.getit('a')))
    [(1, ({'a': 1}, {'a': 1})), (2, ({'a': 2},))]
    """
    index: dict = {}

    for x in l:
        k = f(x)

        index.setdefault(k, [])
        index[k].append(x)

    for k, vs in index.items():
        yield k, tuple(vs)


def groupkv(l: Iterable):
    """Group key value items of l based on key.

    >>> list(groupkv(((0, 0), (1, 1), (0, 2), (1, 3))))
    [(0, (0, 2)), (1, (1, 3))]
    """
    index: dict = {}

    for k, v in l:
        index.setdefault(k, [])
        index[k].append(v)

    for k, vs in index.items():
        yield k, tuple(vs)


# }}}
# FILTERING {{{
filter = builtins.filter
remove = itertools.filterfalse

compress = itertools.compress

dropwhile = itertools.dropwhile
takewhile = itertools.takewhile


def member(l: Iterable, s: Container) -> Iterator:
    """Return item from l member of s.

    >>> list(member(range(5), {5, 7}))
    []
    >>> list(member(range(5), {1, 3, 5, 7}))
    [1, 3]
    """
    for x in l:
        if x in s:
            yield x


def locate(l: Iterable, p: fn.Predicate = bool):
    """Return l index when p is True.

    >>> list(locate(range(5), lambda x: x % 2 == 0))
    [0, 2, 4]
    """
    for i, x in enumerate(l):
        if p(x):
            yield i


def dedupe(l: Iterable, f: Callable = fn.ident) -> Iterator:
    """Remove consecutive items from l based on f.

    >>> list(dedupe((0, 0, 2, 1, 1, 3)))
    [0, 2, 1, 3]
    >>> list(dedupe((0, 0, 2, 1, 1, 3), op.iseven))
    [0, 1]
    """
    lasty = None

    for x in l:
        y = f(x)

        if y != lasty:
            lasty = y
            yield x


def distinct(l: Iterable, f: Callable = fn.ident) -> Iterator:
    """Return distinct items from l based on f.

    >>> list(distinct((0, 0, 2, 1, 1, 3)))
    [0, 2, 1, 3]
    >>> list(distinct((0, 0, 2, 1, 1, 3), op.iseven))
    [0, 1]
    """
    seen: set = set()

    for x in l:
        y = f(x)

        if y not in seen:
            seen.add(y)
            yield x


# }}}
# REDUCTIONS {{{
all = builtins.all
any = builtins.any

max = builtins.max
min = builtins.min
sum = builtins.sum

reduce = functools.reduce


def len(l: Iterable) -> int:
    """Return the length of l.

    >>> len(range(5))
    5
    """
    i = None

    for i, _ in enumerate(l, 1):
        pass

    return i


def mult(l: Iterable, start: Any = 1) -> Any:
    """Return the product of l.

    >>> mult(range(1, 5))
    24
    >>> mult(range(1, 5), 10)
    240
    """
    return reduce(op.mul, l, start)


def contains(l: Iterable, x: Any) -> bool:
    """Return True if l contains x.

    >>> contains(range(9), 3)
    True
    >>> contains(range(2), 3)
    False
    """
    return any(x == z for z in l)


def quantify(l: Iterable, p: fn.Predicate = bool) -> int:
    """Count how many times p is True.

    >>> quantify(range(9), lambda x: x % 2 == 0)
    5
    >>> quantify(range(9), lambda x: x % 2 == 1)
    4
    """
    return sum(map(p, l))


def consume(l: Iterable) -> None:
    """Consume an iterable.

    >>> consume(range(10)) is None
    True
    >>> consume(range(0)) is None
    True
    """
    for _ in l:
        pass


# }}}
# SELECTIONS {{{
def nth(l: Iterable, n: int, d: Any = None) -> Optional[Any]:
    """Return the nth item of l or d.

    >>> nth(range(5), 3)
    3
    >>> nth(range(5), 9) is None
    True
    >>> nth(range(5), 9, False)
    False
    """
    assert n >= 0, "n must be greater or equals to 0"

    for i, x in enumerate(l):
        if i == n:
            return x

    return d


def first(l: Iterable, d: Any = None) -> Optional[Any]:
    """Return the first item of l or d.

    >>> first(range(1, 5))
    1
    >>> first(range(0)) is None
    True
    """
    return nth(l, 0, d=d)


def second(l: Iterable, d: Any = None) -> Optional[Any]:
    """Return the second item of l or d.

    >>> second(range(1, 5))
    2
    >>> second(range(0)) is None
    True
    """
    return nth(l, 1, d=d)


def third(l: Iterable, d: Any = None) -> Optional[Any]:
    """Return the third item of l or d.

    >>> third(range(1, 5))
    3
    >>> third(range(0)) is None
    True
    """
    return nth(l, 2, d=d)


def last(it: Iterable, d: Any = None) -> Optional[Any]:
    """Return the last item of l or d.

    >>> last(range(1, 5))
    4
    >>> last(range(0)) is None
    True
    """
    x = None

    for x in it:
        pass

    try:
        return x
    except UnboundLocalError:
        return d


def butlast(l: Iterable) -> Iterator:
    """Return all but the last item of l.

    >>> list(butlast(range(0)))
    []
    >>> list(butlast(range(5)))
    [0, 1, 2, 3]
    """
    left, right = tee(l)
    right = rest(right)

    for a, _ in zip(left, right):
        yield a


def sub(l: Iterable, start: int, stop: int) -> Iterator:
    """Return item ranging from start to stop in l.

    >>> list(sub(range(5), 3, 6))
    [3, 4]
    >>> list(sub(range(9), 3, 6))
    [3, 4, 5]
    """
    return slice(l, start, stop)


def rest(l: Iterable) -> Iterator:
    """Skip the first item of l.

    >>> list(rest(range(0)))
    []
    >>> list(rest(range(5)))
    [1, 2, 3, 4]
    """
    return slice(l, 1, None)


def take(l: Iterable, n: int) -> Iterator:
    """Return the first n item of l.

    >>> list(take(range(1), 5))
    [0]
    >>> list(take(range(9), 5))
    [0, 1, 2, 3, 4]
    """
    return slice(l, n)


def takenth(l: Iterable, n: int, start: int = 0, end: int = None) -> Iterator:
    """Return every n item of l.

    >>> list(takenth(range(1), 2))
    [0]
    >>> list(takenth(range(9), 2))
    [0, 2, 4, 6, 8]
    """
    return slice(l, start, end, n)


def takelast(l: Iterable, n: int) -> Iterator:
    """Return the last n item of l.

    >>> list(takelast(range(2), 3))
    []
    >>> list(takelast(range(9), 3))
    [6, 7, 8]
    """
    sl: tuple = tuple()

    for sl in slide(l, n):
        pass

    for x in sl:
        yield x


def drop(l: Iterable, n: int) -> Iterator:
    """Drop the first n item of l.

    >>> list(drop(range(3), 5))
    []
    >>> list(drop(range(9), 5))
    [5, 6, 7, 8]
    """
    return slice(l, n, None)


def dropnth(l: Iterable, n: int) -> Iterator:
    """Drop every n item of l.

    >>> list(dropnth(range(1), 2))
    [0]
    >>> list(dropnth(range(9), 2))
    [0, 2, 4, 6, 8]
    """
    assert n > 0, "n must be greater than 0"

    for i, x in enumerate(l, 1):
        if i % n != 0:
            yield x


def droplast(l: Iterable, n: int) -> Iterator:
    """Return the last n item of l.

    >>> list(droplast(range(2), 3))
    []
    >>> list(droplast(range(9), 3))
    [0, 1, 2, 3, 4, 5]
    """
    left, right = tee(l)
    right = butlast(slide(right, n))

    for a, _ in zip(left, right):
        yield a


def find(l: Iterable, p: fn.Predicate = bool, d: Any = None) -> Optional[Any]:
    """Return the first item where p is True or d.

    >>> find(range(3), lambda x: x > 5) is None
    True
    >>> find(range(9), lambda x: x > 5)
    6
    """
    for x in l:
        if p(x):
            return x

    return d


# }}}
# CONSTRUCTIONS {{{
tee = itertools.tee

range = builtins.range
count = itertools.count

cycle = itertools.cycle
repeat = itertools.repeat

cat = itertools.chain
concat = itertools.chain.from_iterable

zip = builtins.zip
transpose = builtins.zip
ziplong = itertools.zip_longest


def pad(l: Iterable, d: Any = None) -> Iterator:
    """Yield items from l then always yield d.

    >>> list(slice(pad(range(3)), 5))
    [0, 1, 2, None, None]
    >>> list(slice(pad(range(3), 0), 5))
    [0, 1, 2, 0, 0]
    """
    return cat(l, repeat(d))


def cons(l: Iterable, x: Any) -> Iterator:
    """Prepend x to l.

    >>> list(cons(range(1, 3), 0))
    [0, 1, 2]
    """
    yield x
    yield from l


def conj(l: Iterable, x: Any) -> Iterator:
    """Append x to l.

    >>> list(conj(range(1, 3), 0))
    [1, 2, 0]
    """
    yield from l
    yield x


def iterate(f: Callable, x: Any) -> Iterator:
    """Call f on x and update x.

    >>> list(slice(iterate(op.inc, 0), 3))
    [0, 1, 2]
    """
    while True:
        yield x
        x = f(x)


def iterwith(x: Any) -> Iterator:
    """Yield from x in a context."""
    with x:
        yield from x


def tabulate(f: Callable, start: int = 0, step: int = 1) -> Iterator:
    """Apply f on every natural numbers.

    >>> list(slice(tabulate(str), 5))
    ['0', '1', '2', '3', '4']
    >>> list(slice(tabulate(str, 2, 2), 5))
    ['2', '4', '6', '8', '10']
    """
    yield from map(f, count(start, step))


def interleave(*ls: Iterable) -> Iterator:
    """Yield item from each iterator successively.

    >>> list(interleave(range(3), range(3, 6)))
    [0, 3, 1, 4, 2, 5]
    >>> list(interleave(range(3), range(3, 7)))
    [0, 3, 1, 4, 2, 5]
    """
    return concat(zip(*ls))


def interchange(*ls: Iterable, x: Any = None) -> Iterator:
    """Yield item from each iterator successively or fill with x.

    >>> list(interchange(range(3), range(3, 6)))
    [0, 3, 1, 4, 2, 5]
    >>> list(interchange(range(3), range(3, 7)))
    [0, 3, 1, 4, 2, 5, None, 6]
    """
    return concat(ziplong(*ls, fillvalue=x))


def interpose(l: Iterable, x: Any) -> Iterator:
    """Yield item from l alternating with x.

    >>> list(interpose(range(1, 4), 0))
    [1, 0, 2, 0, 3]
    """
    return drop(interleave(repeat(x), l), 1)


# }}}
# COMBINATORICS {{{
product = itertools.product
permutated = itertools.permutations
permutations = itertools.permutations
combinations = itertools.combinations
combinatoric = itertools.combinations_with_replacement
# }}}
