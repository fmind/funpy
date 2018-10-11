"""Input/Output library."""

import fileinput
import glob as Glob
import pprint as Print
import textwrap

# TYPES {{{
from typing import AnyStr, Callable, Iterable, Iterator

Path = str
Mode = str
# }}}
# PATHS {{{
glob = Glob.glob

iglob = Glob.iglob
# }}}
# INPUTS {{{
combine = fileinput.input


def slurp(path: Path, mode: Mode = "r") -> AnyStr:
    """Slurp data from path."""
    with open(path, mode) as r:
        return r.read()


# }}}
# OUTPUTS {{{
pprint = Print.pprint


def spit(path: Path, s: AnyStr, mode: Mode = "w") -> None:
    """Spit data to path."""
    with open(path, mode) as w:
        w.write(s)


# }}}
# STREAMS {{{
def interact(
    f: Callable[[AnyStr], AnyStr], files: Iterable[Path] = None, mode: Mode = "r"
) -> Iterator[AnyStr]:
    """Apply f on all line in files."""
    return map(f, combine(files, mode=mode))


# }}}
# STRINGS {{{
wrap = textwrap.wrap

fill = textwrap.fill

indent = textwrap.indent

dedent = textwrap.dedent

shorten = textwrap.shorten


def unnl(l: Iterable[str]) -> Iterator[str]:
    """Remove new lines from l.

    >>> list(unnl([]))
    []
    >>> list(unnl(['hello\\n', '\\n', '', 'world']))
    ['hello', '', '', 'world']
    """
    return (x.rstrip("\n") for x in l)


def unbl(l: Iterable[str]) -> Iterator[str]:
    """Remove blank lines from l.

    >>> list(unbl([]))
    []
    >>> list(unbl(['hello\\n', '\\n', '', 'world']))
    ['hello\\n', '\\n', 'world']
    """
    return (x for x in l if x != "")


def words(s: str) -> Iterator[str]:
    """Return a list of words from s.

    >>> list(words(''))
    []
    >>> list(words('hello fp  world    !'))
    ['hello', 'fp', 'world', '!']
    """
    return (x for x in s.split(None))


def unwords(l: Iterable[str]) -> str:
    """Return joined words from l.

    >>> unwords([])
    ''
    >>> unwords(['hello', '', 'world'])
    'hello  world'
    """
    return " ".join(l)


def lines(s: str) -> Iterator[str]:
    """Return a list of lines from s.

    >>> list(lines(''))
    []
    >>> list(lines('hello\\r\\n\\nworld'))
    ['hello', '', 'world']
    """
    return (x for x in s.splitlines())


def unlines(l: Iterable[str]) -> str:
    """Return joined lines from l.

    >>> unlines([])
    ''
    >>> unlines(['hello', '', 'world'])
    'hello\\n\\nworld'
    """
    return "\n".join(l)


# }}}
