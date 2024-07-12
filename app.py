import streamlit as st

from model import ModelWrapper
from visuals import show_form, show_result

st.set_page_config(page_title="CDSS")
st.title("Heart Disease Prediction")

if not st.session_state.get("model"):
    st.session_state["model"] = ModelWrapper()

show_form()

if st.session_state.get("result"):
    # get model and result from session state
    model = st.session_state["model"]
    result = st.session_state["result"]

    # Predicting the output
    # has to return a number between 0 and 1
    confidence, max_index = model.predict(result)

    show_result(confidence, max_index)
