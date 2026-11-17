# Referencia 08: integrar la Native App sin fingir un despliegue

El proyecto completo se obtiene con el scaffold oficial Rayfin de la version
elegida. Este repo no incluye un item App desplegado ni una copia parcial del
SDK. Sigue el [modulo 08](../docs/modulos/08-native-app.md) para separar
instalacion, acceso, consultas y publicacion.

## Ruta de datos

```text
Usuario autenticado
    -> frontend publicado como Fabric App
    -> conector salesmodel (fabric-semanticmodel, delegado)
    -> workshop_ventas_model
    -> medidas explicitas y relaciones
    -> tablas originales/detalle/calendario del taller
```

El navegador no recibe tokens de servicio ni conexiones SQL. El conector
guarda los selectores del modelo en configuracion del backend local/deploy,
no en este repositorio publico. No se crean entidades CRUD para copiar ventas.

## Integracion de los archivos locales

Tras generar el proyecto y registrar el conector segun la documentacion,
copia `consultar-ventas.mjs` y `ingresos-categoria.json` a una carpeta propia
del frontend. Respeta las convenciones del scaffold y la importacion JSON
que permita su compilador. El siguiente es el punto de integracion, **no**
un programa autonomo ni una sustitucion de la configuracion del cliente:

```javascript
const rows = await consultarVentas(
  (input, options) => client.connectors.salesmodel.executeQuery(input, options),
  payload,
);
```

`client` es el cliente autenticado creado por el scaffold con
`RayfinClient.create`; `payload` es el JSON revisado y `consultarVentas` la
funcion importada del adaptador. El servicio de conectores debe registrar
`fabricSemanticModel()` en el mapa runtime de `salesmodel`: sin ese runtime,
no se garantiza el resultado normalizado que espera el adaptador.
No copies un cliente de otra version del SDK sin adaptarlo.

La funcion devuelve filas con `category`, `lines`, `units`, `revenue` y
`requestId`. `revenue` es texto decimal de dos decimales producido por
FORMAT en el modelo para **presentacion**, nunca para sumar en el navegador.
Las medidas del modelo siguen siendo numericas. Los ejemplos de prueba
locales son fixtures pequenos, no cifras reales del taller.

## Pantalla de referencia

La pantalla tiene titulo "Ventas del taller", explicacion "EUR; lineas, no
pedidos", selector de categoria, boton Actualizar y tabla accesible con
encabezados Categoria, Ingresos EUR, Lineas y Unidades.

Usa el componente de autenticacion Fabric SSO del scaffold, no uno inventado.
Llama al conector solo tras una sesion valida y muestra sus errores de acceso.
Durante la carga, deshabilita Actualizar; al fallar, muestra un error y no
mantengas filas anteriores como si fueran una consulta actual correcta.
Una respuesta vacia indica ausencia de filas, no un total monetario cero.
El selector trabaja sobre categorias devueltas por la consulta; no interpola
texto libre dentro de DAX. No uses innerHTML para mostrar valores del modelo.

## Puertas de verificacion

1. **Adaptador local:** `node --test tests\test_native_app.mjs`, desde la raiz
   de este repositorio si Node esta instalado. No instala nada ni consulta Fabric.
2. **Proyecto:** ejecutar el build/typecheck que declare el scaffold, despues
   de instalar dependencias con consentimiento. Este repo no los ha ejecutado.
3. **Consulta CLI autorizada:** validar status y filas del payload contra
   el modelo; comprobar importes por categoria con el informe.
4. **Publicacion aprobada:** `rayfin up` y `rayfin up status`, revisando
   los recursos aprovisionados. No usar `--force`.
5. **App publicada:** abrir su URL autenticada y verificar que consulta
   y pinta datos reales mediante el conector desplegado. La prueba CLI por si
   sola no cubre identidad delegada, hosting ni el runtime del conector.
6. **Errores y acceso:** comprobar estado vacio y error sin convertirlos a
   ceros ni revelar tokens. No modificar permisos como parte automatica del test.

Solo la ultima parte demuestra una Native App funcionando dentro de Fabric.
Si falta un requisito, conserva el proyecto y explica el punto pendiente;
no presentes una pagina local o un JSON como una App creada.
