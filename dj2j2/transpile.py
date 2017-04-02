import re
import click

from django.template import base as tokens
from django.utils.safestring import SafeText


NODE_TYPE_HANDLERS = {}


def transpile_template(report, template):
    for node in template.nodelist:
        yield handle(report, node)


def handle(report, node):
    handler_fn = NODE_TYPE_HANDLERS[node.__class__.__name__]
    try:
        return ''.join(handler_fn(report, node))
    except Exception:
        click.echo("Failed in file:\n\t%s at line: %d\n\t%s" % (
            report.current_file,
            node.token.lineno,
            render_django_token(node.token),
        ))
        raise


def handler(node_type):
    def handle_decorator(fn):
        NODE_TYPE_HANDLERS[node_type] = fn
        return fn
    return handle_decorator


@handler('TextNode')
def handle_text_node(report, text_node):
    yield text_node.s


@handler('VariableNode')
def handle_variable_node(report, var_node):
    node_text = render_filter_exp(
        report,
        var_node.filter_expression,
    )

    yield '{{ %s }}' % node_text


@handler('IfNode')
def handle_if_node(report, if_node):
    for idx, (condition, nodelist) in enumerate(if_node.conditions_nodelists):
        if condition is None:
            yield '{% else %}'
        else:
            condition_text = render_condition(report, condition)

            yield '{%% %s %s %%}' % (
                'if' if idx == 0 else 'elif',
                condition_text,
            )

        for node in nodelist:
            yield handle(report, node)

    yield '{% endif %}'


def render_condition(report, condition):
    if not condition.value:
        if condition.second:
            # Condition is a boolean expression
            return '%s %s %s' % (
                render_condition(report, condition.first),
                condition.id,
                render_condition(report, condition.second),
            )
        else:
            return '%s %s' % (
                condition.id,
                render_condition(report, condition.first),
            )
    else:
        # Condition is a simple filter expression
        return render_filter_exp(report, condition.value)


@handler('ForNode')
def handle_for_node(report, for_node):
    yield '{%% for %s in %s%s %%}' % (
        ', '.join(for_node.loopvars),
        for_node.sequence,
        '|reverse' if for_node.is_reversed else '',
    )

    for node in for_node.nodelist_loop:
        yield handle(report, node)

    if len(for_node.nodelist_empty):
        yield '{% else %}'

        for node in for_node.nodelist_empty:
            yield handle(report, node)

    yield '{% endfor %}'


@handler('LoadNode')
def handle_load_node(report, load_node):
    libraries = load_node.token.split_contents()[1:]

    for library in libraries:
        report.add_required_library(library, load_node.token)

    yield '' # We must yield content


@handler('ExtendsNode')
def handle_extends_node(report, extends_node):
    extends = render_filter_exp(report, extends_node.parent_name)

    yield '{%% extends %s %%}' % extends

    for node in extends_node.nodelist:
        yield handle(report, node)


@handler('BlockNode')
def handle_block_node(report, block_node):
    yield '{%% block %s %%}' % block_node.name

    for node in block_node.nodelist:
        yield handle(report, node)

    yield '{% endblock %}'


@handler('CsrfTokenNode')
def handle_csrf_token_node(report, csrf_token_node):
    yield '{{ csrf_input }}'


@handler('URLNode')
def handle_url_node(report, url_node):
    report.add_required_global('url', url_node.token)

    url = render_filter_exp(report, url_node.view_name)

    args = ', '.join(render_filter_exp(report, x) for x in url_node.args)

    kwargs = ', '.join(
        '%s=%s' % (x, render_filter_exp(report, y))
        for x, y in sorted(url_node.kwargs.items())
    )

    # First yield the lead in...
    if url_node.asvar:
        yield '{%% set %s = ' % url_node.asvar
    else:
        yield '{{ '

    # ...then the actual url expression...
    if args:
        yield 'url(%s, %s)' % (url, args)
    elif kwargs:
        yield 'url(%s, %s)' % (url, kwargs)
    else:
        yield 'url(%s)' % url

    # ...and finally lead out
    if url_node.asvar:
        yield ' %}'
    else:
        yield ' }}'


@handler('WithNode')
def handle_with_node(report, with_node):
    report.add_required_extension('jinja2.ext.with_', with_node.token)

    yield '{%% with %s %%}' % render_extra_context(
        report,
        with_node.extra_context,
    )

    for node in with_node.nodelist:
        yield handle(report, node)

    yield '{% endwith %}'


@handler('IncludeNode')
def handle_include_node(report, include_node):
    extra_context = render_extra_context(report, include_node.extra_context)
    only_string = ' without context' if include_node.isolated_context else ''

    if extra_context:
        if only_string:
            # Only passing through a select context is supported in Django
            # but not in Jinja2
            report.add_invalid_include(include_node.token.lineno)

        yield '{%% with %s %%}' % extra_context

    yield '{%% include %s%s %%}' % (
        render_filter_exp(report, include_node.template),
        only_string,
    )

    if extra_context:
        yield '{% endwith %}'


@handler('CommentNode')
def handle_comment_node(report, comment_node):
    contents = ''.join(handle(report, node) for node in comment_node.nodelist)

    def is_whitespace(c):
        return re.match(r'\s', c) is not None

    leading_whitespace = '' if is_whitespace(contents[0]) else ' '
    trailing_whitespace = '' if is_whitespace(contents[-1]) else ' '

    yield '{{#{}{}{}#}}'.format(
        leading_whitespace,
        contents,
        trailing_whitespace,
    )


@handler('RegroupNode')
def handle_regroup_node(report, regroup_node):
    as_name = regroup_node.var_name
    group_by_exp = render_filter_exp(report, regroup_node.expression)
    group_by_exp = re.sub(r'^%s\.' % as_name, '', group_by_exp)

    yield '{%% set %s = %s|groupby(\'%s\') %%}' % (
        as_name,
        render_filter_exp(report, regroup_node.target),
        group_by_exp,
    )


@handler('NowNode')
def handle_now_node(report, now_node):
    report.set_requires_django_compat()

    if now_node.asvar:
        yield '{%% set %s = now(\'%s\') %%}' % (
            now_node.asvar,
            now_node.format_string,
        )
    else:
        yield '{{ now(\'%s\') }}' % now_node.format_string


VAR_SPECIAL_CASES = {
    'block.super': 'super()',
    'forloop.last': 'loop.last',
    'forloop.first': 'loop.first',
    'forloop.counter': 'loop.index',
    'forloop.counter0': 'loop.index0',
    'forloop.revcounter': 'loop.revindex',
    'forloop.revcounter0': 'loop.revindex0',
}


def render_filter_exp(report, filter_expression):
    return ''.join(_filter_expression(report, filter_expression))


def _filter_expression(report, filter_expression):
    if isinstance(filter_expression.var, SafeText):
        yield '\'%s\'' % filter_expression.var
    else:
        var = filter_expression.var.var
        var_components = var.split('.')
        first = VAR_SPECIAL_CASES.get(var_components[0], var_components[0])
        result = '.'.join([first] + var_components[1:])
        yield VAR_SPECIAL_CASES.get(result, result)

    for filter_, args in filter_expression.filters:
        if callable(filter_):
            yield '|%s' % filter_.__name__

        if args:
            args = args[0][1:] # Drop "False" initial arg
            yield '(%s)' % ', '.join('\'%s\'' % x for x in args)


def render_extra_context(report, extra_context):
    return ', '.join(
        '%s=%s' % (x, render_filter_exp(report, y))
        for x, y in sorted(extra_context.items())
    )


TOKEN_WRAPPERS = {
    tokens.TOKEN_VAR: (
        tokens.VARIABLE_TAG_START,
        tokens.VARIABLE_TAG_END,
    ),
    tokens.TOKEN_BLOCK: (
        tokens.BLOCK_TAG_START,
        tokens.BLOCK_TAG_END,
    ),
    tokens.TOKEN_COMMENT: (
        tokens.COMMENT_TAG_START,
        tokens.COMMENT_TAG_END,
    ),
}


def render_django_token(token):
    token_type = token.token_type

    # This token is _exactly_ the text token, meaning that it is an unmodified
    # text node.
    if token.token_type is tokens.TOKEN_TEXT:
        return token.contents

    # This token has the same value as the text token, but given the above did
    # not match, it means this is a 'fake text' token, and is in fact a comment
    if token.token_type == tokens.TOKEN_TEXT:
        return '{# %s #}' % token.contents

    start, end = TOKEN_WRAPPERS[token_type]
    return '%s %s %s' % (start, token.contents, end)
