import streamlit as st
from ui.menu_cadastro import ui_cadastro
from ui.menu_fila import ui_fila
from ui.menu_historico import ui_historico


def ui_menu():

    # ================= MENU PRINCIPAL =================
    if st.session_state.pagina == "menu":

        st.title("Sistema de Atendimento - HealthCore")

        col1, col2, col3 = st.columns(3)

        if col1.button("Banco de Pacientes", use_container_width=True):
            st.session_state.pagina = "cadastro"
            st.rerun()

        if col2.button("Fila de Atendimento", use_container_width=True):
            st.session_state.pagina = "fila"
            st.rerun()

        if col3.button("Histórico de Ações", use_container_width=True):
            st.session_state.pagina = "historico"
            st.rerun()

    # ================= MENU DE CADASTRO =================
    elif st.session_state.pagina == "cadastro":
        ui_cadastro()

    # ================= MENU DE FILA =================
    elif st.session_state.pagina == "fila":
        ui_fila()
    # ================= MENU DE HISTÓRICO =================
    elif st.session_state.pagina == "historico":
        ui_historico()
