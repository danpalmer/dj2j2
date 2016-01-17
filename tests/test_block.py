def test_block(assert_equal):
    assert_equal(
        '{% block foo %}{% endblock %}',
        '{% block foo %}{% endblock %}',
    )

def test_block_nodes(assert_equal):
    assert_equal(
        '{% block foo %}bar{% endblock %}',
        '{% block foo %}bar{% endblock %}',
    )

def test_block_super(assert_equal):
    assert_equal(
        '{% block foo %}{{ block.super }}{% endblock %}',
        '{% block foo %}{{ super() }}{% endblock %}',
    )
