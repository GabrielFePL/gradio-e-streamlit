# Cadastro de Pacientes — Gradio x Streamlit

Atividade Prática da Aula 1 de **Aplicações em Data Science** (prof. Francisco Fambrini).

A mesma aplicação de coleta de dados (cadastro de pacientes de um consultório médico) foi feita duas vezes, uma com cada biblioteca:

| Pasta | Biblioteca | Execução | Persistência |
|---|---|---|---|
| [`gradio_app/`](gradio_app/) | Gradio (`gr.Blocks`) | Local | `gradio_app/pacientes.csv` |
| [`streamlit_app/`](streamlit_app/) | Streamlit (`st.form`) | Streamlit Community Cloud | `st.session_state` + botão de download do CSV |

## Campos do formulário

- Nome do paciente (texto)
- Idade (número)
- Convênio (Particular, Unimed, Bradesco Saúde, SulAmérica, Outro)
- Prioridade do atendimento (1 a 5, sendo 5 = urgente)
- Motivo da consulta / observações (texto)

Cada cadastro também grava a data/hora (`timestamp`).

## Como executar localmente

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt

# Versão Gradio
python gradio_app/app.py

# Versão Streamlit
streamlit run streamlit_app/app.py
```

## Deploy no Streamlit Community Cloud

1. Acesse [share.streamlit.io](https://share.streamlit.io) e entre com a conta do GitHub.
2. Clique em **New app** e selecione este repositório, a branch `main` e o arquivo `streamlit_app/app.py`.
3. Aguarde o build e teste pelo link público (`*.streamlit.app`), inclusive no celular.

> O sistema de arquivos do Streamlit Community Cloud é efêmero. Por isso os dados ficam em `st.session_state` e podem ser exportados pelo botão **Baixar CSV**.

## Entrega

- [ ] Link deste repositório
- [ ] Link público do app no Streamlit Community Cloud
- [ ] Print da interface Gradio rodando localmente
- [ ] Arquivo `pacientes.csv` de exemplo gerado nos testes
