"""Cadastro de Pacientes - versão Gradio (execução local).

Executar com:  python gradio_app/app.py
Os dados são gravados em gradio_app/pacientes.csv.
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import gradio as gr
import pandas as pd

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA, "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]
FUSO = ZoneInfo("America/Sao_Paulo")


def carregar_ultimos(n=5):
    """Retorna os n últimos pacientes do CSV (ou uma tabela vazia)."""
    if os.path.exists(ARQUIVO_CSV):
        return pd.read_csv(ARQUIVO_CSV).tail(n)
    return pd.DataFrame(columns=COLUNAS)


def validar(nome, idade, convenio):
    if not nome or not nome.strip():
        return "Informe o nome do paciente."
    if idade is None or not 0 <= idade <= 120:
        return "Informe uma idade entre 0 e 120 anos."
    if convenio not in CONVENIOS:
        return "Selecione o convênio."
    return None


def cadastrar_paciente(nome, idade, convenio, prioridade, motivo):
    erro = validar(nome, idade, convenio)
    if erro:
        # Mantém o que foi digitado para o usuário corrigir.
        return (f"⚠️ {erro}", carregar_ultimos(),
                nome, idade, convenio, prioridade, motivo)

    linha = {
        "timestamp": datetime.now(FUSO).strftime("%Y-%m-%d %H:%M:%S"),
        "nome": nome.strip(),
        "idade": int(idade),
        "convenio": convenio,
        "prioridade": int(prioridade),
        "motivo": (motivo or "").strip(),
    }
    novo = pd.DataFrame([linha], columns=COLUNAS)
    # Cria o arquivo com cabeçalho na primeira execução; depois só acrescenta linhas.
    if os.path.exists(ARQUIVO_CSV):
        novo.to_csv(ARQUIVO_CSV, mode="a", header=False, index=False)
    else:
        novo.to_csv(ARQUIVO_CSV, mode="w", header=True, index=False)

    # Limpa o formulário para o próximo paciente.
    return (f"✅ Paciente {linha['nome']} cadastrado com sucesso!", carregar_ultimos(),
            "", None, None, 1, "")


with gr.Blocks(title="Cadastro de Pacientes") as demo:
    # Layout em coluna única: funciona bem em telas de celular.
    gr.Markdown("## 🏥 Cadastro de Pacientes\nRegistro rápido de pacientes na recepção do consultório.")
    nome = gr.Textbox(label="Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = gr.Number(label="Idade", precision=0)
    convenio = gr.Dropdown(CONVENIOS, label="Convênio", value=None)
    prioridade = gr.Slider(1, 5, step=1, value=1, label="Prioridade do atendimento",
                           info="1 = rotina · 5 = urgente")
    motivo = gr.Textbox(label="Motivo da consulta / observações", lines=3)
    botao = gr.Button("Cadastrar", variant="primary")
    saida_msg = gr.Textbox(label="Status", interactive=False)
    tabela = gr.Dataframe(label="Últimos pacientes cadastrados", headers=COLUNAS,
                          interactive=False, wrap=True)

    botao.click(
        cadastrar_paciente,
        [nome, idade, convenio, prioridade, motivo],
        [saida_msg, tabela, nome, idade, convenio, prioridade, motivo],
    )
    # Atualiza a tabela sempre que a página é aberta.
    demo.load(carregar_ultimos, None, tabela)

if __name__ == "__main__":
    demo.launch()
