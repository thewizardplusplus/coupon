# Microlanguage Grammar

```
script = or expression;

or expression = and expression, {"||", and expression};
and expression = not expression, {"&&", not expression};
not expression = ["!"], atom;
atom = filter | ("(", script, ")");
filter = identifier, "=~", REGULAR EXPRESSION;
identifier = IDENTIFIER, {".", IDENTIFIER};

IDENTIFIER = ? /\w+/ ?;
REGULAR EXPRESSION = ? /\/(?:\\.|[^\/])+\// ?;
SINGLE-LINE COMMENT = ? /\#.*/ ?.
```
