# Workspace Repo Manager (Hermes Platform)

Esta skill permite gestionar el entorno operativo local y asegurar que la conexión con el repositorio de recursos es correcta.

## Comandos Principales

### `status`
Muestra un resumen del estado del workspace, validando que los enlaces a `agentic-ai-resources` definidos en `config/paths.yaml` son válidos.

### `init`
Prepara el entorno local:
1. Crea las carpetas `runtime/`, `dist/` y `data/` si no existen.
2. Valida la estructura de archivos de configuración.

### `sync`
Compara el estado del workspace con las directrices de gobernanza definidas en el repo de recursos.

## Configuración
Esta skill depende de los archivos en la carpeta `config/` de la raíz del workspace. No intentes ejecutarla sin haber completado los pasos en `docs/INSTALL.md`.
