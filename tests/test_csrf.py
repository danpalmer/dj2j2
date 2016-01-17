def test_csrf(assert_equal):
    assert_equal('{% csrf_token %}', '{{ csrf_input }}')
