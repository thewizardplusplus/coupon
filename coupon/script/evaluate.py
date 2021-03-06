import functools

def evaluate_or_expression(node, context):
    return any(evaluate_and_expression(node, context) for node in node.children)

def evaluate_and_expression(node, context):
    return all(
        evaluate_not_expression(node, context) \
            if node.name == 'not_expression' \
            else evaluate_atom(node, context)
        for node in node.children
    )

def evaluate_not_expression(node, context):
    return not evaluate_atom(node.children[0], context)

def evaluate_atom(node, context):
    node = node.children[0]
    return evaluate_or_expression(node, context) \
        if node.name == 'or_expression' \
        else evaluate_filter(node, context)

def evaluate_filter(node, context):
    return any(
        node.children[1].search(value)
        for value in evaluate_identifier_list(node.children[0], context)
    )

def evaluate_identifier_list(node, context):
    return (
        evaluate_identifier(identifier, context)
        for identifier in node.children
    )

def evaluate_identifier(node, context):
    return str(get_nested_item(context, node.children))

# https://stackoverflow.com/a/14692747
def get_nested_item(collection, key_list):
    return functools.reduce(get_item, key_list, collection)

def get_item(collection, key):
    if isinstance(collection, list):
        return collection[int(key)]
    elif isinstance(collection, dict):
        return collection[key]
    else:
        raise Exception(
            'unexpected collection type ' + type(collection).__name__,
        )
