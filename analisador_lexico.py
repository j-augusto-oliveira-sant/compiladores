###################################
# Analisador Léxico               #
# José Augusto Oliveira Sant'Ana  #
###################################
import re
from pydantic import BaseModel


class Token(BaseModel):
    valor: str
    lexema: str
    linha: str
    pos_inicial: str
    pos_final: str


def text_with_color(text, color):
    """Changes text color"""
    color = color.lower()
    if color == "red":
        coloring = "\u001b[31m"
    elif color == "white":
        coloring = "\u001b[37m"
    elif color == "blue":
        coloring = "\u001b[34m"
    elif color == "yellow":
        coloring = "\u001b[33m"
    elif color == "green":
        coloring = "\u001b[32m"

    return coloring + text + "\u001b[0m"


def analisador_lexico(codigo: str):
    tokens = []
    # tratar palavra
    word_positions = []
    lines = codigo.split("\n")
    for line_number, line in enumerate(lines, 1):
        words = re.findall(r"\b\w+\b|[><=()+-{}]", line)
        print(words)
        initial_column = 1
        for word in words:
            start = line.find(word, initial_column)
            end = start + len(word) - 1
            word_positions.append(
                {
                    "word": word,
                    "line": line_number,
                    "initial_column": start + 1,
                    "final_column": end + 1,
                }
            )
            initial_column = end + 2

    for word_position in word_positions:
        palavra = word_position["word"]
        # AFN
        automato = {
            "q0": {
                "letra": "q1",
                "i": "q2",
                "f": "q4",
                "w": "q7",
                "numero": "q12",
                "(": "q13",
                ")": "q14",
                "+": "q15",
                "[": "q16",
                "]": "q17",
                "{": "q18",
                "}": "q19",
                "*": "q20",
                "/": "q21",
                "-": "q22",
                "%": "q23",
                "^": "q24",
                ">": "q25",
                "<": "q27",
                "=": "q29",
            },
            "q1": {"letra": "q1", "numero": "q1"},
            "q2": {"letra": "q1", "f": "q3"},
            "q3": {"letra": "q1", "numero": "q1"},
            "q4": {"letra": "q1", "o": "q5"},
            "q5": {"letra": "q1", "r": "q6"},
            "q6": {"letra": "q1", "numero": "q1"},
            "q7": {"letra": "q1", "h": "q8"},
            "q8": {"letra": "q1", "i": "q9"},
            "q9": {"letra": "q1", "l": "q10"},
            "q10": {"letra": "q1", "e": "q11"},
            "q11": {"letra": "q1", "numero": "q1"},
            "q12": {"numero": "q12"},
            "q13": {"": ""},
            "q14": {"": ""},
            "q15": {"": ""},
            "q16": {"": ""},
            "q17": {"": ""},
            "q18": {"": ""},
            "q19": {"": ""},
            "q20": {"": ""},
            "q21": {"": ""},
            "q22": {"": ""},
            "q23": {"": ""},
            "q24": {"": ""},
            "q25": {"=": "q26"},
            "q26": {"": ""},
            "q27": {"=": "q28"},
            "q28": {"": ""},
            "q29": {"": ""},
        }

        # estado inicial
        inicial_estado = "q0"

        # estados finais
        estados_finais = {
            "q1": "VARIAVEL",
            "q3": "IF",
            "q6": "FOR",
            "q11": "WHILE",
            "q12": "CONSTANTE",
            "q13": "ABRE PARENTESES",
            "q14": "FECHA PARENTESES",
            "q15": "SOMA",
            "q16": "ABRE COLCHETES",
            "q17": "FECHA COLCHETES",
            "q18": "ABRE CHAVES",
            "q19": "FECHA CHAVES",
            "q20": "MULTIPLICACAO",
            "q21": "DIVISAO",
            "q22": "SUBTRACAO",
            "q23": "RESTO",
            "q24": "ELEVADO",
            "q25": "MAIOR",
            "q26": "MAIOR IGUAL",
            "q27": "MENOR",
            "q28": "MENOR IGUAL",
            "q29": "IGUAL",
        }

        estado_atual = inicial_estado
        for simbolo in palavra:
            if simbolo in automato[estado_atual]:
                estado_atual = automato[estado_atual][simbolo]
            elif simbolo.isalpha() and "letra" in automato[estado_atual]:
                estado_atual = automato[estado_atual]["letra"]
            elif simbolo.isdigit() and "numero" in automato[estado_atual]:
                estado_atual = automato[estado_atual]["numero"]
            else:
                break

        if estado_atual in estados_finais:
            tokens.append(
                Token(
                    valor=estados_finais[estado_atual],
                    lexema=word_position["word"],
                    linha=word_position["line"],
                    pos_inicial=word_position["initial_column"],
                    pos_final=word_position["final_column"],
                )
            )

    return tokens


if __name__ == "__main__":
    analisador_lexico()
