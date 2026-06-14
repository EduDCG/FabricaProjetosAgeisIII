import os, json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
from pathlib import Path

nltk.download('stopwords', quiet=True)
stop_words_pt = stopwords.words('portuguese')

root = Path(__file__).resolve().parent.parent
pasta_json = root / "dados_json"

def carregarCandidatos(pasta_json):

    if not os.path.exists(pasta_json):
        print(f"Pasta {pasta_json} não encontrada.")
        return [], []

    arquivos = [f.name for f in pasta_json.iterdir() if f.is_file() and f.name.endswith(".json")]

    if not arquivos:
        print("Nenhum JSON encontrado para rankear.")
        return [],[]

    candidatos = []
    textos_candidatos = []

    # Ler JSONs
    for filename in arquivos:

        caminho_completo = pasta_json / filename

        with open(caminho_completo, "r", encoding="utf-8") as f:

            try:
                dados = json.load(f)
            except json.JSONDecodeError:
                print(f"Erro: {filename} não é um JSON válido. Pulando...")
                continue

            nome = dados.get("nome")
            if not nome or nome == "null":
                nome = filename.replace(".json", "")

            # tratamento das hard skills
            hard_skills_bruto = dados.get("hard_skills") 
            if isinstance(hard_skills_bruto, list):
                hard_skills = " ".join([str(skill) for skill in hard_skills_bruto if skill])
            elif isinstance(hard_skills_bruto, str) and hard_skills_bruto != "null":
                hard_skills = hard_skills_bruto
            else:
                hard_skills = ""

            # tratamento das soft skills
            soft_skills_bruto = dados.get("soft_skills") 
            if isinstance(soft_skills_bruto, list):
                soft_skills = " ".join([str(skill) for skill in soft_skills_bruto if skill])
            elif isinstance(soft_skills_bruto, str) and soft_skills_bruto != "null":
                soft_skills = soft_skills_bruto
            else:
                soft_skills = ""

            resumo = dados.get("resumo_profissional")
            if not resumo or resumo == "null":
                resumo = ""

            texto_final = f"{resumo} {hard_skills} {soft_skills}".strip()
            
            if texto_final:
                candidatos.append(nome)
                textos_candidatos.append(texto_final)
            else:
                print(f"Erro: O candidato possui dados vazios após a análise da IA.")

    return candidatos, textos_candidatos


def calcularRanking(desc_vaga):

    candidatos, textos_candidatos = carregarCandidatos(pasta_json)

    if not candidatos or not textos_candidatos:
        print(f"Erro ao carregar candidatos.")
        return

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


def exibirRanking():
    caminho_ranking = root.parent / "ranking_candidatos.txt"

    if not caminho_ranking.exists():
        print("AVISO: O arquivo ranking_candidatos.txt não foi encontrado. Tem certeza de que ele já foi gerado?")
        return

    try:
        with open(caminho_ranking, "r", encoding="utf-8") as arquivo:
            conteúdo = arquivo.read()
            print(conteúdo)
            
    except Exception as e:
        print(f"Erro ao ler o arquivo de ranking: {e}")