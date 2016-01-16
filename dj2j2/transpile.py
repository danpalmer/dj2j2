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
