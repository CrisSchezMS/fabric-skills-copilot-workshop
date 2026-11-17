---
name: workshop-ventas
description: Guia el ejercicio de ventas sinteticas de este repositorio. Usar al pedir explorar los datos del taller, preparar la limpieza o explicar el resultado. No sustituye a las Microsoft Fabric Skills oficiales.
---
# Ejercicio guiado de ventas

Esta es una skill LOCAL del taller, no una skill oficial de Microsoft.
Orquesta el contexto educativo; para APIs y codigo Fabric utiliza las skills
oficiales instaladas. No las instala ni proporciona herramientas o autenticacion.

1. Lee `docs/datos.md` y `docs/laboratorio.md` antes de proponer una solucion.
2. Pregunta si se quiere generar codigo local o actuar contra un entorno Fabric.
   Si se pide actuar, confirma Lakehouse/endpoint y herramientas disponibles.
   No descubras ni cambies recursos remotos por iniciativa propia.
3. Para notebooks/PySpark usa la skill oficial `spark-cli`, si esta disponible.
   Para T-SQL de solo lectura usa `sqldw-cli`, si esta disponible.
   Si falta, declara la limitacion en vez de simular haberla usado.
4. Empieza por perfilado: filas, claves distintas, copias, nulos, cantidades
   invalidas y relaciones huerfanas. Distingue incidencias raw y ventas unicas.
5. Propone reglas antes de generar la transformacion. Usa dimensiones canonicas,
   decimal y redondeo por linea. Las cancelaciones quedan fuera de ingresos.
6. Espera aprobacion antes de ejecutar cambios remotos o sobrescribir archivos.
   Generar codigo no significa ejecutarlo; una respuesta no prueba un resultado.
7. Pide al asistente del taller que compare con el informe del notebook 01.
   No abras `soluciones/` salvo que el usuario pida ver la solucion.
8. Explica como comprobar recuentos, unicidad e ingresos. Si no has ejecutado,
   declara que el resultado es una propuesta pendiente de validacion.
