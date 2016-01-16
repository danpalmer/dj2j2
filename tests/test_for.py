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
