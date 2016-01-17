import click

from django.template import base as tokens
from django.utils.safestring import SafeText


NODE_TYPE_HANDLERS = {}

def transpile_template(report, template):
    for node in template.nodelist:
        yield handle(report, node)


def handle(report, node):
    try:
        return ''.join(
            NODE_TYPE_HANDLERS[node.__class__.__name__](report, node)
        )
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


VAR_NODE_SPECIAL_CASES = {
    'block.super': 'super()',
}


@handler('VariableNode')
def handle_variable_node(report, var_node):
    node_text = render_filter_exp(
        report,
        var_node.filter_expression,
    )

    node_text = VAR_NODE_SPECIAL_CASES.get(node_text, node_text)

    yield '{{ %s }}' % node_text


@handler('IfNode')
def handle_if_node(report, if_node):
    for idx, (condition, nodelist) in enumerate(if_node.conditions_nodelists):
        if condition is None:
            yield '{% else %}'
        else:
            if not condition.value:
                # Condition is a boolean expression
                condition_text = '%s %s %s' % (
                    render_filter_exp(report, condition.first.value),
                    condition.id,
                    render_filter_exp(report, condition.second.value),
                )
            else:
                # Condition is a simple filter expression
                condition = condition.value
                condition_text = render_filter_exp(report, condition)

            yield '{%% %s %s %%}' % (
                'if' if idx == 0 else 'elif',
                condition_text,
            )

        for node in nodelist:
            yield handle(report, node)

    yield '{% endif %}'


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


def render_filter_exp(report, filter_expression):
    return ''.join(_filter_expression(report, filter_expression))


def _filter_expression(report, filter_expression):
    if isinstance(filter_expression.var, SafeText):
        yield '\'%s\'' % filter_expression.var
    else:
        yield filter_expression.var.var

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
    if token.token_type == tokens.TOKEN_TEXT:
        return token.contents

    else:
        start, end = TOKEN_WRAPPERS[token.token_type]
        return '%s %s %s' % (start, token.contents, end)
