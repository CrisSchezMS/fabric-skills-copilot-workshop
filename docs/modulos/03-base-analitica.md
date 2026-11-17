# 03 - Crear una base analitica reutilizable con Spark

**Objetivo:** dejar de calcular solo en memoria y crear una base que puedan
consumir Power BI, ontologia y aplicaciones. Usa `spark-cli`, no T-SQL para
escribir en el Lakehouse.

## Preparacion y entregables

Necesitas las tres tablas del notebook 01 y un Lakehouse dedicado. Lee
[el contrato original](../datos.md) y [el analitico](../contrato-analitico.md).
Los destinos propuestos son `workshop_sales_clean`, `workshop_sales_daily`
y `workshop_calendar`. No se modifica ninguna tabla original.

## Reto y prompts

Primero pide un diseno, sin consultar Fabric:

```text
Usa spark-cli. Lee docs/datos.md y docs/contrato-analitico.md.
Disena las tres tablas derivadas: granularidad, claves, tipos y consumidores.
Explica por que no se debe unir el agregado al detalle para sumar ingresos.
Prepara celdas que comprueben Lakehouse y esquema, validen los tipos de origen,
limpien en memoria y reconcilien detalle y agregado. No ejecutes ni escribas.
No abras soluciones/ todavia.
```

Revisa el codigo antes de decidir si vas a ejecutarlo manualmente. Despues:

```text
Prepara una celda de publicacion desactivada por defecto. Debe listar los tres
destinos, comprobarlos TODOS antes de escribir, fallar si cualquiera existe
y usar Delta con errorifexists. No incluyas overwrite, borrado ni CREATE SCHEMA.
Despues de guardar, compara recuentos, unidades e ingresos exactos con la entrada.
Explica que un fallo intermedio no se revierte automaticamente. No ejecutes.
```

## Trabajo en Fabric

1. Abre un notebook PySpark con el Lakehouse del generador como predeterminado.
2. Confirma su esquema y las columnas/tipos reales. No corrijas un destino
   desconocido creando otro esquema.
3. Ejecuta perfilado y limpieza en memoria con las reglas acordadas.
4. Construye el agregado por fecha, producto, tienda y canal, y un calendario
   diario continuo con los anios completos observados.
5. Compara los totales con el informe del notebook 01. Si cambiaste parametros,
   ese informe prevalece sobre el JSON de referencia del repositorio.
6. Revisa destinos y autoriza la escritura solo entonces. Lee las tablas
   guardadas y reconcilia otra vez.

## Comprobaciones y cierre

El detalle debe tener `sale_id` unico, claves validas, cantidades positivas,
estado completed y categoria/ciudad canonicas. Las copias no aumentan ingresos.
La suma de `sales_count`, `units` y `net_revenue` debe coincidir con el detalle.
El calendario no puede tener dias repetidos ni saltos.

Reejecutar la publicacion debe detenerse antes de escribir si existe alguno
de los destinos. No lo compruebes activando sobrescritura. Una publicacion
parcial exige revision, no limpieza automatica.

**Cierre:** puedes mostrar el linaje original -> detalle -> agregado y explicar
la granularidad de cada tabla sin confundir filas, unidades y pedidos.

**Referencia, solo despues del intento:** pide abrir
`soluciones/03_publicar_analitica.ipynb`. Es autonomo, incorpora las funciones
de limpieza y viene con `SCHEMA = None` y `WRITE_ANALYTICS = False`.
