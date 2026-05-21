# Projeto de Fábrica de Projetos Ágeis III

## Feito por:
- Eduardo Girão
- Miguel Guimarães
- Vitor Mapelli
- Vitoria Colombo
## Proposta:
Um sistema que recebe arquivos de texto, extrai informações específicas e as vetoriza de forma que consiga compreender semântica e correlacionar informações para criar um score com as características da vaga informada.
## Setup:
1. Abrir o terminal e colar:
```sh
 git clone https://github.com/EduDCG/FabricaProjetosAgeisIII.git
 cd FabricaProjetosAgeisIII/
 python -m venv .venv
```
2. Ativar o ambiente virtual e baixar dependências:
   - Windows:`.venv\Scripts\activate`
   - Linux:`source .venv/bin/activate.fish` ou `source .venv/bin/activate`
```sh
pip install -r requirements.txt
```

3. Criar arquivo `.env` com a chave da API do Groq:
   - Criar manualmente ou digitando `touch .env` no terminal
   - Inserir `GROQ_API_KEY=[ChaveDaAPI]` no arquivo
4. Rodar projeto:
```sh
python main.py
```
**Observação:**
- O texto da vaga pode ser colado diretamente no `vaga.txt`
- Atualmente, os currículos em formato .pdf e .docx são colocados diretamente na pasta `src/arquivos`