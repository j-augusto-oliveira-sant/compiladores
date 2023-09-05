from analisador_lexico import AnalisadorLexico


class AnalisadorSintatico:
    """
    Analisa uma gramatica procurando erros sintaticos após leitura do analisador lexico.
    """

    def __init__(self, analisador_lexico) -> None:
        self.cont = 0
        self.analisador_lexico


if __name__ == "__main__":
    print("-- init analisador sintatico --")
    lexico = AnalisadorLexico()
    code = """
    fn main(){
        integer x;
        x=5;
        if (x==10){
            y = 5;
        };
        print(y);
    }
    """
    sintatico = AnalisadorSintatico(lexico)
