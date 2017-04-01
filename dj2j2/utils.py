import os
import errno

from django.template.base import Lexer, Origin, Parser, UNKNOWN_SOURCE
from django.template.engine import Engine


def ensure_dir_exists(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_all_standard_template_filters():
    """
    Emulate the process in Template.compile_nodelist() to get a parser that is
    loaded with the default filters and tags.
    """

    engine = Engine.get_default()
    lexer = Lexer('')
    tokens = lexer.tokenize()
    origin = Origin(UNKNOWN_SOURCE)
    parser = Parser(
        tokens,
        engine.template_libraries,
        engine.template_builtins,
        origin,
    )

    return parser.filters.keys()
