import os

def alterarVaga(desc_vaga):
    vaga = "./vaga.txt"

    with open(vaga, "w", encoding="utf-8") as f:
        f.write(desc_vaga)