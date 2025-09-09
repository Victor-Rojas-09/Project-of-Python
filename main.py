"""
main.py
Archivo principal que orquesta la ejecucion del proyecto.
"""

from api import load_data, filter_data, compute_median
from ui import get_user_input, show_table

def main():
    # Main: carga, filtra, and muestra los resultados.
    path = "venv/resultado_laboratorio_suelo.xlsx"
    data = load_data(path)

    if data.empty:
        print("No se pudo cargar la informacion.")
        return

    department, municipality, crop, n_records = get_user_input()
    filtered = filter_data(data, department, municipality, crop, n_records)
    medians = compute_median(filtered)
    show_table(filtered, medians)


if __name__ == "__main__":
    main()
