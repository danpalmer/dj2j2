from django import setup
from django.conf import settings

import django.template.base
from django.template import defaulttags
from django.template.base import Node, TextNode

from .transpile import render_django_token


def configure_django():
    if configure_django._run:
        return

    settings.configure(
        INSTALLED_APPS=[
            'django.contrib.humanize',
        ],
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [],
                'APP_DIRS': True,
                'OPTIONS': {
                },
            },
        ],
    )

    setup()

    configure_django._run = True

    patch_django_templates()


configure_django._run = False


def patch_django_templates():
    # Note: must be done after import as we rely on the original values
    # elsewhere.

    # We need to patch the CommentNode and tag to capture more context so we
    # can transpile comments without losing the text. There are 2 forms of
    # comments: blocks and the {##} comment syntax.

    # To handle comment blocks, we patch the comment tag and node to capture
    # the nodelist so that we can render it back out again.

    class CommentNode(Node):
        def __init__(self, nodelist):
            self.nodelist = nodelist

    @defaulttags.register.tag
    def comment(parser, token):
        nodelist = []

        # Manually consume tokens until we reach encomment. This roughly
        # follows the process in `Parser.parse()`, however treats everything
        # as a TextNode so that we don't accidentally check the syntax of
        # comments as templates.
        while parser.tokens:
            token = parser.next_token()
            command = token.contents.split()[0]
            if command == 'endcomment':
                break

            node = TextNode(render_django_token(token))
            parser.extend_nodelist(nodelist, node, token)

        return CommentNode(nodelist)

    # To capture the special comment syntax, we patch the translator comment
    # mark so that it matches all strings to ensure that Django will capture
    # the contents for us.

    django.template.base.TRANSLATOR_COMMENT_MARK = '#'

    # We then patch the identifier for comment tokens to be that of text tokens
    # so that they are handled in the same way as text.

    # We do this by patching with an object that equals the value of the text
    # token, but that will have a different hash and therefore will fail an
    # 'is' check. This allows us to differentiate between the two when
    # rendering in `dj2j2.transpile.render_django_token`.

    class TokenComment(object):
        def __eq__(self, obj):
            return obj == 0 # TOKEN_TEXT value

        def __hash__(self):
            return hash(repr(self))

    django.template.base.TOKEN_COMMENT = TokenComment()
