import os, pymupdf, json, docx2txt
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

curriculos = "./src/arquivos"
pasta_txt = "./src/dados_txt"
pasta_json = "./src/dados_json"

def extrairTxt():
    
    if not os.path.exists(pasta_txt):
        os.makedirs(pasta_txt)

    try:

        if not os.listdir(curriculos):
            print("Nenhum arquivo encontrado para extrair.")
            return

        for filename in os.listdir(curriculos):

            if filename.endswith(".pdf"):
                caminho_pdf = os.path.join(curriculos, filename)
                print(f"Processando {filename}...")

                # abre o documento
                doc = pymupdf.open(caminho_pdf)
                texto_completo = ""

                # extrai texto das páginas
                for page in doc:
                    texto_completo += page.get_text()

                # salva em .txt
                nome_arquivo = filename.replace(".pdf", ".txt")
                caminho_txt = os.path.join(pasta_txt, nome_arquivo)

                with open(caminho_txt, "w", encoding="utf-8") as f:
                    f.write(texto_completo)
            
            if filename.endswith(".docx"):
                caminho_docx = os.path.join(curriculos, filename)
                print(f"Processando {filename}...")

                texto_completo = docx2txt.process(caminho_docx)

                nome_arquivo = filename.replace(".docx", ".txt")
                caminho_txt = os.path.join(pasta_txt, nome_arquivo)

                with open(caminho_txt, "w", encoding="utf-8") as f:
                    f.write(texto_completo)

    except Exception as erro:
        print(f"Erro ao extrair texto: {erro}\n")


# extrair .json dos .txt via IA (Groq)
def extrairJson(texto_pdf):
    system_prompt = {
        "role": "system",
        "content": (
            "Você é um especialista em RH técnico. Extraia informações do currículo fornecido "
            "e responda EXCLUSIVAMENTE em formato JSON. Não escreva explicações. "
            "Siga este esquema: {"
            "'nome': 'string', "
            "'hard_skills': ['lista', 'de', 'strings'], "
            "'soft_skills': ['lista', 'de', 'strings'], "
            "'experiencia_anos': int, "
            "'resumo_profissional': 'string'}"
        )
    }

    user_prompt = {
        "role": "user",
        "content": f"Texto do currículo: {texto_pdf}"
    }

    chat_completion = client.chat.completions.create(
        messages=[system_prompt, user_prompt],
        model="llama-3.1-8b-instant", 
        response_format={"type": "json_object"} # modo JSON do modelo
    )

    # converte a string de resposta em um dicionário Python
    resposta_texto = chat_completion.choices[0].message.content
    return json.loads(resposta_texto)


# transforma os .txt em .Json para organização melhor
def gerarJsons():

    if not os.path.exists(pasta_json):
        os.makedirs(pasta_json)

    arquivos = [f for f in os.listdir(pasta_txt) if f.endswith(".txt")]
    
    if not arquivos:
        print("Nenhum arquivo .txt encontrado.")
        return

    print(f"Iniciando conversão de {len(arquivos)} arquivos para JSON ...")

    for filename in arquivos:
        caminho_txt = os.path.join(pasta_txt, filename)
        
        with open(caminho_txt, "r", encoding="utf-8") as f:
            texto_cv = f.read()

        try:
            print(f"Analisando {filename}...")

            if len(texto_cv) < 50: 
                print(f"Aviso: O arquivo {filename} parece estar vazio ou mal formatado. Pulando...")
                return # passa para outro loop
            
            dados_conferidos = extrairJson(texto_cv) # usando a função da IA
            nome_json = filename.replace(".txt", ".json")
            caminho_final = os.path.join(pasta_json, nome_json)

            with open(caminho_final, "w", encoding="utf-8") as f_json:
                json.dump(dados_conferidos, f_json, indent=4, ensure_ascii=False)

        except Exception as e:
            print(f"Erro ao processar {filename}: {e}")

    print("Geração de arquivos JSON concluída.")
    