import pandas as pd
import pytest

from profiling.profiling import (
    input_validator,
    col_splitter,
    description_numbers,
    composition_categoricals
)


def test_inputvalidator_onlycolumns():
    onlycolumns_df = pd.DataFrame(columns=['location', 'revenue'])
    with pytest.raises(ValueError, match='inga rader'):
        input_validator(onlycolumns_df)


def test_inputvalidator_nocols():
    with pytest.raises(ValueError, match='inga kolumner'):
        input_validator(pd.DataFrame())


def test_col_splitter():
    df = pd.DataFrame({"location":['nw','sw','se'],"revenue":[25.0, 50.0, 75.0]})
    numeric_cols, categorical_cols = col_splitter(df)
    assert numeric_cols == ["revenue"]
    assert categorical_cols == ["location"]


def test_descriptionnumbers_gives_pd_describe():
    df = pd.DataFrame({"revenue":[25.0, 50.0, 75.0]})
    result = description_numbers(df, ["revenue"])
    assert result.loc['revenue', 'min'] == 25.0
    assert result.loc['revenue', 'max'] == 75.0
    assert result.loc['revenue', 'count'] == 3
    assert result.loc['revenue', 'mean'] == pytest.approx(50.0)


def test_descriptionnumbers_gives_empty_onlycategorical():
    df = pd.DataFrame({"location":['nw','sw']})
    result = description_numbers(df, [])
    assert result.empty


def test_compositioncategoricals_countvalues():
    df = pd.DataFrame({"location":['nw','sw','nw','se']})
    result = composition_categoricals(df, "location")
    assert result['nw'] == 2
    assert result['sw'] == 1
    assert result['se'] == 1


def test_compositioncategoricals_limitrows():
    df = pd.DataFrame({"category":['x','y','z','x','x']})
    result = composition_categoricals(df, "category", top_n=2)
    assert len(result) == 2
    assert result.index[0] == "x"
    assert result.iloc[0] == 3