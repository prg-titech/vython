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
    def __init__(self, name, version, bases, body):
        self.name = name
        self.version = version
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
    def __init__(self, func, version, args):
        self.func = func
        self.version = version # バージョン付きインスタンス生成のケースに必要
        self.args = args


class Attribute(ASTNode):
    def __init__(self, value, attr):
        self.value = value
        self.attr = attr


class CallIncompatible(ASTNode):
    def __init__(self, value):
        self.value = value


class Pass(ASTNode):
    pass


class Name(ASTNode):
    def __init__(self, id):
        self.id = id


class NoneNode(ASTNode):
    def __init__(self):
        super().__init__()
