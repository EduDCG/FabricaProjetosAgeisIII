import os, pymupdf, json, docx2txt
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

root = Path(__file__).resolve().parent.parent
curriculos = root / "arquivos"
pasta_txt = root / "dados_txt"
pasta_json = root / "dados_json"

def extrairTxt():
    curriculos.mkdir(parents=True, exist_ok=True)
    pasta_txt.mkdir(parents=True, exist_ok=True)

    try:

        if not any(curriculos.iterdir()):
            print("Nenhum arquivo encontrado para extrair.")
            return

        for arquivo in curriculos.iterdir():

            if not arquivo.is_file(): # pular se não for um arquivo
                continue
            
            filename = arquivo.name

            # para arquivos PDF
            if filename.endswith(".pdf"):
                print(f"Processando {filename}...")

                # abre o documento
                doc = pymupdf.open(arquivo)
                texto_completo = ""

                # extrai texto das páginas
                for page in doc:
                    texto_completo += page.get_text()

                # salva em .txt
                nome_arquivo = filename.replace(".pdf", ".txt")
                caminho_txt = pasta_txt / nome_arquivo

                with open(caminho_txt, "w", encoding="utf-8") as f:
                    f.write(texto_completo)
            
            # para arquivos Word
            if filename.endswith(".docx"):
                print(f"Processando {filename}...")

                texto_completo = docx2txt.process(str(arquivo))

                nome_arquivo = filename.replace(".docx", ".txt")
                caminho_txt = pasta_txt / nome_arquivo

                with open(caminho_txt, "w", encoding="utf-8") as f:
                    f.write(texto_completo)

    except Exception as erro:
        print(f"Erro ao extrair texto: {erro}\n")


# analisa e extrai .json dos .txt via IA (Groq)
def extrairJson(texto_pdf):
    system_prompt = {
        "role": "system",
        "content": (
            "Você é um especialista em RH técnico. Extraia informações do currículo fornecido "
            "e responda EXCLUSIVAMENTE em formato JSON. Não escreva explicações. "
            "Se o texto estiver vazio, confuso ou não for um currículo, retorne todos os campos como null ou listas vazias. "
            "Siga este esquema: {"
            "'nome': 'string', "
            "'hard_skills': ['lista', 'de', 'strings'], "
            "'soft_skills': ['lista', 'de', 'strings'], "
            "'experiencia_anos': int, "
            "'resumo_profissional': 'string'}"
            "NÃO adicione campos novos."
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


# função de processar arquivo (individualmente)
def processarArquivo(arquivo):
    caminho_txt = pasta_txt / arquivo
        
    with open(caminho_txt, "r", encoding="utf-8") as f:
        texto_cv = f.read()

    try:
        print(f"Analisando {arquivo}...")

        if len(texto_cv) < 50: 
            print(f"Aviso: O arquivo {arquivo} parece estar vazio ou mal formatado. Pulando...")
            return # passa para outro loop
        
        dados_conferidos = extrairJson(texto_cv) # usando a função da IA
        nome_json = arquivo.replace(".txt", ".json")
        caminho_final = pasta_json / nome_json

        with open(caminho_final, "w", encoding="utf-8") as f_json:
            json.dump(dados_conferidos, f_json, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Erro ao processar {arquivo}: {e}")


# transforma os .txt em .Json para organização melhor
def gerarJsons():

    pasta_txt.mkdir(parents=True, exist_ok=True)

    arquivos = [f for f in os.listdir(pasta_txt) if f.endswith(".txt")]
    
    if not arquivos:
        print("Nenhum arquivo .txt encontrado.")
        return

    print(f"Iniciando conversão de {len(arquivos)} arquivos para JSON...")

    with ThreadPoolExecutor(max_workers=4) as executor: # executa até 4 de uma vez
        executor.map(processarArquivo, arquivos)
        

    print("Geração de arquivos JSON concluída.")
    