# Preparacion de participantes

## 1. Antes del workshop

- Acceso a Microsoft Fabric y a un workspace con capacidad activa y permisos
  para crear un notebook y escribir en un Lakehouse dedicado al taller.
- El [notebook 01](../notebooks/01_generar_datos_sinteticos.ipynb) importado y
  ejecutado con su configuracion por defecto. Un Lakehouse distinto por persona
  evita pisar las tablas de otra.
- VS Code y GitHub Copilot disponibles, con una cuenta que pueda usar el chat
  o Copilot CLI segun la ruta elegida y las politicas de la organizacion.
- Repo descargado y abierto en su raiz. Revisa el contenido antes de confiar
  en una carpeta o autorizar herramientas.

La generacion de datos se hace en Fabric, no con el kernel Python local de VS Code.
El tiempo de inicio de Spark varia: prepara los datos antes de los 60 minutos.

## 2. Elige UNA ruta de Copilot

### A. Copilot CLI, tambien desde la terminal integrada de VS Code

Requiere GitHub Copilot CLI instalado y autenticado. Sigue la
[guia oficial de instalacion](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-getting-started).
En la terminal, instala el plugin oficial:

```powershell
copilot plugin marketplace add microsoft/skills-for-fabric
copilot plugin install fabric-skills@fabric-collection
```

Despues, desde la raiz de este repo:

```powershell
copilot
```

Dentro de la sesion interactiva, comprueba:

```text
/skills list
```

Busca `spark-cli`, `sqldw-cli` y la skill local `workshop-ventas`.
Los nombres pueden incluir el prefijo del plugin. Pide a Copilot que indique
las skills disponibles antes de comenzar.

El plugin instala un bundle completo, con agentes y configuracion MCP ademas
de skills. Eso NO garantiza permisos ni acceso a tu Fabric. Revisa cualquier
peticion de autenticacion o ejecucion y no autorices todas las herramientas.

### B. Chat de VS Code: solo skills para generar codigo

Esta ruta usa APM siguiendo el README del
[repositorio oficial](https://github.com/microsoft/skills-for-fabric#install-a-single-skill-apm).
Requiere Python y acceso a paquetes publicos para instalar APM. Si tu organizacion
gestiona instalaciones, pide que preparen la herramienta antes de la sesion.

Desde la raiz del proyecto, en la terminal:

```powershell
python -m pip install apm-cli
apm install microsoft/skills-for-fabric --skill spark-cli --skill sqldw-cli --target copilot --only apm
```

`--only apm` evita registrar servidores MCP para el ejercicio basico.
APM despliega las skills y sus referencias compartidas; no copies un SKILL.md
aislado porque puedes romper sus enlaces. Puede desplegar tambien agentes del
paquete. Los archivos generados por la instalacion no son parte del material
publicado en este repo.

Abre una conversacion nueva en el chat de Copilot y comprueba la deteccion de las
skills y de `.github/copilot-instructions.md` en las opciones de personalizacion
de tu version de VS Code. Pide que consulte esas instrucciones. Descubrimiento
no equivale a uso: revisa las referencias y la actividad de herramientas.

En este modo Copilot lee los archivos locales, propone codigo y tu lo revisas
y ejecutas en Fabric. **No puede inspeccionar tus tablas remotas solo por tener
skills instaladas.**

## 3. Conexion en vivo: opcional, solo para la persona facilitadora

No es necesaria para generar codigo ni para ejecutar manualmente el notebook.
Si quieres que Copilot consulte Fabric, prepara antes autenticacion, herramientas
MCP/CLI compatibles y permisos minimos. Consulta el
[MCP setup oficial](https://github.com/microsoft/skills-for-fabric/tree/main/mcp-setup).

Para operaciones CLI que lo requieran, el proyecto oficial utiliza Azure CLI:

```powershell
az login
```

No imprimas ni pegues access tokens en el chat, archivos o presentaciones.
Iniciar sesion en Azure no conecta por si solo todos los clientes MCP.
La disponibilidad depende del cliente, tenant, endpoints y politicas.
Comprueba el destino antes de autorizar una consulta o una escritura.

Este repo no incluye un `.vscode/mcp.json` ni credenciales deliberadamente.
La conexion en vivo debe prepararse y comprobarse antes, no durante la demo.

## 4. Si algo falla

| Sintoma | Comprobacion |
|---|---|
| No hay skills | Revisa la ruta elegida, instalacion y sesion de Copilot; abre una nueva |
| No se aplican instrucciones | Abre la raiz del repo, comprueba el cliente/harness y los patrones applyTo |
| No hay Lakehouse predeterminado | Adjuntalo al notebook en Fabric y reinicia Spark |
| No existe el esquema dbo | Confirma si el Lakehouse tiene esquemas; usa `""` solo si no los tiene |
| Ya existen tablas | Usa otro Lakehouse o revisa conscientemente la sobrescritura |
| Tablas visibles en Spark pero no SQL | Refresca el explorador del SQL endpoint y espera la sincronizacion |
| Copilot no puede consultar Fabric | Trabaja en modo generacion local; no es un fallo del generador |
| Spark no inicia o hay throttling | Revisa capacidad y concurrencia con la persona facilitadora |

## Referencia de preparacion

Las instrucciones de instalacion se contrastaron el 17 de noviembre de 2026 con
el [README oficial en esta revision](https://github.com/microsoft/skills-for-fabric/blob/e31422e7d1045ef3a0906df9ff5991f2338af010/README.md).
Los comandos instalan la version que publique el proveedor: prueba tu configuracion
antes de cada edicion del workshop.
