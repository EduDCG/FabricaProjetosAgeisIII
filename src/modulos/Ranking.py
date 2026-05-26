import os, json
import numpy as np
# from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')
stop_words_pt = stopwords.words('portuguese')

def calcularRanking(desc_vaga):

    pasta_json = "./src/dados_json"
    
    if not os.path.exists(pasta_json):
        print(f"Pasta {pasta_json} não encontrada.")
        return
    
    arquivos = [f for f in os.listdir(pasta_json) if f.endswith(".json")]
    if not arquivos:
        print("Nenhum JSON encontrado para rankear.")
        return
    
    candidatos = []
    textos_candidatos = []
 
    # Aqui ele vai ler cada JSON e guardar todos
    # Pensei nele ler tudo de uma vez pq ai ele consideraria o contexto e pegaria palavras mais "raras" que podem ser mais relevantes por aparecer menos vezes.
    for filename in arquivos:
        caminho_completo = os.path.join(pasta_json, filename)
        with open(caminho_completo, "r", encoding="utf-8") as f:
            dados = json.load(f)
            nome = dados.get("nome", "Desconhecido")
          
            hard_skills = " ".join(dados.get("hard_skills", []))
            soft_skills = " ".join(dados.get("soft_skills", []))
            resumo = dados.get("resumo_profissional", "")
            
            texto_final = f"{resumo} {hard_skills} {soft_skills}"
            
            candidatos.append(nome)
            textos_candidatos.append(texto_final)

  
    corpus = [desc_vaga] + textos_candidatos

    # Vai vetorizar td de uma vez
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # no calculo de similaridade o indice 0 é a vaga, o resto dos indices são os candidatos
    vetor_vaga = tfidf_matrix[0:1]
    vetores_candidatos = tfidf_matrix[1:]
    
    similaridades = cosine_similarity(vetor_vaga, vetores_candidatos)[0]

    # Junta o nome comso score e vai ordenar do maior para o menor
    ranking = list(zip(candidatos, similaridades))
    ranking.sort(key=lambda x: x[1], reverse=True)

    print("--- RANKING DE CANDIDATOS ---")
    for nome, score in ranking:
        print(f"Candidato: {nome} | Score: {score * 100:.2f}%")
