"""Cadastro de Pacientes - versão Gradio (execução local).

Executar com:  python gradio_app/app.py
"""
import os
from datetime import datetime

import gradio as gr
import pandas as pd

ARQUIVO_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]


def carregar_ultimos(n=5):
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(n)
    return pd.DataFrame(columns=COLUNAS)


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    if not nome or not nome.strip():
        return "Informe o nome do paciente.", carregar_ultimos()
    if idade is None:
        return "Informe a idade do paciente.", carregar_ultimos()
    if not convenio:
        return "Selecione o convênio.", carregar_ultimos()

    linha = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": motivo,
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)
    return "Paciente cadastrado com sucesso!", carregar_ultimos()


with gr.Blocks(title="Cadastro de Pacientes") as demo:
    gr.Markdown("## Cadastro de Pacientes")
    nome = gr.Textbox(label="Nome do paciente")
    idade = gr.Number(label="Idade", minimum=0, maximum=120, precision=0)
    convenio = gr.Dropdown(CONVENIOS, label="Convênio")
    prioridade = gr.Slider(1, 5, step=1, value=1, label="Prioridade do atendimento (5 = urgente)")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    botao = gr.Button("Cadastrar", variant="primary")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(value=carregar_ultimos(), label="Últimos pacientes cadastrados")

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela],
    )

if __name__ == "__main__":
    demo.launch()
