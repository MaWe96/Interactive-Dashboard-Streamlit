"""Data Profiling i Streamlit. Användare får interaktiv dashboard från uppladdad CSV."""

import logging
import pandas as pd
import streamlit as st

from profiling.logger_config import logger_configure
from profiling.profiling import (
    input_validator,
    col_splitter,
    description_numbers,
    composition_categoricals
)

TOP_N_CATEGORIES = 10
FILTER_COL_KEY = "filter_col_select"
FILTER_VALUE_KEY = "filter_value_select"
CHART_COL_KEY = "chart_col_select"

logger_configure()
logger = logging.getLogger("profiler.dashboard")


st.title("Data Profiling i Streamlit")

user_uploaded = st.file_uploader("Var god dra in eller bläddra fram en CSV", type="csv")

if user_uploaded is not None:
    try:
        df = pd.read_csv(user_uploaded)
        input_validator(df)
    except pd.errors.ParserError:
        logger.error("Error; uppladdad fil (%s) är inte CSV.", user_uploaded.name)
        st.error("Uppladdad fil är inte CSV; pröva riktig CSV.")
        st.stop()
    except ValueError as e:
        logger.error("Fil (%s) är inte giltig: %s", user_uploaded.name, e)
        st.error(f"Uppladdad fil gick inte att använda: {e}")
        st.stop()

    logger.info("Läst in %s (%d rad, %d kolumn)",user_uploaded.name,len(df),len(df.columns))

    numeric_cols, categorical_cols = col_splitter(df)


    st.subheader("Filtrera data") # ändrar alla visualer

    if categorical_cols:
        filter_col = st.selectbox("Filtrera på kolumn",categorical_cols,key=FILTER_COL_KEY)

        # från widget behavior docs. välj värde blir Alla när kolumnfiltret byts
        value_key = f"{FILTER_VALUE_KEY}_{filter_col}"
        sorted_options = sorted(df[filter_col].dropna().unique().tolist())
        options = ["Alla"] + sorted_options
        user_selectvalue = st.selectbox("Välj värde", options, key=value_key)

        filtered_df = df if user_selectvalue == "Alla" else df[df[filter_col] == user_selectvalue]
    else:
        filter_col = None
        user_selectvalue = None
        filtered_df = df


    filter_signature = (filter_col, user_selectvalue) # för user interact counting

    if "last_filter_signature" not in st.session_state:
        st.session_state.last_filter_signature = None
        st.session_state.filter_changes = 0

    if filter_signature != st.session_state.last_filter_signature:
        st.session_state.filter_changes += 1
        st.session_state.last_filter_signature = filter_signature
        logger.debug("Användaren bytte filter; %s.", filter_signature)

    st.caption(f"Du har visat filter {st.session_state.filter_changes} gånger denna session")
    st.write(f"Visar {len(filtered_df)} av {len(df)} rader")


    st.subheader("Överblick av data") # ändrar utefter huvudfiltret
    st.dataframe(filtered_df.head())

    st.subheader("Grundläggande numerisk statistik")
    described_numbers = description_numbers(filtered_df, numeric_cols)
    st.dataframe(described_numbers) # kan bli  tabell utan rader

    st.subheader("Kategorisk fördelning")
    if categorical_cols:
        users_categor = st.selectbox("Filtrera en kolumn",categorical_cols,key=CHART_COL_KEY)
        st.bar_chart(composition_categoricals(filtered_df, users_categor, top_n=TOP_N_CATEGORIES)
        )