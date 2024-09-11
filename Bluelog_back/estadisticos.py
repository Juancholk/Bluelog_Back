import pandas as pd
def generate_statistics():
    try:
        # Obtener todos los datos de WaveData
        df = pd.read_csv('example.csv')
        df = df.rename(columns={'Date': 'date', 'Time': 'time', 'Wave Height (m)': 'wave_height', 'Wave Period (s)': 'wave_period', 'Wave Direction (°)': 'wave_direction'})
        
        # Calcular estadísticas descriptivas
        statistics = df.describe()
        statistics = statistics.round(2)
        
        # Renombrar los índices (primera columna)
        Estadisticos = statistics.rename(index={
            'count': 'Conteo',
            'mean': 'Media',
            'std': 'Desviación',
            'min': 'Mínimo',
            '25%': 'percentil_25',
            '50%': 'Mediana',
            '75%': 'Percentil_75',
            'max': 'Máximo'
        })

        print(Estadisticos)

        # Convertir las estadísticas a formato JSON y devolverlas
        return Estadisticos.to_dict()

    except Exception as e:
        raise ValueError(f"Error generating statistics: {str(e)}")
