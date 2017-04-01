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


def test_forloop_parentloo(assert_equal):
    assert False
