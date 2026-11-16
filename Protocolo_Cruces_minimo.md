# T16D–Ifá · Protocolo mínimo de cruces

**16 noviembre 2026** · Maikel Núñez / Programa T16D–Ifá

## Objetivo
Diseñar un test falsable que use solo la estructura ya verificada del cubo {0,1}⁸ bajo ⟨R, G, S⟩, sin introducir energía, κ, F, o carrier físico.

## Hipótesis a probar
Que la pertenencia a una órbita de tamaño determinado, o la conjugación bajo σ = GRS, correlaciona con alguna propiedad externa medible más allá del azar.

## Diseño mínimo
1. Tomar un conjunto de firmas externas (datos reales o sintéticos etiquetados).
2. Mapear cada firma a un vértice del cubo (8 bits estructurales).
3. Calcular:
   - Órbita bajo el grupo Rama D.
   - Tamaño de la órbita.
   - Conjugado bajo σ = rev8 = GRS.
4. Comparar la distribución observada de tamaños de órbita o de cruces (calidad × caja, etc.) contra el azar uniforme sobre el cubo.

## Criterio de falsación
Si la distribución no se distingue del azar (p > 0.05 tras corrección, o potencia insuficiente), el protocolo no aporta evidencia a favor de estructura Ifá más allá del cubo genérico.

## Lo que NO se afirma
- Que esto mida energía.
- Que el resultado positivo implique carrier físico.
- Cualquier predicción de precio o magnitud continua.

Este documento es solo el diseño. No se ha corrido ninguna prueba sobre datos reales.

Repo: https://github.com/t16dmn-cloud/T16d-ifa-Anex-paper-2
