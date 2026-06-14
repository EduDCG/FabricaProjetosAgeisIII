from pathlib import Path
from src.modulos import AlterarVaga, Extrator, Ranking

root = Path(__file__).resolve().parent

def main():

    caminho_vaga = root / "vaga.txt"
    if not caminho_vaga.exists():
        with open(caminho_vaga, "w", encoding="utf-8") as f:
            f.write("Descreva os requisitos da vaga aqui.")

    while True:

        vaga_atual = ""
        with open(caminho_vaga, "r", encoding="utf-8") as f:
            vaga_atual = f.read()

        # print(f"\nVaga atual: {vaga_atual}")
        print(f"1: Alterar vaga")
        print(f"2: Converter currículos para .txt")
        print(f"3: Analisar currículos")
        print(f"4: Calcular ranking")
        print(f"Q: Sair")

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
            
        elif op == "3":
            Extrator.gerarJsons()

        elif op == "4":
            print("\n")
            Ranking.calcularRanking(vaga_atual)


if __name__ == "__main__":
    main()
