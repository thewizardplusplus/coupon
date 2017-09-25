# Microlanguage Grammar

```
script = or expression;

or expression = and expression, {"||", and expression};
and expression = not expression, {"&&", not expression};
not expression = ["!"], atom;
atom = filter | ("(", script, ")");
filter = identifier list, "=~", REGULAR EXPRESSION;
identifier list = identifier, {"|", identifier};
identifier = IDENTIFIER, {".", IDENTIFIER};

IDENTIFIER = ? /\w+/ ?;
REGULAR EXPRESSION = ? /\/(?:\\.|[^\/])+\// ?;
SINGLE-LINE COMMENT = ? /\#.*/ ?.
```
