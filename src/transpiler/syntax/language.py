# Prettyprinter
class ReprMixin:
    def __repr__(self):
        return self._one_line_repr(self)

    def detailed_repr(self):
        return self._format_repr(self, 0)

    def _one_line_repr(self, obj):
        if isinstance(obj, ReprMixin):
            parts = [
                f"{key}={self._one_line_repr(value)}"
                for key, value in vars(obj).items()
            ]
            return obj.__class__.__name__ + "(" + ", ".join(parts) + ")"

        elif isinstance(obj, list):
            return "[" + ", ".join(self._one_line_repr(item) for item in obj) + "]"

        elif isinstance(obj, dict):
            return (
                "{"
                + ", ".join(
                    f"{key}: {self._one_line_repr(value)}" for key, value in obj.items()
                )
                + "}"
            )

        elif obj is None:
            return str(None)

        else:
            return "'" + str(obj) + "'"

    def _format_repr(self, obj, indent):
        lines = []
        if isinstance(obj, ReprMixin):
            lines.append(" " * indent + obj.__class__.__name__)

            for key, value in obj.__dict__.items():
                lines.append(" " * (indent + 2) + f"{key}:")
                formatted_value = self._format_repr(value, indent + 4)
                lines.extend(formatted_value.splitlines())

        elif isinstance(obj, list):
            for item in obj:
                item_repr = self._format_repr(item, indent + 4)
                lines.append(" " * (indent + 2) + "- " + item_repr.lstrip())

        elif isinstance(obj, dict):
            for key, value in obj.items():
                lines.append(" " * (indent + 2) + f"{key}:")
                lines.extend(self._format_repr(value, indent + 2).splitlines())

        else:
            lines.append(" " * indent + str(obj))

        return "\n".join(lines)


class ASTNode(ReprMixin):
    pass


# 各ASTNodeの定義
# なるべくPython ASTの仕様に従うように定義
# https://docs.python.org/ja/3/library/ast.html


class Module(ASTNode):
    def __init__(self, body):
        self.body = body


class ClassDef(ASTNode):
    def __init__(self, name, bases, body):
        self.name = name
        self.bases = bases
        self.body = body


class Version(ASTNode):
    def __init__(self, version):
        self.version = version


class FunctionDef(ASTNode):
    def __init__(self, name, args, body):
        self.name = name
        self.args = args
        self.body = body


class Return(ASTNode):
    def __init__(self, value):
        self.value = value


class Assign(ASTNode):
    def __init__(self, targets, value):
        self.targets = targets
        self.value = value


class Expr(ASTNode):
    def __init__(self, value):
        self.value = value


class Call(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args


class Attribute(ASTNode):
    def __init__(self, value, attr):
        self.value = value
        self.attr = attr


class CallIncompatible(ASTNode):
    def __init__(self, value, args):
        self.value = value
        self.args = args


class Pass(ASTNode):
    pass


class Name(ASTNode):
    def __init__(self, id, version):
        self.id = id
        self.version = version


class NoneNode(ASTNode):
    def __init__(self):
        super().__init__()

class Boolean(ASTNode):
    def __init__(self, value):
        self.value = value

class ConstTrue(ASTNode):
    def __init__(self):
        super().__init__()

class ConstFalse(ASTNode):
    def __init__(self):
        super().__init__()

class CompOp(ASTNode):
    def __init__(self, op):
        self.op = op

class Comparison(ASTNode):
    # Pythonのsemanticに則ると、引数の数は可変なので、配列を入れる
    def __init__(self, comp_list):
        self.comp_list = comp_list


class OrExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class AndExpr(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class ArithExpr(ASTNode):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

class Term(ASTNode):
    def __init__(self, left, right, op):
        self.left = left
        self.right = right
        self.op = op

class Factor(ASTNode):
    def __init__(self, op, value):
        self.op = op
        self.value = value

# if文に関するASTNode
class If(ASTNode):
    def __init__(self, test, then_body, elifs, else_body):
        self.test = test
        self.then_body = then_body
        self.elifs = elifs
        self.else_body = else_body

class Elifs(ASTNode):
    def __init__(self, elif_):
        self.elif_ = elif_

class Elif(ASTNode):
    def __init__(self, test, then_body):
        self.test = test
        self.then_body = then_body

