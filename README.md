# T16D-S — Motor de Inercia de Éxito

Puerto Python del clasificador en https://opal-fern-ocean-field.grok.me

256 nodos, 342 aristas, ⟨R, G, S⟩ ≅ SmallGroup(16,11), partición 2 D₄ + 12 C₂ + 2 V₄.
No es oráculo. Clasifica una firma sobre {0,1}⁸: órbita, conjugación S, score.

## Instalación

```bash
pip install numpy
```

Solo numpy. Python 3.10+.

## Uso

```python
from motor import evaluar, conjugar

r = evaluar({
    "crecimiento": "acelerado",
    "calidad": "declarada",
    "flujoCaja": "alineado",
})
r["nodo"], r["score"], r["histórica"], r["proyectada"], r["veredicto"], r["órbita"]
conjugar(r["nodo"])   # S(L,R) = (rev4(R), rev4(L))
```

`evaluar(firma)` recibe un diccionario de parámetros y devuelve nodo, score, histórica, proyectada, veredicto, órbita y aritmética de posición.

Veredicto = `incongruente` si hay cruce calidad × caja, o si ≥2 flags de conciliación (ratio bajo/negativo, cobrables baja, empleados desalineado). Si no, `coherente`.

## Archivos

- `motor.py` — grupo, conjugación S, score, `evaluar`
- `grafo.json` — 256 nodos, 342 aristas extraídos del app
- `pesos.json` — w1…w13 y penalizaciones
- `README.md` — este archivo

## Score

```
w1·crecimiento + w2·diversidad + w3·redundancia + w4·apoyo + w5·densidad
+ w9·calidad_ingresos + w10·flujo_caja + w11·ratio_efectivo
+ w12·rotacion_cobrables + w13·empleados
− w6·detractores − w7·espías − w8·tensión_capital
```

w = (0.2, 0.14, 0.14, 0.12, 0.16, 0.15, 0.2, 0.1, 0.1, 0.1, 0.1, 0.08, 0.06)

Calidad, flujo y conciliación no mueven el nodo (score-only). Semilla = 8 bits estructurales.
