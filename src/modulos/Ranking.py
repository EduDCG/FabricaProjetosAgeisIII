import os, json
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

    # Ler JSONs
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

    # Junta vaga + currículos
    corpus = [desc_vaga] + textos_candidatos

    # Vetorização
    vectorizer = TfidfVectorizer(stop_words=stop_words_pt)
    tfidf_matrix = vectorizer.fit_transform(corpus)

    # Similaridade
    vetor_vaga = tfidf_matrix[0:1]
    vetores_candidatos = tfidf_matrix[1:]

    similaridades = cosine_similarity(vetor_vaga, vetores_candidatos)[0]

    # Ranking
    ranking = list(zip(candidatos, similaridades))
    
    ranking.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # Criar TXT
    with open("ranking_candidatos.txt", "w", encoding="utf-8") as arquivo:

        arquivo.write("================================================\n")
        arquivo.write("          ANÁLISE DE CURRÍCULOS\n")
        arquivo.write("================================================\n\n")

        for posicao, (nome, score) in enumerate(ranking, start=1):

            porcentagem = score * 100

            # Classificação
            if porcentagem >= 40:
                status = "Aderência Alta"
                resumo = "Recomendado para avaliação"

            elif porcentagem >= 20:
                status = "Aderência Média"
                resumo = "Compatibilidade parcial com a vaga"

            elif porcentagem >= 10:
                status = "Aderência Baixa"
                resumo = "Baixa compatibilidade com os requisitos"

            else:
                status = "Pouca Compatibilidade"
                resumo = "Perfil pouco aderente"

            arquivo.write(f"Ranking #{posicao}\n")
            arquivo.write(f"Candidato: {nome}\n")
            arquivo.write(
                f"Compatibilidade com a vaga: {porcentagem:.2f}%\n"
            )
            arquivo.write(f"Status: {status}\n\n")

            arquivo.write("Resumo:\n")
            arquivo.write(f"- {resumo}\n")

            separador = "\n" + "=" * 50 + "\n\n"
            arquivo.write(separador)

    print("Arquivo ranking_candidatos.txt gerado com sucesso!")
