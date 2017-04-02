import pytest

from dj2j2.exceptions import CompilationError


def test_indexing(transpile):
    with pytest.raises(CompilationError):
        _, report = transpile('{{ foo.7_days }}')
