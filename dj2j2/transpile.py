NODE_TYPE_HANDLERS = {}

def transpile_template(template):
    for node in template.nodelist:
        yield ''.join(NODE_TYPE_HANDLERS[node.__class__.__name__](node))


def handle(node_type):
    def handle_decorator(fn):
        NODE_TYPE_HANDLERS[node_type] = fn
        return fn
    return handle_decorator


@handle('TextNode')
def handle_text_node(text_node):
    yield text_node.s


@handle('VariableNode')
def handle_variable_node(var_node):
    yield '{{ '

    exp = var_node.filter_expression
    yield exp.var.var

    for filter_, args in exp.filters:
        if callable(filter_):
            yield '|%s' % filter_.__name__

        if args:
            args = args[0][1:] # Drop "False" initial arg
            yield '(%s)' % ', '.join('\'%s\'' % x for x in args)

    yield ' }}'
