from lark import Lark
from lark.indenter import Indenter


class PythonIndenter(Indenter):
    NL_type = "_NEWLINE"
    OPEN_PAREN_types = ["LPAR", "LSQB", "LBRACE"]
    CLOSE_PAREN_types = ["RPAR", "RSQB", "RBRACE"]
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 8

class Parser:
    def parse(self, code):
        # 文法定義を読み込む
        with open("src/vython.lark", "r") as file:
            grammar = file.read()

        parser = Lark(
            grammar, parser="lalr", postlex=PythonIndenter(), start="file_input"
        )
        ast = parser.parse(code)

        return ast
