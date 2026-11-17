# 03 - Copilot crea y ejecuta la base analitica con Spark

**Entrega:** item `workshop_03_base_analitica` ejecutado y tablas
`workshop_sales_clean`, `workshop_sales_daily`, `workshop_calendar` publicadas.
No se queda en un DataFrame ni en un notebook con escritura desactivada.

Completa descubrimiento y aprobacion del [runbook](../despliegue.md).
Usa `spark-cli`, modo authoring, con sus referencias de notebook/API.
Los origenes y destinos estan en los contratos
[original](../datos.md) y [analitico](../contrato-analitico.md).

## Encargo ejecutable

```text
Ejecuta el modulo 03 en el workspace/Lakehouse ya descubiertos y aprobados.
Usa spark-cli en modo authoring. Conserva el notebook generador y las fuentes.
Comprueba que no existe workshop_03_base_analitica ni ninguna de las tres
tablas derivadas. Genera el notebook autonomo con tools/build_deployment_notebook.py
en una ruta privada fuera del repo; usa el esquema e ID del Lakehouse reales.
Crea el item Notebook con su definicion, configura ese Lakehouse como
predeterminado y relee el binding antes de arrancar el job.
Ejecutalo, sigue el job hasta estado final y lee sus resultados.
No respondas solo con el codigo: quiero las tablas persistidas y verificadas.
```

Copilot rellena los argumentos del constructor; no te pide IDs.
El archivo local no se sube a Git. La API y formato de definicion del notebook
se toman de la skill instalada, no del JSON de una plantilla de diseno.

## Que hace el notebook al ejecutarse

1. Verifica el Lakehouse esperado y columnas/tipos reales de las tres fuentes.
2. Perfila filas raw, sale_id distintos no nulos, contenidos distintos, copias,
   conflictos, nulos, cantidades no positivas y claves huerfanas.
3. Muestra incidencias tanto raw como sobre filas sin copias. Estas ultimas
   solo equivalen a ventas unicas si no hay conflictos; nunca se suman para
   calcular rechazos porque pueden solaparse.
4. Comprueba dimensiones, quita copias exactas y detiene sale_id nulo/conflictivo.
   Limpia con dimensiones canonicas, completed, cantidad positiva y claves validas.
5. Calcula importe decimal con redondeo por linea, agregado y calendario.
   Reconcilia lineas, unidades e ingresos antes de guardar.
6. Comprueba los tres destinos antes de cualquier escritura, usa Delta
   `errorifexists`, relee las tablas y repite reconciliacion.

La autorizacion se obtiene **antes del arranque**. El notebook operativo
publica directamente cuando se ejecuta; no exige editar un flag y relanzarlo.
Los helpers de bajo nivel conservan su proteccion de aprobacion.

## Aceptacion y continuidad

Compara con el informe observado del generador. El calendario debe cubrir
anios completos y dias contiguos; sale_id debe ser unico; no hay lineas
canceladas, cantidades invalidas ni claves sin dimension en el detalle.
Verifica el estado final del job y existencia/lectura de las tres tablas,
no solo el mensaje de publicacion.

Una segunda ejecucion de publicacion debe bloquearse por destinos existentes.
No la lances como prueba en vivo sin necesidad: ya es una proteccion local
probada. Ante carga parcial, sigue la reanudacion del runbook, sin borrar.

Continua con [modelo e informe](05-modelo-informe.md) y
[ontologia](06-ontologia.md). No ejecutes despues Osmos sobre estos destinos.
