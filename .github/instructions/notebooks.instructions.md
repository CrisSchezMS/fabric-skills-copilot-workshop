---
applyTo: "**/*.ipynb"
---
# Notebooks distribuibles

- Mantener formato Jupyter nbformat 4.5, kernel `synapse_pyspark` y metadatos sin IDs.
- `execution_count` debe ser null y `outputs` debe estar vacio en todas las celdas.
- No guardar enlaces privados, rutas personales, tokens ni bindings a workspaces.
- Mantener instrucciones iniciales, celda de parametros y notas de reejecucion.
- Cada linea de source debe terminar en salto de linea. No compactar el JSON.
- Los notebooks generados incorporan el codigo de `src/`; no deben importar
  `src`, `tools` ni archivos locales del repositorio cuando se ejecutan en Fabric.
- Modificar las fuentes y ejecutar `python -m tools.build_notebooks`.
- El notebook 01 escribe las tres tablas raw/dimension. La solucion 02 solo lee
  esas tablas y calcula resultados en memoria; no debe persistir tablas nuevas.
- La referencia avanzada 03 solo publica sus tres destinos del contrato analitico
  con autorizacion explicita; por defecto calcula en memoria y nunca sobrescribe.
