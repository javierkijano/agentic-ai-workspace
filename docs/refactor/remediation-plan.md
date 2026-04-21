# Remediation Plan: Agentic AI Ecosystem Alignment

**Fecha**: 2026-04-21  
**Basado en**: `docs/refactor/implementation-alignment-audit.md`  
**Estado**: Propuesta de Ejecución

## 1. Executive Summary

Este plan describe la secuencia de acciones necesarias para elevar el ecosistema desde una base técnica sólida pero introspectiva hacia un entorno de trabajo operativo completo. El principio rector es la **"Apertura al Exterior"**: transformar el sistema para que su prioridad sea la gestión de proyectos reales, utilizando una disciplina Git rigurosa de worktrees por tarea.

La secuencia propuesta es: **Visibilidad -> Disciplina -> Refinamiento**. Primero haremos visibles los proyectos y el sistema (Onboarding), luego forzaremos la disciplina Git correcta, y finalmente puliremos las fronteras de gestión entre el canon y la operación.

---

## 2. Resumen de Hallazgos de Partida

| Categoría | Puntos Clave |
| :--- | :--- |
| ✅ **Aligned** | Separación de repositorios (Resources/Workspace), Naming, Ubicación del estado mutable (`runtime/`). |
| ⚠️ **Partially Aligned** | Onboarding jerárquico incompleto, solapamiento visual en interfaces de management. |
| ❌ **Misaligned** | **Inexistencia de Proyectos** en la topología local, **Abuso de Clones Base** (falta de worktrees por tarea). |
| ❓ **Open Questions** | Implementación de Views (vistas restringidas), Persistencia de Memory Viva. |

---

## 3. Clasificación de Cambios

| Cambio | Categoría | Hallazgo de Origen | Valor Esperado | Riesgo | Prioridad |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Crear Onboarding Nivel 0 (`~/AGENTS.md`) | Quick Win | Falta de entrada jerárquica | Claridad de entrada inmediata para cualquier agente. | Bajo | P0 |
| Mapear Proyectos en `topology.yaml` | Structural Correction | Introversión sistémica | Los proyectos son ciudadanos de primera clase. | Bajo | P0 |
| Establecer Flujo "Worktree por Tarea" | Structural Correction | Abuso de Clones Base | Limpieza del canon y aislamiento de cambios. | Medio | P1 |
| Refinar Interfaces de Skills de Gestión | Delicate Change | Solapamiento visual | Frontera clara entre "Gobernanza" y "Operación". | Medio | P2 |
| Actualizar Docs con "Historia Correcta" | Quick Win | Documentación desactualizada | Coherencia entre lo que se lee y lo que se opera. | Bajo | P1 |

---

## 4. Plan por Fases

### Fase 1: Identidad y Ciudadanía (Visibilidad)
**Objetivo**: Establecer la jerarquía de entrada y reconocer los proyectos reales como parte del sistema.

- **Cambios incluidos**:
    - Creación de `~/AGENTS.md` (Nivel 0).
    - Actualización de `topology.yaml` para incluir la sección `projects:`.
    - Registro de al menos 3 proyectos reales existentes en el workspace.
- **Cambios excluidos**: Modificaciones en la lógica Git o en las herramientas de gestión.
- **Criterio de Aceptación**: Un agente que entre en `$HOME` entiende que existe un Workspace y una lista de proyectos disponibles.
- **Validación**: Ejecutar `navigator.py status` y ver los proyectos listados (requiere actualización mínima del script).
- **Riesgos**: Ninguno significativo.

### Fase 2: Disciplina Operativa (Git Workflow)
**Objetivo**: Migrar la operativa diaria desde los clones base hacia worktrees por tarea.

- **Cambios incluidos**:
    - Creación de una guía de "Protocolo Git" en `resources/protocols/`.
    - Script de conveniencia en `workspace-repo-manager` para automatizar `git worktree add` para nuevas tareas.
    - Definición de los clones en `/git-repositories/own/` como "Clones de Mantenimiento/Base".
- **Cambios excluidos**: No se moverán los clones base de sitio.
- **Criterio de Aceptación**: Toda nueva tarea de remediación de este plan se realiza en un worktree independiente.
- **Validación**: `git worktree list` debe mostrar el aislamiento de la tarea actual.
- **Riesgos**: Desorientación del agente al cambiar de directorio. Mitigación: El script de creación de tarea debe imprimir claramente el nuevo path.

### Fase 3: Refinamiento de Gobernanza (Interfaces)
**Objetivo**: Eliminar ambigüedades entre el Gestor de Recursos y el Gestor del Workspace.

- **Cambios incluidos**:
    - Limpieza de comandos duplicados en `resources-repo-manager` (ej: mover ayuda al commit al workspace).
    - Refuerzo de la capacidad de "Exploración Canónica" en Resources.
    - Asegurar que el Workspace solo tiene wrappers y nada de lógica de decisión estructural.
- **Cambios excluidos**: No se fusionarán las skills; la separación física se mantiene.
- **Criterio de Aceptación**: Las interfaces de usuario de ambas skills son unívocas y no se solapan.
- **Validación**: Auditoría visual de los `resource.yaml` de ambas skills.

---

## 5. Temas que deben seguir abiertos
1. **Views restringidas**: No se implementarán hasta que el flujo de proyectos sea estable.
2. **Memory Viva**: Sigue en fase de diseño; no se moverán archivos de memoria todavía.
3. **Migración de `runtime/`**: Se mantiene en el Workspace como deuda aceptable y funcional.

---

## 6. Orden Recomendado de Ejecución

1.  **Fase 1.1**: `~/AGENTS.md` (Quick Win).
2.  **Fase 1.2**: Inyección de Proyectos en `topology.yaml`.
3.  **Fase 1.3**: Actualización de `navigator.py` para visualizar proyectos.
4.  **Fase 2.1**: Protocolo Git y script de Worktrees.
5.  **Fase 3.1**: Limpieza de interfaces de Management.

---

## 7. Riesgos Globales
- **Inercia**: Tendencia a seguir trabajando en el clone base por costumbre. Mitigación: El `AGENTS.md` de nivel 0 debe ser muy enfático sobre el uso de worktrees.
- **Fragmentación**: Demasiados worktrees si no se limpian. Mitigación: Incluir comando `task close` para eliminar worktrees terminados.

---

## 8. Conclusión
El plan es de bajo riesgo porque se apoya en una estructura de carpetas ya existente y solo requiere actualizaciones de configuración y documentación en su primera fase. El mayor esfuerzo es el cambio cultural hacia el uso de worktrees, que es la clave para la escalabilidad del sistema.
