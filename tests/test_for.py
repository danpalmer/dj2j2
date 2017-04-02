import pytest

from dj2j2.exceptions import CompilationError


def test_simple_for(assert_equal):
    assert_equal(
        '{% for x in y %}{% endfor %}',
        '{% for x in y %}{% endfor %}',
    )


def test_for_empty(assert_equal):
    assert_equal(
        '{% for x in y %}{% empty %}foo{% endfor %}',
        '{% for x in y %}{% else %}foo{% endfor %}',
    )


def test_for_empty_empty(assert_equal):
    assert_equal(
        '{% for x in y %}{% empty %}{% endfor %}',
        '{% for x in y %}{% endfor %}',
    )


def test_for_reversed(assert_equal):
    assert_equal(
        '{% for x in y reversed %}{% endfor %}',
        '{% for x in y|reverse %}{% endfor %}',
    )


def test_forloop_counter(assert_equal):
    assert_equal(
        '{% for x in y %}{{ forloop.counter }}{% endfor %}',
        '{% for x in y %}{{ loop.index }}{% endfor %}',
    )


def test_forloop_counter0(assert_equal):
    assert_equal(
        '{% for x in y %}{{ forloop.counter0 }}{% endfor %}',
        '{% for x in y %}{{ loop.index0 }}{% endfor %}',
    )


def test_forloop_revcounter(assert_equal):
    assert_equal(
        '{% for x in y %}{{ forloop.revcounter }}{% endfor %}',
        '{% for x in y %}{{ loop.revindex }}{% endfor %}',
    )


def test_forloop_revcounter0(assert_equal):
    assert_equal(
        '{% for x in y %}{{ forloop.revcounter0 }}{% endfor %}',
        '{% for x in y %}{{ loop.revindex0 }}{% endfor %}',
    )


def test_forloop_first(assert_equal):
    assert_equal(
        '{% for x in y %}{{ forloop.first }}{% endfor %}',
        '{% for x in y %}{{ loop.first }}{% endfor %}',
    )


def test_forloop_last(assert_equal):
    assert_equal(
        '{% for x in y %}{{ forloop.last }}{% endfor %}',
        '{% for x in y %}{{ loop.last }}{% endfor %}',
    )


def test_forloop_parentloop(transpile):
    _, report = transpile(
        '''
            {% for x in y %}
                {% for z in x %}
                    {{ forloop.parentloop.counter }}
                {% endfor %}
            {% endfor %}
        ''',
    )

    expected = (
        "Use of 'parentloop' can't be automatically migrated. The suggested "
        "workaround is to capture the parent loop as a variable in the "
        "enclosing scope with 'set'."
    )

    assert len(report.failed_files) == 1
    assert str(list(report.failed_files.values())[0]) == expected


def test_for_filter_exp(assert_equal):
    assert_equal(
        '{% for x in y|first %}{% endfor %}',
        '{% for x in y|first %}{% endfor %}',
    )
