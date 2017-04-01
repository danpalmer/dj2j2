def test_comment(assert_equal):
    assert_equal(
        '{# hello #}',
        '{# hello #}',
    )


def test_comment_block(assert_equal):
    assert_equal(
        '{% comment %}Hello!{% endcomment %}',
        '{# Hello! #}',
    )


def test_comment_block_containing_syntax(assert_equal):
    # This comment block contains invalid template syntax, ensure we aren't
    # attempting to parse it.
    assert_equal(
        '{% comment %}{% include %}{% endcomment %}',
        '{# {% include %} #}',
    )


test_multiline_comment_block_input = """
{% comment %}
    Hello, world!
{% endcomment %}
"""

test_multiline_comment_block_output = """
{#
    Hello, world!
#}
"""


def test_multiline_comment_block(assert_equal):
    assert_equal(
        test_multiline_comment_block_input,
        test_multiline_comment_block_output,
    )
