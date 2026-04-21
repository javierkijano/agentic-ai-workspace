# Guía de Instalación del Workspace

Este documento detalla los pasos para configurar tu entorno operativo local y conectarlo con el repositorio canónico de recursos.

## Requisitos Previos
1. Tener clonado `agentic-ai-resources` en tu máquina.
2. Tener clonado este repositorio (`agentic-ai-workspace`).

## Paso 1: Configuración del Entorno
El sistema utiliza dos archivos principales en la carpeta `config/` para definir cómo opera este workspace:

### A. Configuración de Rutas (`config/paths.yaml`)
Define el valor de los placeholders. Asegúrate de que `AGENTIC_RESOURCES` apunte a tu clon de recursos:
```yaml
variables:
  AGENTIC_RESOURCES: /tu/ruta/al/repo/agentic-ai-resources
```

### B. Configuración de Topología (`config/topology.yaml`)
Define la identidad de este workspace y los enlaces con otros agentes o worktrees. Revisa que las rutas en la sección `links` y `worktrees` sean correctas para tu máquina.

## Paso 2: Inicialización del Entorno
Ejecuta el script de inicialización encapsulado en la skill de gestión:

```bash
python3 skills/workspace-repo-manager/core/scripts/navigator.py init
```

## Paso 3: Verificación
Puedes verificar que la conexión es correcta usando la interfaz de la skill:

```bash
# Si usas un runner de skills:
skill-run workspace-repo-manager status
```

---
*Nota: Nunca subas tu `config/paths.yaml` con rutas personales al repositorio canónico. Este archivo es específico de tu instalación local.*
