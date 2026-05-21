import os, json
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer

def calcularRanking(desc_vaga):

    pasta_json = "./src/dados_json"
    arquivos = [f for f in os.listdir(pasta_json) if f.endswith(".json")]
    if not arquivos:
        print("Nenhum JSON encontrado para rankear.")
        return

    for filename in arquivos:
        # join para obter o caminho completo do arquivo
        with open(os.path.join(pasta_json, filename), "r", encoding="utf-8") as f:
            dados = json.load(f)
            nome = dados.get("nome")

            # unindo as skills em uma única string
            hardskills_texto = ", ".join(dados.get("hard_skills", []))
            softskills_texto = ", ".join(dados.get("soft_skills", []))
            resumo_texto = dados.get("resumo_profissional") + " | " + hardskills_texto + " | " + softskills_texto
            # print(f"{resumo_texto}")

            n = 1
            counts = CountVectorizer(analyzer='word', ngram_range=(n, n)) 
            n_grams = counts.fit_transform([desc_vaga, resumo_texto])
            n_grams_array = n_grams.toarray()

            intersection_list = np.amin(n_grams_array, axis=0)
            intersection_count = np.sum(intersection_list)
            
            A_count = np.sum(n_grams_array[0])
            score = intersection_count / A_count
            print(f"{nome}\nScore: {score*100:.2f}\n")
