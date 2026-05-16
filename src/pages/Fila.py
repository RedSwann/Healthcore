import streamlit as st
from structures.fila_atendimento import FilaAtendimento
from structures.lista_pacientes import ListaPacientes
from structures.pilha_acoes import PilhaAcoes

st.set_page_config(layout="wide")

if "lista" not in st.session_state:
    st.session_state.lista = ListaPacientes()

if "fila" not in st.session_state:
    st.session_state.fila = FilaAtendimento()

if "pilha" not in st.session_state:
    st.session_state.pilha = PilhaAcoes()

lista = st.session_state.lista
fila = st.session_state.fila
pilha = st.session_state.pilha

st.title("Fila de Atendimento - HealthCore")

st.subheader("Adicionar Paciente na Fila")

with st.form("fila_form"):

    cpf = st.text_input("CPF do Paciente")
    nivel = st.selectbox(
        "Nível de Emergência",
        ["Vermelho", "Laranja", "Amarelo", "Verde"]
    )

    enviar = st.form_submit_button("Adicionar")

    if enviar:

        paciente = lista.buscar(cpf)

        if not paciente:
            st.error("Paciente não cadastrado.")
        else:
            ok = fila.adicionar(paciente, nivel)

            if ok:
                pilha.empilhar({
                    "tipo": "adicionar_fila",
                    "paciente": paciente,
                    "nivel": nivel
                })

                st.success("Paciente adicionado à fila.")
                st.rerun()
            else:
                st.error("Paciente já está na fila.")

if st.button("Atualizar fila"):
    fila.atualizar_fila()
    st.rerun()

if st.button("Atender próximo"):

    paciente = fila.atender_proximo()

    if paciente:
        pilha.empilhar({
            "tipo": "atender",
            "paciente": paciente.paciente,
            "nivel": paciente.nivel
        })

        st.success(f"Atendendo: {paciente.paciente.nome}")
        st.rerun()
    else:
        st.info("Fila vazia.")


# =========================
# Método que desfaz ação
# =========================

if st.button("Desfazer última ação"):

    ultima_acao = pilha.desempilhar()

    if not ultima_acao:
        st.warning("Nenhuma ação para desfazer.")

    else:

        tipo = ultima_acao["tipo"]

        # -------------------------
        # DESFAZER ADIÇÃO NA FILA
        # -------------------------
        if tipo == "adicionar_fila":

            cpf = ultima_acao["paciente"].cpf

            fila.remover(cpf)

            st.success("Adição na fila desfeita.")
            st.rerun()

        # -------------------------
        # DESFAZER ATENDIMENTO
        # -------------------------
        elif tipo == "atender":

            paciente = ultima_acao["paciente"]
            nivel = ultima_acao["nivel"]

            fila.adicionar(paciente, nivel)

            st.success("Atendimento desfeito.")
            st.rerun()

        else:
            st.warning("Última ação não pertence à fila.")


st.divider()
st.subheader("Fila de Atendimento")

atual = fila.inicio

if not atual:
    st.info("Fila vazia.")
else:
    i = 1
    while atual:
        st.write(
            f"{i}. {atual.paciente.nome} | "
            f"CPF: {atual.paciente.cpf} | "
            f"Nível: {atual.nivel}"
        )
        atual = atual.proximo
        i += 1