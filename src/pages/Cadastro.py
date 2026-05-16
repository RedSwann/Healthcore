import streamlit as st
from structures.lista_pacientes import ListaPacientes

st.set_page_config(layout="wide")

# SESSION STATE
if "lista" not in st.session_state:
    st.session_state.lista = ListaPacientes()

if "editando" not in st.session_state:
    st.session_state.editando = None

lista = st.session_state.lista

st.title("Cadastro de Pacientes")

# ================= NOVO PACIENTE =================
st.subheader("Novo Paciente")

with st.form("form_cadastro"):

    c1, c2, c3, c4, c5 = st.columns(5)

    nome = c1.text_input("Nome")
    cpf = c2.text_input("CPF")
    idade = c3.text_input("Idade")
    telefone = c4.text_input("Telefone")
    deficiencia = c5.selectbox("Portador de deficiência", ["Não", "Sim"])

    salvar = st.form_submit_button("Salvar")

    if salvar:

        if not nome or not cpf or not idade or not telefone:
            st.error("Preencha todos os campos.")

        elif not cpf.isdigit() or len(cpf) != 11:
            st.error("CPF inválido.")

        elif not idade.isdigit():
            st.error("Idade deve ser numérica.")

        else:
            sucesso = lista.inserir(
                nome,
                cpf,
                int(idade),
                telefone,
                deficiencia
            )

            if sucesso:
                st.success("Paciente cadastrado.")
                st.rerun()
            else:
                st.error("CPF já cadastrado.")

# ================= EDIÇÃO =================
if st.session_state.editando:

    paciente = lista.buscar(st.session_state.editando)

    st.divider()
    st.subheader("Editar Paciente")

    with st.form("form_edicao"):

        nome = st.text_input("Nome", paciente.nome)
        idade = st.number_input("Idade", 0, 120, paciente.idade)
        telefone = st.text_input("Telefone", paciente.telefone)
        deficiencia = st.selectbox(
            "Portador de deficiência",
            ["Não", "Sim"],
            index=0 if paciente.deficiencia == "Não" else 1
        )

        col1, col2 = st.columns(2)

        salvar = col1.form_submit_button("Salvar alterações")
        cancelar = col2.form_submit_button("Cancelar")

        if salvar:

            lista.atualizar(
                paciente.cpf,
                nome,
                idade,
                telefone,
                deficiencia
            )

            st.session_state.editando = None
            st.success("Paciente atualizado.")
            st.rerun()

        if cancelar:
            st.session_state.editando = None
            st.rerun()

# ================= LISTAGEM =================
lista.ordenar_por_nome()

st.divider()
st.subheader("Pacientes Cadastrados")

df = lista.dataframe()

if df.empty:
    st.info("Nenhum paciente cadastrado.")
else:

    for _, p in df.iterrows():

        cols = st.columns([2,2,1,2,2,1,1])

        cols[0].write(p["Nome"])
        cols[1].write(p["CPF"])
        cols[2].write(str(p["Idade"]))
        cols[3].write(p["Telefone"])
        cols[4].write(p["Portador de deficiência"])

        if cols[5].button("Editar", key=f"editar_{p['CPF']}"):
            st.session_state.editando = p["CPF"]
            st.rerun()

        if cols[6].button("Excluir", key=f"excluir_{p['CPF']}"):
            lista.remover(p["CPF"])
            st.success("Paciente removido.")
            st.rerun()