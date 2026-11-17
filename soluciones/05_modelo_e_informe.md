# Referencia 05: modelo y dos paginas

Copilot utiliza esta referencia al desplegar el
[modulo 05](../docs/modulos/05-modelo-informe.md): modelo con
`semantic-model-authoring`, informe con `powerbi-report-cli`. El documento
no es un modelo desplegado ni un `.pbix`.

## Decisiones de referencia

Usa exactamente los mapeos de `plantillas/modelo-semantico.json`. Productos,
Tiendas y Calendario filtran Ventas con relaciones activas 1:* y una sola
direccion. El detalle conserva la identidad de linea; el agregado diario
se queda fuera del modelo. No se calcula `net_amount` otra vez en DAX.

Las cuatro medidas, creadas individualmente en Ventas, son:

```dax
Ingresos netos EUR = SUM('Ventas'[Importe neto])
```

```dax
Lineas de venta = COUNTROWS('Ventas')
```

```dax
Unidades = SUM('Ventas'[Cantidad])
```

```dax
Ingreso medio por linea EUR =
DIVIDE([Ingresos netos EUR], [Lineas de venta])
```

Las dos medidas monetarias llevan `#,##0.00 "EUR"` y las otras `#,##0`.
Los nombres del modelo no cambian las columnas fisicas. El modo de referencia
es Direct Lake, no Import. Usa Decimal/fixed decimal para el importe en el modelo.
Agrega descripciones, oculta las claves y los campos base sumables y configura
los atributos Anio, Trimestre y Mes numero sin sumar.

## Construccion del informe

En Resumen, coloca tres tarjetas arriba: ingresos, lineas y unidades.
Debajo, barras por categoria y una serie diaria con Calendario.Fecha.
A un lado, segmentadores de fecha, ciudad y canal. Usa interacciones de filtro
consistentes y titulos que indiquen EUR y que las lineas no son pedidos.

En Exploracion, crea una matriz con Categoria > Producto > Tienda y las cuatro
medidas; una barra por ciudad permite contrastar la distribucion. Sincroniza
fecha y canal con la primera pagina. No geocodifiques ciudades ficticias.

El informe puede sumar visualmente por categoria, pero no redondea una suma
de calculos float ni usa precio de catalogo para reconstruir ingresos.

## Comprobacion razonada

Ejecuta `plantillas/validar-modelo.dax` como consulta DAX autorizada. Sin filtros,
su ingreso por categoria debe coincidir exactamente con el resumen PySpark
y su suma con el informe del generador. Cambia a online y enero de 2026:
el nuevo total solo se compara con una referencia que use esos mismos filtros.

Si un filtro no se propaga, revisa relacion activa, cardinalidad, direccion
y tipos de las claves. Si crecen las cifras, revisa dimensiones duplicadas
y hechos repetidos antes de cambiar una medida. No arregles un join incorrecto
con DISTINCTCOUNT mientras sigues sumando ingresos duplicados.

No hay cifras publicadas aqui: dependen de la ejecucion y configuracion reales.
No se incluye un PBIP ficticiamente funcional sin su conexion y definicion
de informe. La autoria debe guardarse, desplegarse y validarse mediante las herramientas
soportadas antes de marcar este modulo como terminado.
