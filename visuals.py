import os

import streamlit as st


def show_form():
    with st.form("user_input_form"):
        st.write("Please enter the patients data here")
        # first row
        col1_1, col1_2 = st.columns(2)

        with col1_1:
            age = st.number_input("Age", min_value=29, max_value=77, step=1)
        with col1_2:
            sex = st.selectbox("Gender", ["Female", "Male"])

        # second row
        col2_1, col2_2 = st.columns(2)

        with col2_1:
            trestbps = st.number_input(
                "Resting Blood Pressure [mm Hg]", min_value=0, max_value=200, step=1
            )
        with col2_2:
            chol = st.number_input(
                "Serum Cholestoral [mg/dl]", min_value=0, max_value=603, step=1
            )

        # third row
        col3_1, col3_2 = st.columns(2)

        with col3_1:
            fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dl", ["True", "False"])

        with col3_2:
            exang = st.selectbox("Exercise induced angina", ["Yes", "No"])

        # fourth row
        col4_1, col4_2 = st.columns(2)

        with col4_1:
            slope = st.selectbox(
                "The slope of the peak exercise ST segment",
                [
                    "upsloping",
                    "flat",
                    "downsloping",
                ],
            )

        with col4_2:
            cp = st.selectbox(
                "Chest Pain Type",
                [
                    "Typical Angina",
                    "Atypical Angina",
                    "Non-Anginal Pain",
                    "Asymptomatic",
                ],
            )

        # fifth row
        col5_1, col5_2 = st.columns(2)

        with col5_1:
            oldpeak = st.number_input(
                "ST depression induced by exercise relative to rest",
                min_value=-2.6,
                max_value=6.2,
                step=0.1,
            )

        with col5_2:
            thalach = st.number_input(
                "Maximum heart rate achieved", min_value=60, max_value=202, step=1
            )

        col6_1 = st.columns(1)[0]
        with col6_1:
            restecg = st.selectbox(
                "Resting electrocardiographic results",
                [
                    "normal",
                    "having ST-T wave abnormality",
                    "showing probable or definite left ventricular hypertrophy by Estes' criteria",
                ],
            )

        # Submit button for the form
        submitted = st.form_submit_button("Submit")
        if submitted:
            result = {
                "age": age,
                "sex": sex,
                "chest pain type": cp,
                "resting bp s": trestbps,
                "cholesterol": chol,
                "fasting blood sugar": fbs,
                "resting ecg": restecg,
                "max heart rate": thalach,
                "exercise angina": exang,
                "oldpeak": oldpeak,
                "ST slope": slope,
            }
            st.session_state["result"] = result


def show_result(confidence: float, max_index: int):
    os.write(1, f"Confidence: {confidence}\n".encode())
    os.write(1, f"Max Index: {max_index}\n".encode())
    os.write(1, "\n".encode())
    confidence = round(confidence * 100, 1)

    st.write("")
    st.write("")

    classification = "Heart Disease" if max_index == 1 else "No Heart Disease"

    # Displaying a colored box based on the prediction value
    text = f"{classification} detected with a probability of {confidence}%"

    if max_index == 0 and confidence > 90:
        st.markdown(
            f"<div style='background-color: green; color: white; padding: 10px;'>{text}</div>",
            unsafe_allow_html=True,
        )
    elif max_index == 1 and confidence > 85:
        st.markdown(
            f"<div style='background-color: red; color: white; padding: 10px;'>{text}</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='background-color: yellow; color: black; padding: 10px;'>{text}</div>",
            unsafe_allow_html=True,
        )
