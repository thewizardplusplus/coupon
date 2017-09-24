import json

import ply.lex

from .. import logger

class Lexer:
    tokens = [
        'IDENTIFIER',
        'REGULAR_EXPRESSION',
        'MATCH_OPERATOR',
        'AND_OPERATOR',
        'OR_OPERATOR',
    ]
    t_IDENTIFIER = r'\w+'
    t_REGULAR_EXPRESSION = r'/(?:\\.|[^/])+/'
    t_MATCH_OPERATOR = '=~'
    t_AND_OPERATOR = '&&'
    t_OR_OPERATOR = '\|\|'
    t_ignore = ' \t\n\r'
    literals = '.|!()'
    errors = []

    def __init__(self):
        self._lexer = ply.lex.lex(module=self)

    def input(self, code):
        self._lexer.input(code)

    def token(self):
        return self._lexer.token()

    @ply.lex.TOKEN('\#.*')
    def t_SINGLE_LINE_COMMENT(self, token):
        pass

    def t_error(self, token):
        err = 'illegal character ' + json.dumps(token.value[0])
        self.errors.append(err)
        logger.get_logger().warning(err)

        self._lexer.skip(1)
