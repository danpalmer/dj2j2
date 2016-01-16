NODE_TYPE_HANDLERS = {}

def transpile_template(report, template):
    for node in template.nodelist:
        yield handle(report, node)


def handle(report, node):
    return ''.join(NODE_TYPE_HANDLERS[node.__class__.__name__](report, node))


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
    yield '{{ '
    yield ''.join(handle_filter_expression(report, var_node.filter_expression))
    yield ' }}'


@handler('IfNode')
def handle_if_node(report, if_node):
    for idx, (condition, nodelist) in enumerate(if_node.conditions_nodelists):
        if condition is None:
            yield '{% else %}'
        else:
            condition = condition.value
            condition_text = ''.join(
                handle_filter_expression(report, condition),
            )
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
    lineno = load_node.token.lineno

    for library in libraries:
        report.add_required_library(library, lineno)

    yield '' # We must yield content


def handle_filter_expression(report, filter_expression):
    yield filter_expression.var.var

    for filter_, args in filter_expression.filters:
        if callable(filter_):
            yield '|%s' % filter_.__name__

        if args:
            args = args[0][1:] # Drop "False" initial arg
            yield '(%s)' % ', '.join('\'%s\'' % x for x in args)
