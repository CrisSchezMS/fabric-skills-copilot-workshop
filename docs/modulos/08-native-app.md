# 08 - Crear una Fabric Native App de ventas

**Objetivo:** crear un item **App de Fabric**, con autenticacion y una consulta
real al modelo semantico. No es una App de distribucion Power BI, un HTML local
con cifras pegadas ni una aplicacion web alojada fuera de Fabric.

## Requisitos y alcance

Completa 05. La documentacion actual denomina la experiencia **Fabric Apps
(preview)** y usa Rayfin. Requiere capacidad, region soportada, habilitacion
administrativa de Fabric Apps, permisos de creacion/despliegue y Node.js 20+
en el equipo de desarrollo. Revisa las
[fuentes verificadas](../referencias-avanzadas.md) antes de impartir.

No se presupone una skill especifica de Native Apps. Copilot trabaja con la
documentacion oficial y el proyecto generado por Rayfin; las Fabric Skills
ayudan con las fuentes y el modelo, no sustituyen el SDK.

El producto minimo se llama `workshop_ventas_app`: una pantalla autenticada
con ingresos, lineas y unidades por categoria, selector de categoria, boton
Actualizar y estados de carga, error y ausencia de datos. Consulta el modelo
con un conector **fabric-semanticmodel** delegado; no duplica ventas en la
base SQL de la app ni recalcula importes en JavaScript.

## Fase 1: preparar sin instalar ni conectar

```text
Prepara una Fabric Native App de ventas usando la documentacion oficial actual
de Fabric Apps y Rayfin. Lee docs/modulos/08-native-app.md y las plantillas
native-app/. No es una Power BI App ni un HTML con datos incrustados.
Planea el scaffold oficial, autenticacion Fabric SSO, conector delegado al
modelo workshop_ventas_model y una pantalla de solo lectura por categoria.
Separa instalaciones, autenticacion, descubrimiento, consultas y despliegues.
No ejecutes comandos ni consultes mi tenant hasta que autorice cada fase.
```

El repo aporta un payload y un adaptador local, **no** un proyecto Rayfin completo.
El scaffold oficial de la version elegida proporciona estructura, autenticacion,
configuracion y dependencias. No generes a mano un `rayfin.yml` con IDs ficticios.

## Fase 2: crear el proyecto, con aprobacion de instalacion

Desde una carpeta de trabajo personal **fuera de este repo publico**, y solo
tras aprobar descargas/instalacion:

```powershell
npm create @microsoft/rayfin@latest workshop_ventas_app
Set-Location workshop_ventas_app
```

Revisa el scaffold y sus instrucciones, `package.json` y lockfile. No mezcles
paquetes Rayfin 1.x y 2.x; el adaptador de este repo usa la respuesta normalizada
documentada para 2.x. Si el scaffold tiene otra version, adapta contra su
documentacion antes de usarlo, sin forzar una actualizacion silenciosa.

Autenticarse, crear el item desde el portal o desplegar son operaciones
separadas del scaffold. Antes de autorizarlas, confirma workspace y nombre.
Revisa especialmente el codigo de ejemplo generado: esta app no necesita
crear entidades de negocio, CRUD sobre ventas ni acceso anonimo.

## Fase 3: conectar al modelo correcto

Tras aprobar autenticacion y descubrimiento de solo lectura, usa la skill de
modelado o la busqueda de conectores para resolver el modelo por su nombre.
No copies IDs al repo publico. `npx rayfin login` no concede acceso al modelo.

Usa el comando `connector add` que devuelva la busqueda para **ese modelo**,
tipo `fabric-semanticmodel`, nombre `salesmodel`. Revisa sus selectores antes
de ejecutarlo. Instala solo los paquetes/versiones exactos que indique el CLI,
tras aprobacion. El schema generado de este conector no se edita a mano.

Sigue la guia de registro del runtime `fabricSemanticModel()` en
`connectorsService`, manteniendo el nombre `salesmodel` en todas las partes.
El conector solo admite identidad **delegada**. La prueba CLI directa requiere
Read y Build en el modelo; no reutilices el minimo Read del modulo Data Agent.

Copia `plantillas/native-app/ingresos-categoria.json` a una ruta local del
proyecto y autoriza por separado esta consulta de solo lectura:

```powershell
npx rayfin connector invoke salesmodel executeQuery --file .\ingresos-categoria.json
```

Ese comando consulta Fabric aunque se ejecute en una terminal local.
Comprueba `status`, columnas y filas; una prueba CLI correcta no demuestra
que el conector desplegado funcione bajo la identidad del usuario de la app.

## Fase 4: crear la pantalla y desplegar

```text
Usa el cliente del scaffold y el conector salesmodel ya comprobado.
Integra consultar-ventas.mjs con ingresos-categoria.json. Crea una pantalla
accesible con una tabla por categoria, selector local de categoria y Actualizar.
Seleccionar categoria filtra las filas recibidas, no envia DAX construido
desde texto del usuario. Mantiene los importes como texto decimal recibido
del modelo; no suma ni recalcula dinero en el navegador.
Muestra carga, error con requestId y estado vacio sin fingir ingresos cero.
Usa Fabric SSO y hosting protegido. No uses autenticacion anonima, tokens
incrustados, credenciales nuevas ni consultas arbitrarias escritas por usuarios.
Prepara los cambios y los comandos de build; no arranques ni despliegues.
```

El [adaptador](../../plantillas/native-app/consultar-ventas.mjs) recibe la funcion
`executeQuery` del cliente oficial; no implementa autenticacion alternativa.
El importe llega como string con dos decimales desde `FORMAT` en DAX para
presentacion. Las medidas siguen siendo numericas en el modelo.

Ejecuta el build que declare el scaffold y revisa configuracion antes de
autorizar despliegue. Los comandos de publicacion documentados son:

```powershell
npx rayfin up
npx rayfin up status
```

**No son comandos locales inocuos.** `up` puede aprovisionar servicios, aplicar
migraciones y publicar el frontend; requiere revisar y aprobar su alcance.
`npm run dev` tambien puede provisionar/reutilizar backend en Fabric segun la
version. No lo ejecutes pensando que es una previsualizacion desconectada.
No uses `--force` ni un flag de aprobacion automatica para saltar revisiones.

## Criterio de cierre

La app debe existir como item Fabric y la **URL publicada** debe cargar con
SSO y mostrar filas reales a traves del conector desplegado. Contrasta cada
categoria con el informe; prueba actualizar, sin datos y error de acceso.
Un fallo de permisos debe mostrarse como error, no como una tabla de ceros.
No cambies permisos para hacer pasar la prueba sin una autorizacion adicional.

Referencia de integracion y lista de comprobacion:
`soluciones/08_native_app.md`. Sin servicios habilitados se entrega el proyecto
o diseno local como pendiente de despliegue, nunca como app creada en Fabric.
