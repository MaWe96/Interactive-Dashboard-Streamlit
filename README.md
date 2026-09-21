# Data Profiling med Streamlit
Pythonfördjupning i interaktiv streamlit med inslag av dashboard-design, logging och testing. Lärdomar i hur lokalt körd Python-webbflik skiljer sig från webbutveckling framkommer.

## Vad dashboard.py gör
Användare lägger in en csv och får tabeller och visualer som går att filtra genom drop-down menyer. Hur mycket filtrande som användaren görs visas i en counter. Logikmotorn *profiling*, tester och logging sköts utanför, enligt arbetets struktur.

## Installation
Hämta ner github repo, navigera till mappen och enable virtuell miljö, följt av `pip install -e .` (anpassningsbar installation igenom *.toml*)

## Biblioteksberoenden
1. `Streamlit`
2. `Pandas`
3. `pyproject.toml` detaljerar mer.

## Hur appen körs
Kör följande i terminal inuti repo: `streamlit run dashboard.py`, då öppnas webbflik med interaktiva dashboarden.

För pytest, kör i terminal `pytest`.

## Data
Behandling av data från csv görs allmän genom Pandas *select_dtypes*. Valt dataset är *IBM HR Analytics Employee Attrition & Performance* hämtat ifrån Kaggle.

## Arbetets struktur
**1. Mapp: src**

**1.1 mapp: profiling**
1. `__init__.py`
2. `logger_config.py`
3. `profiling.py`

**2. pyproject.toml**

**3. report.pdf**

**4. README.md**

**5. dashboard.py**

**6. Mapp: tests**

**6.1 test_profiling.py**

## Begränsningar
Upload stödjer bara .csv, analysen är på beskrivande nivå, felhantering missar edge cases och arbetet körs på lokal maskin.
