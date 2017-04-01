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
