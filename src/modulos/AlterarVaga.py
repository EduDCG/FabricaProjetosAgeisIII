import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent.parent

def alterarVaga(desc_vaga):
    vaga = root / "vaga.txt"

    with open(vaga, "w", encoding="utf-8") as f:
        f.write(desc_vaga)