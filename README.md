# Prueba Técnica de Análisis de Datos

## Descripción
Este proyecto consiste en un análisis de datos de campañas comerciales utilizando archivos JSON como fuente de datos. El objetivo es procesar y analizar información sobre conversiones y leads para obtener insights valiosos sobre el rendimiento de las campañas.

## Objetivos del Análisis
1. Calcular la tasa de conversión por fuente de campaña
2. Determinar el porcentaje de leads que se convierten en cada campaña comercial
3. Plantear una solución que permita actualizaciones recurrentes de los datos (no es necesario implementarla)

## Estructura del Proyecto
```
data-assesment/
├── data/           # Directorio para archivos JSON de entrada
├── src/            # Código fuente
└── README.md       # Este archivo
```

## Requisitos Técnicos
- Python 3.8+
- Pandas
- Jupyter Notebook (opcional, para exploración de datos)
- BBDD opcional, se puede usar SQLite, MongoDB, etc.

## Instalación
1. Clonar el repositorio:
```bash
git clone https://github.com/UcademyTech/data-assesment.git
cd data-assesment
```

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Unix/macOS
# o
.\venv\Scripts\activate  # En Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso
1. Colocar los archivos JSON de entrada en el directorio `data/`
2. Ejecutar los scripts de análisis desde el directorio `src/`

## Estructura de la Solución

### 1. Conversión por Fuente de Campaña
- Análisis de las tasas de conversión segmentadas por cada fuente de campaña
- Métricas de rendimiento por canal

### 2. Porcentaje de Conversión de Leads
- Seguimiento de la evolución de leads a lo largo del embudo de conversión
- Análisis porcentual de conversiones exitosas por campaña

### 3. Actualización Recurrente
La solución planteará:
- Scripts automatizados para procesamiento periódico
- Validación de datos de entrada
- Almacenamiento de resultados históricos

## Entregables Esperados
1. Código fuente comentado y documentado
3. Documentación de la solución
4. Resultados y visualizaciones
5. Propuesta de automatización

## Criterios de Evaluación
- Calidad y claridad del código
- Eficiencia en el procesamiento de datos
- Precisión en los cálculos
- Escalabilidad de la solución
- Facilidad de mantenimiento
- Documentación
