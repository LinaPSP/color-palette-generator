# 🎨 Generador de Paletas de Colores

Aplicación web desarrollada con Python y Streamlit que genera paletas de colores armónicas a partir de un color base.

## Características

- 5 esquemas de armonía: Monocromática, Análoga, Complementaria, Triádica y Complementaria dividida
- Selector de color base con vista previa en tiempo real
- Control de cantidad de colores (3 a 6)
- Texto adaptativo (claro u oscuro) según la luminancia de cada color
- Exportación de la paleta como variables CSS

## Instalación

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Uso

1. Selecciona un color base en la barra lateral
2. Elige el esquema de armonía
3. Ajusta la cantidad de colores con el slider
4. Copia los códigos HEX o descarga el archivo `palette.css`

## Tecnologías

- Python 3.12
- Streamlit
- `colorsys` (biblioteca estándar)
