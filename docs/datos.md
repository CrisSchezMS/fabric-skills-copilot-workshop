# Contrato de datos y reglas del ejercicio

Todos los valores son ficticios. No hay clientes, emails, direcciones ni datos
copiados de un tenant. Cada fila representa una **linea de venta**, no un pedido
con varias lineas: no interpretes COUNT(*) como numero de pedidos reales.

## Tablas y tipos

`workshop_products`:

| Columna | Tipo Spark | Significado |
|---|---|---|
| product_id | int | Clave unica del producto |
| product_name | string | Producto 01 a Producto 12 |
| category | string | Categoria canonica |
| list_price | decimal(18,2) | Precio de catalogo en EUR |

`workshop_stores`:

| Columna | Tipo Spark | Significado |
|---|---|---|
| store_id | int | Clave unica de tienda |
| store_name | string | Nombre ficticio |
| city | string | Ciudad canonica ficticia |

`workshop_sales_raw`:

| Columna | Tipo Spark | Significado |
|---|---|---|
| sale_id | string | Identificador de la linea; las copias exactas lo repiten |
| sale_date | date | Fecha entre START_DATE y START_DATE + DAYS - 1 |
| product_id | int | Relacion con producto; hay valores huerfanos intencionados |
| store_id | int | Relacion con tienda |
| channel | string | online o tienda |
| quantity | int | Unidades; hay ceros y negativos intencionados |
| unit_price | decimal(18,2) | Precio unitario en EUR |
| discount_rate | decimal(4,2) | Fraccion: 0.10 significa 10 % |
| status | string | completed o cancelled |
| category_raw | string nullable | Categoria recibida en origen, no canonica |
| city_raw | string nullable | Ciudad recibida en origen, no canonica |

## Configuracion original

- Semilla 42, 10.000 ventas base y 90 dias a partir de 2026-01-01.
- 12 productos, 4 categorias, 4 tiendas.
- 2 % de copias exactas: 200 filas adicionales.
- Seis grupos disjuntos de incidencias ANTES de duplicar: cada grupo contiene
  el 1 % de las ventas base (100 con los parametros originales).
- Grupos: categoria nula, ciudad nula, cantidad no positiva, producto huerfano,
  categoria con espacios/mayusculas y ciudad con espacios/mayusculas.
- Cancelacion con probabilidad 10 %; no garantiza exactamente 1.000 filas.
  Es un estado de negocio, independiente de las incidencias.

Los duplicados se anaden despues de introducir las incidencias y pueden copiarlas.
Por eso el recuento raw de un error puede superar 100 y los contadores no deben
sumarse para calcular rechazos. Los resultados exactos estan en
[expected-results.json](expected-results.json).

El generador es reproducible con la misma configuracion y la implementacion
de Python usada para validarlo (Python 3.11). No depende de la fecha actual,
red, Faker, pandas ni archivos externos. El contrato de CI comprueba esa version;
no se garantiza identidad binaria entre todas las versiones futuras de Python.

## Reglas de limpieza

1. Elimina copias completamente iguales. Si el mismo sale_id tiene versiones
   diferentes, detente: la demo no incluye una regla de seleccion de version.
2. Comprueba que las dimensiones tienen claves unicas y no nulas antes de unir.
3. Conserva ventas con status completed, quantity > 0 y claves existentes en
   ambas dimensiones. No corrijas cantidades negativas ni inventes productos.
4. Recupera categoria y ciudad de sus dimensiones. Los campos raw no son la
   fuente canonica: un nulo o un texto desnormalizado no elimina la venta.
5. Calcula `net_amount` en EUR como:
   `ROUND(quantity * unit_price * (1 - discount_rate), 2)`.
   Usa decimal y redondeo comercial HALF_UP, **por linea y antes de sumar**.
6. Agrupa por categoria canonica para comparar ventas, unidades e ingresos.

No hay impuestos, devoluciones, costes, margen ni conversion monetaria.
No generalices esta simplificacion a un sistema real.

## Destinos y limites

El notebook 01 escribe solo las tres tablas con prefijo `workshop_`.
`SCHEMA = "dbo"` selecciona ese esquema dentro del Lakehouse predeterminado.
`SCHEMA = ""` deja una referencia simple para Lakehouses sin esquemas.
El esquema es un parametro explicito, no se infiere de un nombre.

La solucion 02 no escribe una capa silver ni gold: calcula todo en memoria.
Persistir una capa limpia es una ampliacion que requiere plan y confirmacion.
La ampliacion opcional de este repositorio se define por separado en
[contrato-analitico.md](contrato-analitico.md). No cambia las tres tablas
originales ni implica que existan ya los nuevos destinos.

El generador construye filas en el driver. Admite entre 100 y 100.000 ventas base
para limitar memoria/coste de esta demo; **no** es una propuesta de escalado.
Las tablas se crean sin particionado: son demasiado pequenas para necesitarlo.
