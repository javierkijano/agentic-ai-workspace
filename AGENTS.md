# Agentic Workspace - Operational Environment

Este es el repositorio de **Workspace**, encargado de la operación local, la topología y la gestión del estado de los agentes en esta instalación específica.

## Propósito
A diferencia de `agentic-ai-resources` (que contiene la inteligencia canónica), este workspace facilita:
- La ejecución de herramientas locales.
- El almacenamiento de estados mutables (`runtime/`, `logs`).
- La configuración de la topología local (dónde están los recursos).

## Conexión con Recursos
Este workspace depende de:
- **Recursos**: `/home/jq-hermes-01/git-repositories/own/agentic-ai-resources`

## Herramientas de Gestión
- **`workspace-repo-manager`**: Skill local central que encapsula toda la lógica de gestión (status, init, sync).
- **Scripts de Core**: Los entrypoints operativos residen en `skills/workspace-repo-manager/core/scripts/`.

## Reglas de Operación
1. Este repositorio NO contiene lógica canónica; solo wrappers y configuraciones.
2. Todo cambio estructural debe proponerse en `resources`.
3. **Higiene Operativa (CRÍTICO)**:
    - Es MANDATORIO registrar cada tarea en `runtime/session_registry.jsonl`.
    - No cierres una sesión sin haber realizado `git commit` de tus cambios en la rama de trabajo.
    - Consulta el protocolo de trazabilidad en el repositorio de recursos: `protocols/traceability-and-commits.md`.


---
*Operatividad local al servicio de la inteligencia canónica.*
