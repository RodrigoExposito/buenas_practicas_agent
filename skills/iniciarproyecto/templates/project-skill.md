---
name: convenciones-{{dominio}}
description: Convenciones obligatorias para escribir {{qué: endpoints de API / componentes de UI / acceso a datos}} en este proyecto. Usar siempre que se cree o modifique {{dónde: archivos en app/api/ ...}}.
---

# Convenciones: {{dominio}}

## Cuándo aplica
{{rutas o tipos de archivo}}

## Patrón obligatorio
```{{lenguaje}}
{{ejemplo mínimo y real del patrón: estructura, validación de input, manejo de errores, respuesta}}
```

## Reglas
- {{ej: validar input con zod en la primera línea del handler}}
- {{ej: errores de negocio devuelven 4xx con { error: string }, nunca throw sin capturar}}
- {{ej: nada de SQL fuera de lib/db.ts}}

## Antipatrones (no hacer)
- {{ej: try/catch vacío}}
- {{ej: lógica de negocio en el componente}}
