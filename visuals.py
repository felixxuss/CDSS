import os

import streamlit as st

pre_idx = 2

pre_vals = {
    "age": [37, 37, 49],
    "sex": [1, 1, 0],
    "chest pain type": [1, 3, 2],
    "resting bp s": [130, 140, 160],
    "cholesterol": [283, 207, 180],
    "fasting blood sugar": [1, 1, 1],
    "resting ecg": [1, 0, 0],
    "max heart rate": [98, 130, 156],
    "exercise angina": [1, 0, 1],
    "oldpeak": [0.0, 1.5, 1.0],
    "ST slope": [0, 1, 1],
}


def show_form():
    with st.form("user_input_form"):
        st.write("Please enter the patients data here")
        # first row
        col1_1, col1_2 = st.columns(2)

        with col1_1:
            age = st.number_input(
                "Age",
                min_value=29,
                max_value=77,
                step=1,
                value=pre_vals["age"][pre_idx],
            )
        with col1_2:
            sex = st.selectbox(
                "Gender", ["Female", "Male"], index=pre_vals["sex"][pre_idx]
            )

        # second row
        col2_1, col2_2 = st.columns(2)

        with col2_1:
            trestbps = st.number_input(
                "Resting Blood Pressure [mm Hg]",
                min_value=0,
                max_value=200,
                step=1,
                value=pre_vals["resting bp s"][pre_idx],
            )
        with col2_2:
            chol = st.number_input(
                "Serum Cholestoral [mg/dl]",
                min_value=0,
                max_value=603,
                step=1,
                value=pre_vals["cholesterol"][pre_idx],
            )

        # third row
        col3_1, col3_2 = st.columns(2)

        with col3_1:
            fbs = st.selectbox(
                "Fasting Blood Sugar > 120 mg/dl",
                ["True", "False"],
                index=pre_vals["fasting blood sugar"][pre_idx],
            )

        with col3_2:
            exang = st.selectbox(
                "Exercise induced angina",
                ["Yes", "No"],
                index=pre_vals["exercise angina"][pre_idx],
            )

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
                index=pre_vals["ST slope"][pre_idx],
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
                index=pre_vals["chest pain type"][pre_idx],
            )

        # fifth row
        col5_1, col5_2 = st.columns(2)

        with col5_1:
            oldpeak = st.number_input(
                "ST depression induced by exercise relative to rest",
                min_value=-2.6,
                max_value=6.2,
                step=0.1,
                value=pre_vals["oldpeak"][pre_idx],
            )

        with col5_2:
            thalach = st.number_input(
                "Maximum heart rate achieved",
                min_value=60,
                max_value=202,
                step=1,
                value=pre_vals["max heart rate"][pre_idx],
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
                index=pre_vals["resting ecg"][pre_idx],
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


def show_disclaimer():
    st.markdown(
        """
        <div>
            <h1>Disclaimer</h1>
            <p>This Clinical Decision Support System (CDSS) for heart disease prediction is designed to assist healthcare professionals in evaluating the risk of heart disease in patients. It is intended to be used exclusively by licensed medical professionals who have the requisite knowledge and expertise to interpret and utilize the information provided.
                <h3>Important Notice</h3>
                <h5>Advisory Nature</h5>
                The predictions and recommendations generated by this CDSS are advisory and are not intended to replace professional clinical judgment. All diagnostic and treatment decisions should be made by a healthcare professional, considering the unique characteristics and medical history of each patient.
                <br><br>
                <h5>Limitations of the System</h5>
                While this CDSS uses advanced algorithms to provide predictions, no model can guarantee complete accuracy. There is always the potential for errors or omissions. The system should be used as one of many tools in the clinical decision-making process.
                <br><br>
                <h5>User Responsibility</h5>
                The user is responsible for the interpretation and application of the information provided by the CDSS. The developers and providers of this system assume no liability for any outcomes resulting from its use.
                <br><br>
                <h5>Patient Data Security</h5>
                Users must ensure that all patient data entered into the CDSS is handled in accordance with relevant data protection laws and regulations. Appropriate measures should be taken to protect patient confidentiality and privacy.
                <br><br><br>
                By using this CDSS, you acknowledge that you have read, understood, and agree to the terms outlined in this disclaimer. Always use this system with caution and in conjunction with professional medical expertise.</p>
                </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("Understood"):
        st.session_state["disclaimer_displayed"] = True
