import streamlit as st
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
 
 
# Prompt Template
template = """
    Tu es un professeur de sciences au lycée. Sois clair, concis et pédagogue.
    Explique les réponses en utilisant des exemples simples et un langage adapté aux élèves de 16 ans.
 
    Voici des informations tirées d'un document fourni par l'utilisateur :
    {doc_context}
 
    Voici l'historique de la conversation :
    {chat_context}
 
    Question : {question}
 
    Réponse :
"""
# Langchain Setup
model = OllamaLLM(model = "mistral")
prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
 
 
# Streamlit UI
st.set_page_config(page_title= "🏫 Alexandra- prof de Teccart", layout="centered")
st.title("👩🏻‍🏫 Alexandra, Prof de Teccart")
 
# session state initialisation
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""
 
with st.sidebar:
    st.header("Charger un document")
    uploaded = st.file_uploader("PDF ou Docx :", type=["pdf","docx"])
    if uploaded:
        ext = uploaded.name.lower().split(".")[-1]
        if ext == "pdf":
            from pypdf import PdfReader
            reader = PdfReader(uploaded)
            text = "\n".join(p.extract_text() or "" for p in reader.pages)
        if ext == "docx":
            import docx
            doc = docx.Document(uploaded)
            text = "\n".join(p.text for p in doc.paragraphs)
        st.session_state.doc_text = text.strip()[:20_000]
        st.success(" Document charger avec succes, vous pouvez poser vos questions.")
 
 
# Afficher l'historique
 
for speaker , msg in st.session_state.chat_history:
    prefix = "🧑‍🎓" if speaker == "Vous" else "👩‍🏫"
    st.markdown(f"**{prefix} {speaker}** :{msg}")
 
user_input = st.chat_input("pose ta question...")
 
if user_input:
    with st.spinner("Alexandra reflechit..."):
        result = chain.invoke({
            "doc_context" : st.session_state.doc_text or "(aucun document)",
            "chat_context" : "\n".join(
                f"{s}: {m}" for s,m in st.session_state.chat_history
            ), "question" : user_input
        })
 
    # Memoriser l'echange
    st.session_state.chat_history.append(("Vous", user_input))
    st.session_state.chat_history.append(("Alexandra", result))
    st.rerun()
 