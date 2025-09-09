"""
ui.py
Modulo para la interaccion del usuario en la linea de comandos.
"""

from tabulate import tabulate


def get_user_input() -> tuple:
    
    # Input para el filtro de departamento, municipio, cultivo y número de registros.
    department = input("Ingrese el departamento: ")
    municipality = input("Ingrese el municipio: ")
    crop = input("Ingrese el cultivo: ")

    # Extrae los digitos en el caso de '5 registros'
    raw_input = input("Ingrese el número de registros a consultar: ")
    n_records = int("".join(filter(str.isdigit, raw_input)))

    return department, municipality, crop, n_records


def show_table(df, medians: dict) -> None:
    
    # Display filtered records and summary with medians.
    if df.empty:
        print("No se encontraron resultados.")
        return

    # Mostrar registros filtrados
    print("\nRegistros filtrados:")
    # Solo mostramos columnas principales
    print(tabulate(
        df[["Departamento", "Municipio", "Cultivo", "Topografia"]],
        headers="keys",
        tablefmt="grid"
    ))

    # Mostrar resumen con medianas
    if not medians:
        print("\nNo se encontraron datos válidos para calcular medianas.")
        return

    row = [
        df["Departamento"].iloc[0],
        df["Municipio"].iloc[0],
        df["Cultivo"].iloc[0],
        df["Topografia"].iloc[0],
    ]

    # Agregar valores de medianas
    for var in ["pH", "Phosphorus", "Potassium", "Aluminum", "Calcium", "Sodium", "Zinc"]:
        row.append(medians.get(var, "N/A"))

    headers = [
        "Departamento", "Municipio", "Cultivo", "Topografía",
        "pH (Mediana)", "Fósforo (Mediana)", "Potasio (Mediana)",
        "Aluminio (Mediana)", "Calcio (Mediana)", "Sodio (Mediana)", "Zinc (Mediana)"
    ]

    print("\nResumen estadístico (medianas):")
    print(tabulate([row], headers=headers, tablefmt="grid"))
