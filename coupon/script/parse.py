from . import lexer
from . import parser

def parse(script):
    lexerObj = lexer.Lexer()
    parserObj = parser.Parser(lexerObj)
    ast = parserObj.parse(script)
    errors = lexerObj.errors + parserObj.errors
    if len(errors) != 0:
        raise Exception('incorrect script: ' + ', '.join(errors))

    return ast
