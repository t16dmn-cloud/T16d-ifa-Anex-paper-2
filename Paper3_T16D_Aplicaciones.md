# T16D–Ifá · Paper 3
## Aplicaciones del motor T16D-S: protocolo, lectura y frontera

**Maikel Núñez** · Programa T16D–Ifá  
15 de septiembre de 2026

---

### Resumen

El Paper 1 fija el álgebra: $\langle R, G, S \rangle \cong$ SmallGroup(16,11) $\cong C_2 \times D_4$, realizado en el byte por $R = \mathrm{rot}_8(\cdot,2)$, $G = \mathrm{inv}_8$, $S = \mathrm{rev}_8$. El Paper 2 fija la gramática: una firma sobre $\{0,1\}^8$, órbita, conjugación $S$ y un score de trece pesos. Este Paper 3 no demuestra ni lo uno ni lo otro. Dice cómo se *aplica* el instrumento, qué sale de `evaluar(firma)`, y qué no se puede afirmar todavía.

El motor no predice un precio. No detecta fraude. Recibe una firma, aterriza en un vértice del cubo y pregunta dos cosas: en qué órbita cae el cuerpo, y si las dos piernas se desmienten por cruce o por conciliación.

**Palabras clave:** T16D-S, SmallGroup(16,11), conjugación $S$, firma estructural, veredicto de coherencia.

---

## 1. Qué cierra este paper

Tres piezas, tres funciones:

| paper | función | lo que no hace |
|---|---|---|
| Paper 1 | existencia y presentación del grupo; Rama D de orden 16; firma $2\,D_4 + 12\,C_2 + 2\,V_4$; Rama I explota | no lee un 10-K |
| Paper 2 | gramática de la firma, score, veredicto, grafo 256/342 | no es un panel estadístico |
| Paper 3 | protocolo de aplicación y frontera de lectura | no inventa nodos para cuerpos no firmados |

El ciclo publicable no está cerrado mientras los *textos* de los Papers 1 y 2 no estén depositados junto a sus anexos. Este documento solo cubre la tercera pata: aplicación.

Código canónico:

- Anexo Paper 1: `paper1_rama_d.py`
- Anexo Paper 2: `motor.py`, `motor_inercia.py`, `grafo.json`, `pesos.json`
- Repositorio: https://github.com/t16dmn-cloud/T16d-ifa-Anex-paper-2

---

## 2. El instrumento que se aplica

Una firma es un diccionario de marcas categóricas del protocolo del app. Las claves usadas son:

`valoracion`, `crecimiento`, `capex`, `calidad`, `flujoCaja`, `ratioEfectivo`, `rotacionCobrables`, `empleadosIngresos`, `rotacion`, `exposicion`, `diversidad`, `redundancia`, `apoyo`, `detractores`, `fuerza`, `espias`, `fondos`, `nombre`.

Las que faltan toman el default del motor. La semilla de 8 bits se arma solo con marcas estructurales. Calidad, flujo y conciliación no mueven el nodo: mueven el score.

`evaluar(firma)` devuelve, entre otros campos:

`nodo`, `bits`, `score`, `histórica`, `proyectada`, `veredicto`, `órbita`, `aritmética`, `semilla`, `conjugación_coherente`, `incongruencia_conciliacion`, `cruce_calidad_caja`.

Veredicto:

- `incongruente` si hay cruce calidad × caja, o si hay $\ge 2$ flags de conciliación (ratio bajo/negativo, cobrables baja, empleados desalineado).
- `coherente` en cualquier otro caso.

La conjugación algebraica $S^2 = 1$ se cumple en los 256 vértices por construcción. El veredicto semántico no es ese test: es la falla de las piernas bajo las reglas de cruce y conciliación.

Score (campo `formula` de `pesos.json`):

```
w1·crecimiento + w2·diversidad + w3·redundancia + w4·apoyo + w5·densidad
+ w9·calidad_ingresos + w10·flujo_caja + w11·ratio_efectivo
+ w12·rotacion_cobrables + w13·empleados
− w6·detractores − w7·espías − w8·tensión_capital
```

Vector, en el orden del campo `orden`:

$w = (0.2,\, 0.14,\, 0.14,\, 0.12,\, 0.16,\, 0.15,\, 0.2,\, 0.1,\, 0.1,\, 0.1,\, 0.1,\, 0.08,\, 0.06)$.

Umbral de trayectoria: $0.05$. Score $> 0.05$ → histórica ascendente. Score $< -0.05$ → descendente. El resto, estable.

---

## 3. Protocolo de lectura de un cuerpo

Aplicar el motor a un emisor —una compañía, un fondo, un estado— es un acto de *codificación*, no de oráculo. El protocolo tiene cuatro pasos.

**Paso 1. Separar las piernas.**  
Pierna derecha $R$: lo que el cuerpo declara (valoración, crecimiento, calidad, plantilla).  
Pierna izquierda $L$: lo que el cuerpo sostiene (caja, flujo, cobrables, ratio).  
$S$ intercambia las piernas: $S(L,R) = (\mathrm{rev}_4(R),\, \mathrm{rev}_4(L)) \equiv \mathrm{rev}_8$.

**Paso 2. Traducir el 10-K (o el estado equivalente) a marcas categóricas.**  
Cada clave toma un valor del vocabulario del app (`acelerado`, `declarada`, `alineado`, `divergente`, `bajo`, …). La traducción es una decisión del lector. Dos lectores honestos pueden discrepar en una marca. El paper no resuelve esa disputa: exige que la firma quede escrita y fechada.

**Paso 3. Correr `evaluar`.**  
El motor elige el nodo activo dentro de la órbita de la semilla, ranking por score, grado, proximidad de Hamming a la semilla y proximidad de peso.

**Paso 4. Leer el veredicto como gramática, no como sentencia.**  
`coherente` no significa «sano». Significa: bajo las reglas de cruce y conciliación, las piernas no se desmienten. `incongruente` no significa «fraude». Significa: las piernas se desmienten.

---

## 4. Ejemplo runnable (anexo Paper 2, §7)

Desde el directorio del anexo:

```python
from motor import evaluar, conjugar

print(conjugar(23))
r = evaluar({
    "crecimiento": "acelerado",
    "calidad": "declarada",
    "flujoCaja": "alineado",
})
print(r["nodo"], r["score"], r["veredicto"], r["histórica"])
```

Salida verificada el 15 de septiembre de 2026 sobre el commit del anexo:

- `conjugar(23) = 232`
- nodo activo $74$
- score $\approx 0.901$
- veredicto `coherente`
- histórica `ascendente`

Ese ejemplo no es una empresa. Es una firma mínima: crecimiento acelerado, calidad declarada, caja alineada, el resto en default. Sirve para que un revisor reproduzca el instrumento, no para tasar un ticker.

El mismo motor, con cruce calidad $\times$ caja o con dos flags de conciliación, devuelve `incongruente`. Eso también es reproducible y no asigna un nombre propio.

---

## 5. Palantir como anotación cerrada

El anexo del Paper 2 registra una anotación del motor *desplegado* (https://opal-fern-ocean-field.grok.me), fechada el 15 de septiembre de 2026, sobre cerrado: score $0.866$ para Palantir. Ese número no se reimprime aquí como recálculo del puerto Python. El anexo lo dice con claridad: este material no afirma que el puerto reproduzca $0.866$.

Lo que sí afirma este paper:

1. Existe un instrumento desplegado y un puerto Python del mismo clasificador.
2. La anotación de Palantir pertenece al instrumento desplegado, no al anexo.
3. Que Palantir acierte o falle no cambia el álgebra del Paper 1. Cambia la confianza en *esta* lectura.

No se publica aquí la firma categórica completa que produjo esa anotación. Sin esa firma, nadie puede auditar el $0.866$ desde `evaluar()`. Eso es una laguna de aplicación, no un resultado.

---

## 6. Casos que este paper no asigna

El cuerpo del Paper 2 no asigna nodos ni scores a Wirecard, Luckin, Theranos ni Monster. Este Paper 3 tampoco.

Nombrar esos cuerpos sirve solo para marcar el tipo de pregunta que *un* estudio de aplicación tendría que hacer:

- ¿La pierna declarada (calidad, crecimiento) se sostiene en caja y cobrables, o se desmiente?
- ¿Cuántos flags de conciliación habría que marcar, y con qué fecha de 10-K?

Hasta que alguien escriba la firma, feche el documento fuente y corra `evaluar`, no hay nodo. Inventar el nodo para «demostrar» que el motor «caza fraudes» sería exactamente lo que el anexo prohíbe.

Tampoco se afirma:

- que el motor detecte fraude;
- que pronostique precio;
- que $n = 5$ sea estadística;
- que una órbita de tamaño 8 sea un rating.

---

## 7. Qué haría falta para un estudio de aplicación

Un Paper 3 *empírico* —distinto de este protocolo— exigiría, como mínimo:

1. Un panel de emisores con 10-K (o equivalente) fechado.
2. Una firma escrita por emisor, con regla de código visible para cada marca.
3. Doble lectura independiente de un subconjunto, para medir desacuerdo entre codificadores.
4. Salida cruda de `evaluar` por emisor: nodo, órbita, score, veredicto, flags.
5. Un desenlace posterior —impago, restatement, fraude adjudicado, supervivencia— que *no* entre en la firma.
6. La admisión de que el veredicto es una etiqueta gramatical, no una probabilidad.

Sin esos seis puntos, lo que hay es instrumento + protocolo. No hay validación.

---

## 8. Conclusión

El trabajo T16D–Ifá, para publicarse como ciclo, necesita tres textos y dos anexos. Los anexos ya están en GitHub. Este Paper 3 deja escrito el modo de uso:

- se firma un cuerpo;
- se corre `evaluar`;
- se lee órbita, conjugación y veredicto;
- no se finge un panel que no existe.

La aplicación honesta del motor es estrecha. Esa estrechez es la condición para que el álgebra del Paper 1 y la gramática del Paper 2 sobrevivan a la primera lectura hostil.

---

## Referencias de trabajo

- Núñez, M. *T16D–Ifá · Paper 1 · Rama D.* Anexo computacional: `paper1_rama_d.py`.
- Núñez, M. *T16D–Ifá · Paper 2 · Gramática y motor T16D-S.* Anexo: `ANEXO_NOTA.md`, `motor.py`, `grafo.json`, `pesos.json`.
- Repositorio: https://github.com/t16dmn-cloud/T16d-ifa-Anex-paper-2
- Instrumento desplegado: https://opal-fern-ocean-field.grok.me

Programa T16D–Ifá · Paper 3 · aplicaciones · fin
