def test_simple_var(assert_equal):
    assert_equal('{{ foo }}', '{{ foo }}')


def test_var_filter(assert_equal):
    assert_equal('{{ foo|lower }}', '{{ foo|lower }}')


def test_var_filter_with_args(assert_equal):
    assert_equal('{{ foo|join:", " }}', '{{ foo|join(\', \') }}')


def test_multiple_filters(assert_equal):
    assert_equal('{{ foo|lower|upper }}', '{{ foo|lower|upper }}')


def test_multiple_filters_with_args(assert_equal):
    assert_equal('{{ foo|join:", "|upper }}', '{{ foo|join(\', \')|upper }}')
