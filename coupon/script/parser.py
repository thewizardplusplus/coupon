import re

import ply.yacc

from . import ast_node
from .. import logger

def _rule(grammar):
    def set_doc(function):
        function.__doc__ = grammar
        return function

    return set_doc

class Parser:
    errors = []

    def __init__(self, lexer):
        self.tokens = lexer.tokens
        self._lexer = lexer
        self._preparser = ply.yacc.yacc(module=self, debug=False)

    def parse(self, code):
        return self._preparser.parse(code, lexer=self._lexer)

    @_rule('''or_expression : and_expression
        | or_expression OR_OPERATOR and_expression''')
    def p_or_expression(self, node):
        _process_list('or_expression', node)

    @_rule('''and_expression : not_expression
        | and_expression AND_OPERATOR not_expression''')
    def p_and_expression(self, node):
        _process_list('and_expression', node)

    @_rule('''not_expression : atom
        | '!' atom''')
    def p_not_expression(self, node):
        node[0] = ast_node.AstNode(name='not_expression', children=[node[2]]) \
            if len(node) == 3 \
            else node[1]

    @_rule("""atom : filter
        | '(' or_expression ')'""")
    def p_atom(self, node):
        node[0] = ast_node.AstNode(
            name='atom',
            children=[node[2 if len(node) == 4 else 1]],
        )

    @_rule('filter : identifier_list MATCH_OPERATOR REGULAR_EXPRESSION')
    def p_filter(self, node):
        try:
            node[0] = ast_node.AstNode(
                name='filter',
                children=[node[1], re.compile(node[3][1:-1])],
            )
        except Exception as exception:
            self._process_error(
                'incorrect regular expression: ' + str(exception),
            )

    @_rule('''identifier_list : identifier
        | identifier_list '|' identifier''')
    def p_identifier_list(self, node):
        _process_list('identifier_list', node)

    @_rule('''identifier : IDENTIFIER
        | identifier '.' IDENTIFIER''')
    def p_identifier(self, node):
        _process_list('identifier', node)

    def p_error(self, token):
        self._process_error(
            'unexpected token ' + str(token) \
                if token is not None \
                else 'unexpected token EOF',
        )

        if token is not None:
            self._preparser.errok()

    def _process_error(self, err):
        self.errors.append(err)
        logger.get_logger().warning(err)

def _process_list(name, node):
    node[0] = ast_node.AstNode(
        name=name,
        children=node[1].children + [node[3]] \
            if len(node) == 4 \
            else [node[1]],
    )
