###################################
# Analisador Léxico               #
# José Augusto Oliveira Sant'Ana  #
###################################
from pydantic import BaseModel


class Token(BaseModel):
    valor: str
    lexema: str
    linha: int
    pos_inicial: int
    pos_final: int


def tokenize_code(codigo: str):
    tokens = []
    linhas = codigo.split("\n")
    for contador_linhas, linha in enumerate(linhas, start=1):
        palavra = []
        estado_atual = "q0"
        posicao_inicial = 1
        posicao_final = 1
        lista_simbolos_linha = [symbol for symbol in linha if not symbol.isspace()]
        while len(lista_simbolos_linha) > 0:
            for simbolo in lista_simbolos_linha:
                posicao_final += 1
                palavra.append(simbolo)
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
                    "q14": {},
                    "q15": {},
                    "q13": {},
                    "q16": {},
                    "q17": {},
                    "q18": {},
                    "q19": {},
                    "q20": {},
                    "q23": {},
                    "q21": {},
                    "q22": {},
                    "q24": {},
                    "q25": {"=": "q26"},
                    "q26": {},
                    "q27": {"=": "q28"},
                    "q28": {},
                    "q29": {},
                }

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

                if simbolo in automato[estado_atual]:
                    estado_atual = automato[estado_atual][simbolo]
                elif simbolo.isalpha() and "letra" in automato[estado_atual]:
                    estado_atual = automato[estado_atual]["letra"]
                elif simbolo.isdigit() and "numero" in automato[estado_atual]:
                    estado_atual = automato[estado_atual]["numero"]
                else:
                    lexema = "".join(palavra[:-1])
                    posicao_final -= 1
                    if len(lexema) > 0:
                        tokens.append(
                            Token(
                                valor=estados_finais[estado_atual],
                                lexema=lexema,
                                linha=contador_linhas,
                                pos_inicial=posicao_inicial,
                                pos_final=posicao_final,
                            )
                        )
                    palavra.clear()
                    estado_atual = "q0"
                    posicao_inicial = posicao_final
                    tamanho_lexema = len(lexema)
                    lista_simbolos_linha = lista_simbolos_linha[tamanho_lexema:]
                    break
            else:
                lexema = "".join(palavra)
                posicao_final -= 1
                if len(lexema) > 0:
                    tokens.append(
                        Token(
                            valor=estados_finais[estado_atual],
                            lexema=lexema,
                            linha=contador_linhas,
                            pos_inicial=posicao_inicial,
                            pos_final=posicao_final,
                        )
                    )
                palavra.clear()
                estado_atual = "q0"
                posicao_inicial = posicao_final
                tamanho_lexema = len(lexema)
                lista_simbolos_linha = lista_simbolos_linha[tamanho_lexema:]
                break

    return tokens
