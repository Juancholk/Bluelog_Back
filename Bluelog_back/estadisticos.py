import pandas as pd
def generate_statistics():
    try:
        # Obtener todos los datos de WaveData
        df = pd.read_csv('example.csv')
        df = df.rename(columns={'Date': 'date', 'Time': 'time', 'Wave Height (m)': 'wave_height', 'Wave Period': 'Wave Period (s)', 'Wave Direction (°)': 'wave_direction'})
        # Crear un DataFrame con los datos

        # Calcular estadísticas descriptivas
        statistics = df.describe()
        statistics = statistics.round(2)
        print(statistics)
        # Convertir las estadísticas a formato JSON y devolverlas
        return statistics.to_dict()
    
    except Exception as e:
        raise ValueError(f"Error generating statistics: {str(e)}")
