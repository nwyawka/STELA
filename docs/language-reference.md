# Language Reference (0.1)

The language is indentation-sensitive. Indented declarations belong to the preceding block. Use either exactly four spaces or one tab for a member line. Do not mix spaces and tabs on the same line. Blank lines and lines beginning with `#` are ignored.

```text
model Name

requirement symbolic_name:
    id: REQ-001
    shall expression
    verify_by test | analysis | inspection | demonstration

component TypeName:
    property name: unit = number
    port name: Interface in | out
    part name: ComponentType
    connect part.port -> part.port
    satisfies REQ-001

action name:
    input name: unit
    output name: unit
    set name = arithmetic_expression

scenario name:
    set dotted.name = number unit
    perform action with parameter = expression
    assert expression comparison expression
    verifies REQ-001
```

Arithmetic expressions support numeric literals, names, dotted names, `+`, `-`, `*`, `/`, and parentheses. They are evaluated by a restricted interpreter and cannot call Python functions or access Python objects.
