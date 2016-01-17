from collections import namedtuple

from django.template import base as tokens

from dj2j2.transpile import render_django_token

Token = namedtuple('Token', ('contents', 'token_type'))

def test_render_var():
    token = Token('foo', tokens.TOKEN_VAR)
    assert render_django_token(token) == '{{ foo }}'

def test_render_block():
    token = Token('foo', tokens.TOKEN_BLOCK)
    assert render_django_token(token) == '{% foo %}'

def test_render_comment():
    token = Token('foo', tokens.TOKEN_COMMENT)
    assert render_django_token(token) == '{# foo #}'

def test_render_text():
    token = Token('foo', tokens.TOKEN_TEXT)
    assert render_django_token(token) == 'foo'
