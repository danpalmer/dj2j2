from django.template.defaulttags import TemplateLiteral


NODE_TYPE_HANDLERS = {}

def transpile_template(template):
    for node in template.nodelist:
        yield handle(node)

def handle(node):
    return ''.join(NODE_TYPE_HANDLERS[node.__class__.__name__](node))


def handler(node_type):
    def handle_decorator(fn):
        NODE_TYPE_HANDLERS[node_type] = fn
        return fn
    return handle_decorator


@handler('TextNode')
def handle_text_node(text_node):
    yield text_node.s


@handler('VariableNode')
def handle_variable_node(var_node):
    yield '{{ '
    yield ''.join(handle_filter_expression(var_node.filter_expression))
    yield ' }}'


@handler('IfNode')
def handle_if_node(if_node):
    for idx, (condition, nodelist) in enumerate(if_node.conditions_nodelists):
        if condition is None:
            yield '{% else %}'
        else:
            condition = condition.value
            condition_text = ''.join(handle_filter_expression(condition))
            yield '{%% %s %s %%}' % (
                'if' if idx == 0 else 'elif',
                condition_text,
            )

        for node in nodelist:
                yield handle(node)

    yield '{% endif %}'

def handle_filter_expression(filter_expression):
    yield filter_expression.var.var

    for filter_, args in filter_expression.filters:
        if callable(filter_):
            yield '|%s' % filter_.__name__

        if args:
            args = args[0][1:] # Drop "False" initial arg
            yield '(%s)' % ', '.join('\'%s\'' % x for x in args)
