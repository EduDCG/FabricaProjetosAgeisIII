from src.modulos import Ranking
from src.modulos import AlterarVaga, Extrator

def main():

    while True:

        vaga_atual = ""
        with open("vaga.txt", "r", encoding="utf-8") as f:
            vaga_atual = f.read()

        # print(f"\nVaga atual: {vaga_atual}")
        print(f"1: Alterar vaga\n2: Converter currículos\n3: Calcular ranking\nQ: Sair\n")
        op = input()
        op = op.lower()

        if op == 'q':
            break  
        
        elif op == "1":
            print("Descreva a nova vaga:")
            desc_vaga = input()
            AlterarVaga.alterarVaga(desc_vaga)

        elif op == "2":
            Extrator.extrairTxt()
            Extrator.gerarJsons()

        elif op == "3":
            print("\n")
            Ranking.calcularRanking(vaga_atual)


if __name__ == "__main__":
    main()
