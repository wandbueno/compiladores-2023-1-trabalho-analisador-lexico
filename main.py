import re
from enum import Enum
from dataclasses import dataclass


class TokenClass(Enum):
    PALAVRA_RESERVADA = r"(struct\b|if\b|int\b|else\b|while\b|do\b|for\b|\bfloat\b|double\b|char\b|long\b|short\b|break\b|continue\b|case\b|switch\b|default\b|void\b|return)"
    CONSTANTE_NUMERICA = r"(\d+(\.\d*)?|\.\d+)(?![a-zA-Z])"
    IDENTIFICADOR = r"([a-zA-Z_][a-zA-Z0-9_]*|main|printf)"
    CONSTANTE_TEXTO = r'\".*?\"'
    OPERADOR = r"(==|!=|<=|>=|\|\||&&|\+=|-=|\*=|\=|--|\+\+|\+|\/|->|\*|\-|\||!|&|%|<|>)"
    DELIMITADOR = r"\[|\]|\(|\)|\{|\}|\;|\,|\:"


@dataclass
class Token:
    token_class: TokenClass
    token_value: str

    def __str__(self) -> str:
        return f'\n {self.token_class.name}: {self.token_value}'


with open('testes/teste-erro1.c', 'r', encoding='utf-8') as f:
    code = f.read()

code = re.sub(r'/\*[\s\S]*?\*/', '', code)
code = re.sub(r'//\s*[^\n]*', '', code, flags=re.DOTALL)

lines = code.split('\n')

tokens = []

for line_num, line in enumerate(lines, start=1):
    line = re.sub(r'\s+', ' ', line.strip())

    while line:
        match = None
        for token_class in TokenClass:
            regex = token_class.value
            match = re.match(regex, line)
            if match:
                break
        if match:
            lexema = match.group(0)
            token = Token(token_class, lexema)
            tokens.append(token)
            line = line[len(lexema):].lstrip()
        else:
            raise ValueError(
                f"Erro léxico na linha {line_num}: caractere inesperado: {line[0]!r}")

for token in tokens:
    print(token)
