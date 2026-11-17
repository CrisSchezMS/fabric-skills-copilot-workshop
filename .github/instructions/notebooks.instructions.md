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
- El notebook 01 es el unico distribuido; conservarlo y mantener su generacion
  con `python -m tools.build_notebooks`.
- El notebook operativo se compone desde `src/` y
  `tools/build_deployment_notebook.py` fuera del repo. Puede contener bindings
  privados en el despliegue, nunca en los archivos publicados.
- Tras aprobar el alcance, Copilot lo crea, vincula, ejecuta y verifica en Fabric.
  Publica los tres destinos del contrato analitico sin flag desactivado.
  Conserva las comprobaciones previas de todos los destinos y nunca sobrescribe.
