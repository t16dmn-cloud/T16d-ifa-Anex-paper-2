# T16D–Ifá · Paper 2 · Anexo computacional
**Motor T16D-S — inercia de éxito** · 15 septiembre 2026

Maikel Núñez · Programa T16D–Ifá

Este anexo reproduce el instrumento del Paper 2. No demuestra ⟨R, G, S⟩. Eso es el Paper 1.

El motor no predice un precio. Recibe una firma, aterriza en un vértice del cubo {0,1}⁸ y pregunta dos cosas: en qué órbita cae el cuerpo, y si las dos piernas se desmienten por cruce o por conciliación. Fuente del instrumento desplegado: https://opal-fern-ocean-field.grok.me

---

## 1. Archivos

| archivo | qué es |
|---|---|
| `motor.py` | grupo, conjugación S, score, `evaluar` |
| `grafo.json` | 256 nodos, 342 aristas (320 fibra + 22 conjugadas) |
| `pesos.json` | w1…w13, penalizaciones, umbral de trayectoria |
| `README.md` | instalación y uso |

Solo numpy. Python 3.10+.

```bash
pip install numpy
```

```python
from motor import evaluar, conjugar

r = evaluar({
    "crecimiento": "acelerado",
    "calidad": "declarada",
    "flujoCaja": "alineado",
})
r["nodo"], r["score"], r["histórica"], r["proyectada"], r["veredicto"], r["órbita"]
conjugar(r["nodo"])   # S(L,R) = (rev4(R), rev4(L)) ≡ rev8
```

---

## 2. Gramática (Paper 2, §§1–2)

La firma se escribe \(b = r \| l\).

- Pierna derecha \(r\): lo que el cuerpo declara (valoración, crecimiento, calidad, plantilla).
- Pierna izquierda \(l\): lo que el cuerpo sostiene (caja, flujo, cobrables, ratio).
- \(S\) intercambia las piernas: \(S(L,R) = (\mathrm{rev}_4(R),\mathrm{rev}_4(L))\). En el byte, eso es `rev8`. \(S^2 = 1\).

Veredicto del motor:

- `incongruente` si hay cruce calidad × caja, o si hay ≥ 2 flags de conciliación (ratio bajo/negativo, cobrables baja, empleados desalineado).
- `coherente` en cualquier otro caso.

La conjugación algebraica \(S^2 = 1\) se cumple en los 256 vértices por construcción. El veredicto semántico no es ese test: es la falla de las piernas del 10-K bajo las reglas de cruce y conciliación.

Calidad, flujo y conciliación no mueven el nodo. Mueven el score. La semilla de 8 bits es estructural.

---

## 3. Score

Fórmula (pesos.json, campo `formula`):

```
w1·crecimiento + w2·diversidad + w3·redundancia + w4·apoyo + w5·densidad
+ w9·calidad_ingresos + w10·flujo_caja + w11·ratio_efectivo
+ w12·rotacion_cobrables + w13·empleados
− w6·detractores − w7·espías − w8·tensión_capital
```

Vector, en el orden del campo `orden`:

```
w = (0.2, 0.14, 0.14, 0.12, 0.16, 0.15, 0.2, 0.1, 0.1, 0.1, 0.1, 0.08, 0.06)
```

Penalizaciones adicionales, restadas al total:

| clave | valor |
|---|---|
| cruce_calidad_caja | 0.20 |
| caja_divergente | 0.15 |
| caja_negativo | 0.30 |
| ratio_bajo | 0.10 |
| ratio_negativo | 0.25 |
| cobrables_baja | 0.10 |
| empleados_desalineado | 0.10 |

Umbral de trayectoria: 0.05. Score > 0.05 → histórica ascendente. Score < −0.05 → descendente. El resto, estable.

`w5·densidad` usa el grado del nodo activo sobre el grado máximo del grafo.

---

## 4. Grafo

Grupo: \(\langle R, G, S \rangle \cong\) SmallGroup(16,11) \(\cong C_2 \times D_4\).

Relaciones: \(R^4 = 1\), \(G^2 = 1\), \(S^2 = 1\), \(G\) central, \(SRS = R^{-1}\).

Realización en el byte: \(R = \mathrm{rot}_8(\cdot, 2)\), \(G = \mathrm{inv}_8\), \(S = \mathrm{rev}_8\).

Partición bajo corte pierna-fija (afirmada en el Paper 1, usada aquí): \(2\,D_4 + 12\,C_2 + 2\,V_4\).

256 nodos. 342 aristas no dirigidas, sin bucles.

**Fibra (320).** Misma pierna izquierda \(L\). La derecha \(R\) se transforma por \(\{\mathrm{rot}_4, \mathrm{inv}_4, \mathrm{rev}_4\}\). Se descartan lazos. No dirigidas.

**Conjugadas (22).** Pares \(\{n, S(n)\}\) con \(n < S(n)\), lista cerrada extraída del app:

```
1–128, 2–64, 3–192, 4–32, 6–96, 7–224,
9–144, 11–208, 12–48, 13–176, 14–112,
31–248, 47–244, 63–252, 79–242, 111–246,
127–254, 143–241, 159–249, 191–253, 207–243, 223–251
```

320 + 22 = 342.

Nodo 023, el de la anotación ciega del Paper 2:

| campo | valor |
|---|---|
| id | 23 |
| bits | 00010111 |
| L / tipo | 7 / C2 |
| R / tipo | 1 / C2 |
| peso | 4 |
| capa | media |
| grado | 3 |
| órbita | 8 |
| \|Stab\| | 2 |
| conjugado | 232 = rev8(23) |

---

## 5. `evaluar(firma)`

Entrada: diccionario. Claves usadas (valores categóricos del protocolo del app):

`valoracion`, `crecimiento`, `capex`, `calidad`, `flujoCaja`, `ratioEfectivo`, `rotacionCobrables`, `empleadosIngresos`, `rotacion`, `exposicion`, `diversidad`, `redundancia`, `apoyo`, `detractores`, `fuerza`, `espias`, `fondos`, `nombre`.

Las que faltan toman el default del motor. La semilla de 8 bits se arma solo con marcas estructurales. El nodo activo se elige dentro de la órbita de esa semilla, ranking por score, grado, proximidad de Hamming a la semilla y proximidad de peso.

Salida:

```
nodo, bits, score, histórica, proyectada, veredicto, órbita,
aritmética (L, R, tipos, S_n, stab, peso, capa, grado, densidad),
semilla, g, conjugación_coherente,
incongruencia_conciliacion, cruce_calidad_caja, nombre
```

---

## 6. Frontera de este anexo

Afirma:

- El puerto Python carga el grafo de 256/342 y los trece pesos del app.
- `conjugar` es \(S = \mathrm{rev}_8\).
- `evaluar` reproduce la gramática del Paper 2: órbita, conjugación, score, veredicto.
- El nodo 023 del grafo tiene los campos de la tabla de la §4.

No afirma:

- Que este anexo recalcule el score 0.866 de Palantir. Esa cifra es anotación del motor desplegado, fechada el 15 de septiembre de 2026, sobre cerrado (Paper 2, §5).
- Nodos o scores para Wirecard, Luckin, Theranos o Monster. El cuerpo del Paper 2 no los asigna.
- Que el motor detecte fraude o pronostique precio.
- Que n = 5 sea estadística.

Que Palantir acierte o falle no cambia el álgebra del Paper 1. Cambia la confianza en esta lectura.

---

## 7. Verificación mínima

Correr, desde el directorio de los cuatro archivos:

```bash
python3 -c "from motor import evaluar, conjugar; print(conjugar(23), evaluar({'crecimiento':'acelerado','calidad':'declarada','flujoCaja':'alineado'})['veredicto'])"
```

Esperado: `232 coherente`.

El `assert` de `motor.py` exige `nodeCount == 256` y `edgeCount == 342`. Si el JSON no es el extraído del app, el import falla.

---

## 8. pesos.json (canónico)

```json
{
  "w1": 0.2,
  "w2": 0.14,
  "w3": 0.14,
  "w4": 0.12,
  "w5": 0.16,
  "w6": 0.1,
  "w7": 0.08,
  "w8": 0.06,
  "w9": 0.15,
  "w10": 0.2,
  "w11": 0.1,
  "w12": 0.1,
  "w13": 0.1,
  "orden": ["w1", "w2", "w3", "w4", "w5", "w9", "w10", "w11", "w12", "w13", "w6", "w7", "w8"],
  "vector": [0.2, 0.14, 0.14, 0.12, 0.16, 0.15, 0.2, 0.1, 0.1, 0.1, 0.1, 0.08, 0.06],
  "formula": "w1·crecimiento + w2·diversidad + w3·redundancia + w4·apoyo + w5·densidad + w9·calidad_ingresos + w10·flujo_caja + w11·ratio_efectivo + w12·rotacion_cobrables + w13·empleados − w6·detractores − w7·espías − w8·tensión_capital",
  "penalizaciones": {
    "cruce_calidad_caja": 0.2,
    "caja_divergente": 0.15,
    "caja_negativo": 0.3,
    "ratio_bajo": 0.1,
    "ratio_negativo": 0.25,
    "cobrables_baja": 0.1,
    "empleados_desalineado": 0.1
  },
  "umbral_trayectoria": 0.05,
  "fuente": "https://opal-fern-ocean-field.grok.me"
}
```

`motor.py` y `grafo.json` van en el zip de este anexo. No se reimprimen aquí: el primero son 465 líneas; el segundo, 256 nodos y 342 aristas.

Programa T16D–Ifá · Paper 2 · anexo computacional · fin
