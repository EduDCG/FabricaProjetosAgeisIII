from pathlib import Path
from src.modulos import AlterarVaga, Extrator, Ranking

root = Path(__file__).resolve().parent
largura_separador = 35

def main():

    caminho_vaga = root / "vaga.txt"
    if not caminho_vaga.exists():
        with open(caminho_vaga, "w", encoding="utf-8") as f:
            f.write("Descreva os requisitos da vaga aqui.")

    while True:

        vaga_atual = ""
        with open(caminho_vaga, "r", encoding="utf-8") as f:
            vaga_atual = f.read()

        print("\n" + " VAGA ATUAL ".center(largura_separador, "="))
        print(f"Vaga Atual: {vaga_atual[:100]}..." if len(vaga_atual) > 100 else f"Vaga Atual: {vaga_atual}")
        print(" OPÇÕES ".center(largura_separador, "="))
        print(f"1: Alterar vaga")
        print(f"2: Converter currículos para .txt")
        print(f"3: Analisar currículos")
        print(f"4: Calcular ranking")
        print(f"5: Processar tudo")
        print(f"Q: Sair")
        print("".center(largura_separador, "=")) 
        print(f"Escolha uma opção: ", end="")

        op = input().lower().strip()

        if op == 'q':
            break  
        
        elif op == "1":
            print("Descreva a nova vaga:")
            desc_vaga = input()
            if desc_vaga.strip():
                AlterarVaga.alterarVaga(desc_vaga)
            else:
                print("A descrição da vaga não pode ser vazia.")

        elif op == "2":
            Extrator.extrairTxt()
            
        elif op == "3":
            Extrator.gerarJsons()

        elif op == "4":
            Ranking.calcularRanking(vaga_atual)

        else:
            print("\nOpção inválida.")


if __name__ == "__main__":
    main()
