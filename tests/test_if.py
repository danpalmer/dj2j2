def test_simple_if(assert_equal):
    assert_equal('{% if foo %}{% endif %}', '{% if foo %}{% endif %}')

def test_simple_if_else(assert_equal):
    assert_equal(
        '{% if foo %}{% else %}{% endif %}',
        '{% if foo %}{% else %}{% endif %}',
    )

def test_if_subnodes(assert_equal):
    assert_equal('{% if foo %}bar{% endif %}', '{% if foo %}bar{% endif %}')

def test_if_else_subnodes(assert_equal):
    assert_equal(
        '{% if foo %}1{% else %}2{% endif %}',
        '{% if foo %}1{% else %}2{% endif %}',
    )

def test_if_filters(assert_equal):
    assert_equal(
        '{% if foo|lower %}{% endif %}',
        '{% if foo|lower %}{% endif %}',
    )

def test_if_filters_with_args(assert_equal):
    assert_equal(
        '{% if foo|join:", " %}{% endif %}',
        '{% if foo|join(\', \') %}{% endif %}',
    )

def test_if_elif(assert_equal):
    assert_equal(
        '{% if foo %}{% elif bar %}{% endif %}',
        '{% if foo %}{% elif bar %}{% endif %}',
    )

def test_if_elif_filters(assert_equal):
    assert_equal(
        '{% if foo %}{% elif bar|lower %}{% endif %}',
        '{% if foo %}{% elif bar|lower %}{% endif %}',
    )

def test_if_elif_filters_with_args(assert_equal):
    assert_equal(
        '{% if foo %}{% elif bar|join:", " %}{% endif %}',
        '{% if foo %}{% elif bar|join(\', \') %}{% endif %}',
    )

def test_if_multiple_elif(assert_equal):
    assert_equal(
        '{% if foo %}{% elif bar %}{% elif baz %}{% endif %}',
        '{% if foo %}{% elif bar %}{% elif baz %}{% endif %}',
    )

def test_if_elif_else(assert_equal):
    assert_equal(
        '{% if foo %}{% elif bar %}{% else %}{% endif %}',
        '{% if foo %}{% elif bar %}{% else %}{% endif %}',
    )
