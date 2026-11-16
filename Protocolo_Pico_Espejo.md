# T16D–Ifá · Protocolo Pico Espejo (ventana S)

**16 noviembre 2026** · Diseño preliminar · Programa T16D–Ifá

## Objetivo
Diseñar un protocolo computacional o experimental que use la conjugación σ = GRS = rev8 para buscar una firma (pico) distinguible del azar, usando solo la estructura verificada del cubo.

## Diseño preliminar
1. Mapear un conjunto de datos a vértices del cubo {0,1}⁸.
2. Para cada vértice, calcular su conjugado bajo σ = rev8.
3. Medir alguna distancia o correlación entre el vértice y su conjugado (peso de Hamming de la diferencia, órbita compartida, etc.).
4. Comparar la distribución observada contra el azar uniforme o contra un modelo nulo de permutación.

## Criterio de falsación
Si no hay exceso estadísticamente significativo de correlación o de pico en la distribución de distancias conjugadas, la ventana no aporta evidencia.

## Lo que NO se afirma
- Que un resultado positivo mida energía o carrier físico.
- Cualquier interpretación ontológica.
- Que el protocolo esté listo para datos reales (esto es solo diseño).

Este documento deja la ventana explícita y lista para que el Abogado del Diablo la ataque o para que se refine con datos sintéticos.

Repo: https://github.com/t16dmn-cloud/T16d-ifa-Anex-paper-2
