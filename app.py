import streamlit as st

from model import ModelWrapper
from visuals import show_disclaimer, show_form, show_result

st.set_page_config(page_title="CDSS")

if not st.session_state.get("model"):
    st.session_state["model"] = ModelWrapper()

if "disclaimer_displayed" not in st.session_state:
    st.session_state["disclaimer_displayed"] = False

if not st.session_state["disclaimer_displayed"]:
    show_disclaimer()
else:
    st.title("Heart Disease Prediction")
    show_form()
    if st.session_state.get("result"):
        # get model and result from session state
        model = st.session_state["model"]
        result = st.session_state["result"]

        # Predicting the output
        # has to return a number between 0 and 1
        confidence, max_index = model.predict(result)

        show_result(confidence, max_index)
