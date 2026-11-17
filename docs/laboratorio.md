# Laboratorio: de una pregunta a una transformacion revisable

Ejecuta antes el notebook 01 en Fabric. En Copilot abre la raiz del repositorio.
No abras la solucion al principio. Los bloques siguientes son prompts copiables,
no comandos que se ejecuten por si solos.

## 1. Separar instrucciones, skills y herramientas

```text
Estoy empezando con Copilot. Lee .github/copilot-instructions.md y docs/datos.md.
Explica que aportan las instrucciones del repo, la skill local workshop-ventas
y las Microsoft Fabric Skills oficiales. Indica cuales tienes disponibles y
si realmente puedes acceder a mi Fabric. No ejecutes ni modifiques nada.
```

Resultado esperado: una explicacion basada en archivos y capacidades reales.
No basta con que Copilot diga que conoce Fabric: debe distinguir tener
instrucciones de disponer de herramientas conectadas y permisos.

## 2. Perfilar antes de limpiar

```text
Usa la Fabric Skill spark-cli si esta instalada. A partir del contrato de datos,
propone celdas PySpark para perfilar las tablas del taller en mi Lakehouse
predeterminado. Comprueba primero el esquema. Necesito recuento raw, ventas
distintas, copias, nulos, cantidades invalidas y productos huerfanos.
Distingue ventas unicas de incidencias raw y no inventes cifras.
Solo prepara la propuesta: no consultes ni modifiques mi entorno.
```

Revisa los nombres y ejecuta manualmente las celdas aprobadas en un notebook de
Fabric con el mismo Lakehouse. Si decides usar herramientas conectadas, autoriza
por separado el alcance de solo lectura y confirma el destino.

## 3. Acordar las reglas

```text
Propone un plan de limpieza para estos datos. Que filas se recuperan con las
dimensiones y cuales se excluyen? Como evitas contar dos veces una venta?
Que haces si hay dos versiones diferentes de un sale_id? Explica el descuento,
el uso de decimal y cuando se redondea. No generes ni ejecutes cambios todavia.
```

Compara con `docs/datos.md`. No aceptes eliminar todas las filas con nulos ni
elegir una version arbitraria de una venta con contenido distinto.

## 4. Generar y revisar codigo

```text
Con las reglas acordadas y usando spark-cli si esta disponible, genera las
celdas PySpark para crear un DataFrame sales_clean en memoria. Usa la sesion
spark existente. No alteres las tablas raw, no instales paquetes ni guardes
tablas nuevas. Anade comprobaciones de claves, unicidad e ingresos. Explica
como ejecutarlo manualmente en Fabric; no lo ejecutes desde este chat.
```

Ejecuta el codigo revisado en Fabric. Compara el resultado con el informe del
notebook 01; con parametros originales tambien con `docs/expected-results.json`.
Los ingresos deben coincidir exactamente a dos decimales, no aproximadamente.

## 5. Contrastar con T-SQL (opcional)

```text
Usa sqldw-cli si esta disponible y revisa los ejemplos de sql/. Explica por que
se ejecutan en el SQL analytics endpoint y no como Spark SQL. Antes del resumen,
comprueba las consultas de validacion de claves. No ejecutes SQL desde el chat.
```

En el SQL analytics endpoint del Lakehouse:

1. Ejecuta `sql/01_descubrir_tablas.sql` y confirma el esquema.
2. Selecciona y ejecuta cada consulta de `sql/02_perfilado.sql` por separado.
3. Ejecuta cada consulta de `sql/03_validar_claves.sql`: deben devolver cero filas.
   Si alguna devuelve filas, detente antes del resumen.
4. Ejecuta `sql/04_ventas_por_categoria.sql` y compara los ingresos.

Los ejemplos suponen `dbo`. Si descubriste otro esquema, revisalos antes de usar.
En un cliente MCP que solo devuelve el ultimo resultado del lote, enviar varias
SELECT juntas puede ocultar los primeros resultados.

## Cierre

Explica con tus palabras que hizo Copilot, que aporto la skill y que tuviste
que verificar. Si necesitas la referencia, importa
`soluciones/02_limpiar_y_analizar.ipynb` en el mismo Lakehouse.

## 6. Pasar de analizar a crear

El ejercicio no termina necesariamente con un resumen en memoria. Sigue
[el recorrido avanzado](modulos-avanzados.md) para crear una base persistida,
un modelo con informe, ontologia, Data Agent y Native App. El generador se
mantiene como punto de partida comun.

```text
Lee docs/modulos-avanzados.md y docs/contrato-analitico.md. Quiero continuar
con el modulo 03 para preparar una base reutilizable por Power BI.
Usa spark-cli si esta instalada. Primero genera codigo local y un plan de
publicacion de los tres destinos exactos; no consultes ni modifiques Fabric.
Incluye validaciones antes/despues, proteccion de todos los destinos y
explicacion de la reejecucion. No abras soluciones/ hasta que te lo pida.
```

Puedes elegir [Project Osmos](modulos/04-project-osmos.md) como alternativa
de ingenieria completa, no como una segunda carga sobre los mismos destinos.
La creacion de cada artefacto posterior tiene requisitos, prompts y una puerta
de aprobacion propios. No prometas construir todo el recorrido en 60 minutos.
