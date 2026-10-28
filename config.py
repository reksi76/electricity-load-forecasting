from pathlib import Path 

PROJECT_DIR = Path(__file__).resolve().parent

DATA_PATH = (
        PROJECT_DIR
        /'data'
        /'raw'
        /'Tetuan City power consumption.csv'
        )

FIGURES_DIR = PROJECT_DIR/'outputs'/'figures'
EVALUATIONS_DIR = PROJECT_DIR/'outputs'/'evaluations'

FIGURES_DIR.mkdir(parents=True, exist_ok=True)
EVALUATIONS_DIR.mkdir(parents=True, exist_ok=True)
