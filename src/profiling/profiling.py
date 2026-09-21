"""Ett paket med funktioner som säkrar csv filen och delar upp kolumntyperna"""

import logging
import pandas as pd

logger = logging.getLogger(__name__)


def input_validator(df: pd.DataFrame) -> None:
    """Säkrar profilering av uppladdad fil med felhantering."""
    if len(df.columns) == 0:
        logger.error("I den uppladdade filen fanns ej kolumner.")
        raise ValueError("I filen fanns ej kolumner.")

    if df.empty:
        logger.error("I den uppladdade filen fanns ej rader.")
        raise ValueError("I filen fanns ej rader.")

    logger.info("Filen validerades: %d rader, %d kolumner.", len(df), len(df.columns))


def col_splitter(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """Delar upp kolumnnamn i numeriska och kategoriska."""
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(exclude="number").columns.tolist()

    logger.debug("Hittade %d numeriska kolumner och %d kategoriska kolumner.",len(numeric_cols),len(categorical_cols))
    return numeric_cols, categorical_cols


def description_numbers(df: pd.DataFrame, numeric_cols: list[str]) -> pd.DataFrame:
    """Grundstatistik (mean, min, max, osv.) för numeriska kolumner."""
    if not numeric_cols:
        logger.debug("Fanns inte numeriska cols att sammanfatta.")
        return pd.DataFrame()

    return df[numeric_cols].describe().T


def composition_categoricals(df: pd.DataFrame, col: str, top_n: int = 10) -> pd.Series:
    """Value count av kategorisk kolumn."""
    logger.debug("Sammanfattar kolumnen %s med begränsning %d rader.", col, top_n)
    return df[col].value_counts().head(top_n)