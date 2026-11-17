# 05 - Copilot despliega el modelo y el dashboard Power BI

**Entrega:** `workshop_ventas_model` Direct Lake, cuatro medidas validadas e
informe `workshop_ventas_report` de dos paginas. "Dashboard" aqui significa
**informe Power BI**, no Real-Time Dashboard ni tiles del servicio.

Necesitas base analitica validada, autoria y capacidad Direct Lake compatibles.
Comprueba que ambos nombres estan libres. Las plantillas son disenos propios,
no PBIP ni definiciones REST; Copilot construye los formatos reales.

## 1. Crear y desplegar el modelo

```text
Usa semantic-model-authoring. Crea y despliega workshop_ventas_model en el
workspace aprobado desde las tablas reales del Lakehouse confirmado.
Aplica plantillas/modelo-semantico.json: Direct Lake, cuatro tablas,
tres relaciones 1:* unidireccionales y cuatro medidas explicitas.
Usa el MCP de modelado si esta disponible y autorizado; en caso contrario,
la ruta de archivos y despliegue soportada por la skill. Guarda los archivos
con bindings fuera del repo publico. No cambies a Import/DirectQuery sin
explicar el bloqueo y obtener mi decision. Relee el modelo desplegado.
Ejecuta plantillas/validar-modelo.dax y contrasta con Spark.
```

| Tabla del modelo | Fuente |
|---|---|
| Ventas | workshop_sales_clean |
| Productos | workshop_products |
| Tiendas | workshop_stores |
| Calendario | workshop_calendar |

Dimensiones filtran Ventas, sin raw ni agregado como hechos adicionales.
Configura nombres, descripciones, formatos y columnas sin agregacion segun
la plantilla. No recalcules net_amount en DAX ni crees un calendario calculado.
No edites TMDL en paralelo si MCP es la fuente de verdad de la sesion.
Desplegar desde archivos y desplegar un modelo MCP no son la misma operacion:
usa el procedimiento correspondiente de la skill.

## 2. Planificar el informe y aprobar su especificacion

Usa la skill oficial **`powerbi-report-cli`**. Si falta en la instalacion,
solicita instalar/actualizar el bundle oficial; no uses FabricIQ como autoria.
No conviertas el paso automaticamente en una tarea manual de Power BI.

```text
Usa powerbi-report-cli y el modelo ya desplegado. Planifica las paginas
Resumen y Exploracion de plantillas/informe.json. Descubre campos y medidas
reales; fija filtros, interacciones, formato EUR y accesibilidad.
Guarda la especificacion en el proyecto privado de trabajo y muestramela.
Detente para que la apruebe antes de construir o publicar.
```

La skill requiere **planning -> design -> authoring -> management**.
La especificacion debe aprobarse en un turno posterior. Una peticion inicial
de "desplegar todo" no omite ese gate.

## 3. Construir y publicar despues de aprobar

```text
Apruebo la especificacion del informe presentada. Continua con
powerbi-report-cli: disena, genera el PBIR/PBIP real con sus herramientas,
valida esquemas, previsualiza y revisa las capturas. Publica el informe
workshop_ventas_report en el workspace confirmado, vinculado al modelo
validado. Sigue la operacion hasta estado final y relee el item/vinculo.
```

No basta crear un item vacio o un PBIP inventado. Usa las herramientas y esquemas
actuales de la skill. Si aparece una colision, no reemplaces el informe existente.

## Aceptacion

Comprueba cuatro medidas, tres relaciones y totales por categoria. Aplica los
**mismos filtros** de fecha, ciudad y canal en DAX/Spark/informe y reconcilia.
Revisa las dos paginas, sus visuales y propagacion de filtros en el publicado.
Las ciudades ficticias no se geocodifican. No inventes clientes, margen,
pedidos ni crecimiento interanual sin datos.

El modelo validado permite avanzar a Data Agent y App aunque el informe tenga
un bloqueo propio. [Decisiones de referencia](../../soluciones/05_modelo_e_informe.md).
