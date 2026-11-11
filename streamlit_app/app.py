"""Cadastro de Pacientes - versão Streamlit (deploy no Streamlit Community Cloud).

Executar localmente com:  streamlit run streamlit_app/app.py

O sistema de arquivos do Streamlit Community Cloud é efêmero, então:
- os pacientes da sessão ficam em st.session_state;
- cada cadastro também é gravado em pacientes.csv (mesma lógica da versão Gradio),
  mas esse arquivo pode sumir quando o app reinicia;
- o botão "Baixar CSV" exporta os dados cadastrados na sessão.
"""
import os
from datetime import datetime
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_CSV = os.path.join(PASTA, "pacientes.csv")
COLUNAS = ["timestamp", "nome", "idade", "convenio", "prioridade", "motivo"]
CONVENIOS = ["Particular", "Unimed", "Bradesco Saúde", "SulAmérica", "Outro"]
FUSO = ZoneInfo("America/Sao_Paulo")


def gravar_csv(linha):
    """Acrescenta uma linha ao CSV, criando o arquivo com cabeçalho se ele não existir."""
    novo = pd.DataFrame([linha], columns=COLUNAS)
    existe = os.path.exists(ARQUIVO_CSV)
    novo.to_csv(ARQUIVO_CSV, mode="a" if existe else "w", header=not existe, index=False)


st.set_page_config(page_title="Cadastro de Pacientes", page_icon="🏥", layout="centered")
st.title("🏥 Cadastro de Pacientes")
st.caption("Registro rápido de pacientes na recepção do consultório.")

if "pacientes" not in st.session_state:
    st.session_state.pacientes = pd.DataFrame(columns=COLUNAS)

with st.form("cadastro", clear_on_submit=True):
    nome = st.text_input("Nome do paciente", placeholder="Ex.: Maria da Silva")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    convenio = st.selectbox("Convênio", CONVENIOS, index=None, placeholder="Selecione...")
    prioridade = st.slider("Prioridade do atendimento", 1, 5, help="1 = rotina · 5 = urgente")
    motivo = st.text_area("Motivo da consulta / observações")
    enviado = st.form_submit_button("Cadastrar", type="primary", width="stretch")

if enviado:
    if not nome.strip():
        st.error("Informe o nome do paciente.")
    elif convenio is None:
        st.error("Selecione o convênio.")
    else:
        nova_linha = {
            "timestamp": datetime.now(FUSO).strftime("%Y-%m-%d %H:%M:%S"),
            "nome": nome.strip(),
            "idade": int(idade),
            "convenio": convenio,
            "prioridade": int(prioridade),
            "motivo": motivo.strip(),
        }
        st.session_state.pacientes = pd.concat(
            [st.session_state.pacientes, pd.DataFrame([nova_linha], columns=COLUNAS)],
            ignore_index=True,
        )
        gravar_csv(nova_linha)
        st.success(f"Paciente {nova_linha['nome']} cadastrado!")

st.subheader("Últimos pacientes cadastrados")
total = len(st.session_state.pacientes)
st.caption(f"{total} paciente(s) cadastrado(s) nesta sessão.")
st.dataframe(st.session_state.pacientes.tail(5), hide_index=True, width="stretch")

csv = st.session_state.pacientes.to_csv(index=False).encode("utf-8")
st.download_button("Baixar CSV", csv, "pacientes.csv", "text/csv",
                   disabled=total == 0, width="stretch")
