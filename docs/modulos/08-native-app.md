# 08 - Copilot construye y despliega una Fabric Native App

**Entrega:** item `workshop_ventas_app` de **Fabric Apps (preview)**, URL
publicada con SSO y consulta delegada real al modelo. No es una Power BI App
de distribucion, un HTML local ni una web alojada fuera de Fabric.

## Requisitos y aprobacion

Modelo validado; Fabric Apps habilitado; capacidad/region soportadas;
permisos de despliegue; Node.js 20+. La consulta delegada al modelo requiere
los permisos de Read y Build de esa ruta; no generalices el minimo Read del
consumo mediante Data Agent.

No se presupone una skill especifica de Apps instalada. Copilot utiliza
el **scaffold y CLI oficiales Fabric Apps/Rayfin** y las Fabric Skills para
descubrir/validar el modelo. Lee la documentacion vigente antes de operar.
El repo aporta adaptador y payload, no un SDK parcial ni una App ya creada.

El plan aprobado incluye proyecto privado, instalaciones concretas,
autenticacion, conector y recursos internos que Rayfin vaya a aprovisionar.
Si ese detalle aun no estaba aprobado, presentalo antes de ejecutar.
`npm run dev` y `rayfin up` pueden crear backend remoto; no son pasos offline.

## 1. Encargo de construccion real

```text
Construye y despliega workshop_ventas_app en el workspace confirmado usando
el scaffold oficial Fabric Apps/Rayfin. Usa un proyecto privado fuera del repo.
Comprueba colisiones y requisitos, muestra paquetes y recursos por aprobar
si aun no lo estan. Despues ejecuta el scaffold, implementa, compila y publica.
Quiero una pantalla con SSO, tabla por categoria, ingresos EUR, lineas,
unidades, selector de categoria, Actualizar y estados de carga/vacio/error.
Usa el modelo validado y un conector delegado fabric-semanticmodel salesmodel.
Integra plantillas/native-app/consultar-ventas.mjs e ingresos-categoria.json.
No copies ventas al backend, no recalcules importes en JavaScript y no uses
datos incrustados. Prueba la URL publicada, no solo una pantalla local.
```

## 2. Scaffold, autenticacion y conector

Copilot ejecuta los comandos documentados tras las aprobaciones necesarias:

```powershell
npm create @microsoft/rayfin@latest workshop_ventas_app
Set-Location workshop_ventas_app
npx rayfin login
```

Sigue las instrucciones del scaffold, package.json y lockfile. No mezcles
Rayfin 1.x/2.x; los paquetes `@microsoft/rayfin` deben tener las versiones
exactas coherentes que indique el proyecto. El adaptador de este repo sigue
la respuesta normalizada 2.x; adapta si cambia el contrato documentado.
No inventes un `rayfin.yml` con IDs de ejemplo.

Descubre el modelo real y ejecuta el `connector add` que devuelva la herramienta
para ese recurso, tipo `fabric-semanticmodel`, nombre `salesmodel`.
No inventes sus selectores ni edites a mano el schema generado.
Registra el runtime `fabricSemanticModel()` en `connectorsService` del cliente
`RayfinClient.create`, segun la documentacion de la version.

Prueba el conector con el payload del proyecto:

```powershell
npx rayfin connector invoke salesmodel executeQuery --file .\ingresos-categoria.json
```

Esto consulta Fabric de verdad. Comprueba status, columnas y filas. La prueba
CLI no demuestra aun que la identidad/connector desplegados funcionen.

## 3. Implementar, compilar y publicar

Copilot integra el adaptador con el cliente real del scaffold y construye
la pantalla accesible. Las medidas del modelo siguen siendo numericas; el
payload formatea el importe a string decimal solo para presentar. El navegador
no suma dinero ni interpola texto libre en DAX. El selector filtra las categorias
recibidas; Actualizar vuelve a consultar. No convertir errores en filas de ceros.

Ejecuta build/typecheck definidos por el scaffold. Revisa configuracion/recursos
y despliega el alcance autorizado:

```powershell
npx rayfin up
npx rayfin up status
```

Sigue el estado hasta finalizacion. Usa hosting protegido y autenticacion
oficial Fabric SSO; sin tokens incrustados, acceso anonimo ni `--force`.
No habilites ajustes de tenant ni cambies permisos para superar un fallo.

## 4. Aceptacion desde Fabric

Abre la **URL publicada** con una identidad autorizada, comprueba el item App
y que los datos llegan mediante el conector desplegado. Contrasta cada categoria
con DAX/informe, prueba Actualizar y verifica estados vacio/error sin modificar
permisos reales solo para provocar pruebas. No inventes una prueba si el cliente
no permite observarla: despliegue completado y UX verificada son estados distintos.

Sin requisito de preview o permiso, informa del bloqueo exacto y conserva
el proyecto para reanudar; no declares terminada la App porque existe un frontend.
[Referencia de integracion](../../soluciones/08_native_app.md).
