"""Motor de Inercia de Éxito T16D-S.

Puerto fiel del clasificador en
https://opal-fern-ocean-field.grok.me
(256 nodos, 342 aristas, ⟨R,G,S⟩ ≈ SmallGroup(16,11)).

No es oráculo. Lee una firma sobre {0,1}⁸, aterriza en una órbita
y comprueba si las dos piernas se conjugan por S.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# bits
# ---------------------------------------------------------------------------


def popcount(n: int) -> int:
    return int(n & 0xFF).bit_count()


def rot4(n: int, k: int = 1) -> int:
    x = n & 0xF
    s = k & 3
    return ((x << s) | (x >> (4 - s))) & 0xF


def rev4(n: int) -> int:
    r = 0
    for i in range(4):
        if n & (1 << i):
            r |= 1 << (3 - i)
    return r


def inv4(n: int) -> int:
    return n ^ 0xF


def rot8(n: int, k: int = 2) -> int:
    x = n & 0xFF
    s = k & 7
    return ((x << s) | (x >> (8 - s))) & 0xFF


def rev8(n: int) -> int:
    r = 0
    for i in range(8):
        if n & (1 << i):
            r |= 1 << (7 - i)
    return r


def inv8(n: int) -> int:
    return n ^ 0xFF


def left_leg(n: int) -> int:
    return n & 0xF


def right_leg(n: int) -> int:
    return (n >> 4) & 0xF


def pack_legs(left: int, right: int) -> int:
    return (left & 0xF) | ((right & 0xF) << 4)


def hamming(a: int, b: int) -> int:
    return popcount(a ^ b)


def leg_type(n: int) -> str:
    x = n & 0xF
    if x in (0, 15):
        return "D4"
    if x in (5, 10):
        return "V4"
    return "C2"


def layer_of(weight: int) -> str:
    if weight <= 2:
        return "baja"
    if weight <= 5:
        return "media"
    return "alta"


def conjugar(b: int) -> int:
    """Acción de S: S(L, R) = (rev4(R), rev4(L)). Equivale a rev8. S² = 1."""
    return rev8(int(b) & 0xFF)


def conjugacion_coherente(b: int) -> bool:
    """S² = id y S realiza el espejo de nibbles (rev8)."""
    b = int(b) & 0xFF
    s = conjugar(b)
    return conjugar(s) == b and s == pack_legs(rev4(right_leg(b)), rev4(left_leg(b)))


# ---------------------------------------------------------------------------
# grupo ⟨R, G, S⟩ ≈ C2 × D4 ≈ SmallGroup(16,11)
# g = G^γ S^σ R^ρ ; R = rot8(·, 2), G = inv8, S = rev8
# ---------------------------------------------------------------------------

_ELEMENTS: list[dict] = []
for _gamma in (0, 1):
    for _sigma in (0, 1):
        for _rho in (0, 1, 2, 3):
            parts: list[str] = []
            if _gamma:
                parts.append("G")
            if _sigma:
                parts.append("S")
            if _rho == 1:
                parts.append("R")
            elif _rho == 2:
                parts.append("R²")
            elif _rho == 3:
                parts.append("R³")
            _ELEMENTS.append(
                {
                    "gamma": _gamma,
                    "sigma": _sigma,
                    "rho": _rho,
                    "word": "".join(parts) or "1",
                }
            )


def apply8(gamma: int, sigma: int, rho: int, x: int) -> int:
    y = x & 0xFF
    for _ in range(rho):
        y = rot8(y, 2)
    if sigma:
        y = rev8(y)
    if gamma:
        y = inv8(y)
    return y


def orbit_of(node: int) -> list[int]:
    seen = {apply8(e["gamma"], e["sigma"], e["rho"], node) for e in _ELEMENTS}
    return sorted(seen)


def word_from_to(src: int, dst: int) -> str | None:
    dst &= 0xFF
    for e in _ELEMENTS:
        if apply8(e["gamma"], e["sigma"], e["rho"], src) == dst:
            return e["word"]
    return None


# ---------------------------------------------------------------------------
# grafo + pesos extraídos del app
# ---------------------------------------------------------------------------

with (_DIR / "grafo.json").open(encoding="utf-8") as _f:
    GRAFO = json.load(_f)
with (_DIR / "pesos.json").open(encoding="utf-8") as _f:
    PESOS = json.load(_f)

NODOS = GRAFO["nodes"]
ARISTAS = GRAFO["edges"]
N_NODOS = int(GRAFO["nodeCount"])
N_ARISTAS = int(GRAFO["edgeCount"])
assert N_NODOS == 256
assert N_ARISTAS == 342
assert len(NODOS) == 256
assert len(ARISTAS) == 342

_ADJ: list[list[int]] = [[] for _ in range(256)]
for _e in ARISTAS:
    _ADJ[_e["a"]].append(_e["b"])
    _ADJ[_e["b"]].append(_e["a"])
for _lst in _ADJ:
    _lst.sort()

ADJ = np.zeros((256, 256), dtype=np.int8)
for _e in ARISTAS:
    ADJ[_e["a"], _e["b"]] = 1
    ADJ[_e["b"], _e["a"]] = 1

GRADOS = ADJ.sum(axis=1).astype(int)
MAX_GRADO = int(GRADOS.max())


def densidad(degree: int) -> float:
    return 0.0 if MAX_GRADO == 0 else degree / MAX_GRADO


# ---------------------------------------------------------------------------
# parámetros → semilla 8 bits + score
# ---------------------------------------------------------------------------

STEP = {
    "baja": 0.0,
    "media": 0.5,
    "alta": 1.0,
    "extrema": 1.0,
    "negativo": 0.0,
    "plano": 0.33,
    "positivo": 0.66,
    "acelerado": 1.0,
    "sostenible": 0.0,
    "tenso": 0.55,
    "critico": 1.0,
    "ninguno": 0.0,
    "ninguna": 0.0,
    "pocos": 0.45,
    "poca": 0.45,
    "muchos": 1.0,
    "mucha": 1.0,
    "parcial": 0.5,
    "fuerte": 1.0,
    "debil": 0.3,
    "declarada": 1.0,
    "no_verificable": 0.4,
    "no_reportada": 0.0,
    "alineado": 1.0,
    "divergente": 0.0,
    "alto": 1.0,
    "normal": 0.5,
    "bajo": 0.0,
    "desalineado": 0.0,
}

DEFAULT_FIRMA = {
    "nombre": "",
    "valoracion": "media",
    "crecimiento": "positivo",
    "capex": "tenso",
    "calidad": "declarada",
    "flujoCaja": "alineado",
    "ratioEfectivo": "normal",
    "rotacionCobrables": "normal",
    "empleadosIngresos": "alineado",
    "rotacion": "media",
    "exposicion": "media",
    "diversidad": "media",
    "redundancia": "baja",
    "apoyo": "parcial",
    "detractores": "pocos",
    "fuerza": "media",
    "espias": "poca",
    "fondos": "ninguno",
}

W = PESOS
P = PESOS["penalizaciones"]


def _n01(value: str) -> float:
    return float(STEP.get(value, 0.5))


def features_of(firma: dict) -> dict:
    f = {**DEFAULT_FIRMA, **firma}
    crecimiento = _n01(f["crecimiento"])
    diversidad = _n01(f["diversidad"])
    redundancia = _n01(f["redundancia"])
    apoyo = min(1.0, _n01(f["apoyo"]) + 0.22 * _n01(f["fondos"]))
    detractores = min(
        1.0,
        _n01(f["detractores"])
        * (0.45 + 0.55 * _n01(f["fuerza"]))
        * (0.75 + 0.35 * _n01(f["exposicion"])),
    )
    espias = _n01(f["espias"])
    tension = _n01(f["capex"])
    calidad = _n01(f["calidad"])
    flujo = _n01(f["flujoCaja"])
    cruce = f["calidad"] in ("no_verificable", "no_reportada") and f["flujoCaja"] in (
        "divergente",
        "negativo",
    )
    if f["flujoCaja"] == "negativo":
        caja_pen = P["caja_negativo"]
    elif f["flujoCaja"] == "divergente":
        caja_pen = P["caja_divergente"]
    else:
        caja_pen = 0.0
    ratio = _n01(f["ratioEfectivo"])
    if f["ratioEfectivo"] == "negativo":
        ratio_pen = P["ratio_negativo"]
    elif f["ratioEfectivo"] == "bajo":
        ratio_pen = P["ratio_bajo"]
    else:
        ratio_pen = 0.0
    cobrables = _n01(f["rotacionCobrables"])
    cob_pen = P["cobrables_baja"] if f["rotacionCobrables"] == "baja" else 0.0
    empleados = _n01(f["empleadosIngresos"])
    emp_pen = P["empleados_desalineado"] if f["empleadosIngresos"] == "desalineado" else 0.0
    flags = [
        f["ratioEfectivo"] in ("bajo", "negativo"),
        f["rotacionCobrables"] == "baja",
        f["empleadosIngresos"] == "desalineado",
    ]
    incongruencia = sum(flags) >= 2
    rotacion_baja = 1.0 - _n01(f["rotacion"])

    seed = 0
    if _n01(f["valoracion"]) >= 0.66:
        seed |= 1 << 0
    if crecimiento >= 0.66:
        seed |= 1 << 1
    if tension < 0.4:
        seed |= 1 << 2
    if rotacion_baja >= 0.6:
        seed |= 1 << 3
    if diversidad >= 0.5:
        seed |= 1 << 4
    if redundancia >= 0.5:
        seed |= 1 << 5
    if apoyo >= 0.5:
        seed |= 1 << 6
    if detractores < 0.35 and espias < 0.4:
        seed |= 1 << 7

    return {
        "crecimiento": crecimiento,
        "diversidad": diversidad,
        "redundancia": redundancia,
        "apoyo": apoyo,
        "detractores": detractores,
        "espias": espias,
        "tension": tension,
        "calidad": calidad,
        "cruce": cruce,
        "flujo": flujo,
        "caja_pen": caja_pen,
        "ratio": ratio,
        "ratio_pen": ratio_pen,
        "cobrables": cobrables,
        "cob_pen": cob_pen,
        "empleados": empleados,
        "emp_pen": emp_pen,
        "incongruencia": incongruencia,
        "seed": seed,
        "firma": f,
    }


def score_of(node: dict, feat: dict) -> float:
    dens = densidad(node["degree"])
    total = (
        W["w1"] * feat["crecimiento"]
        + W["w2"] * feat["diversidad"]
        + W["w3"] * feat["redundancia"]
        + W["w4"] * feat["apoyo"]
        + W["w5"] * dens
        + W["w9"] * feat["calidad"]
        + W["w10"] * feat["flujo"]
        + W["w11"] * feat["ratio"]
        + W["w12"] * feat["cobrables"]
        + W["w13"] * feat["empleados"]
        - W["w6"] * feat["detractores"]
        - W["w7"] * feat["espias"]
        - W["w8"] * feat["tension"]
        - (P["cruce_calidad_caja"] if feat["cruce"] else 0.0)
        - feat["caja_pen"]
        - feat["ratio_pen"]
        - feat["cob_pen"]
        - feat["emp_pen"]
    )
    return float(total)


def _rank_key(node: dict, feat: dict, seed_w: int) -> tuple:
    s = score_of(node, feat)
    return (
        s,
        node["degree"],
        -hamming(node["id"], feat["seed"]),
        -abs(node["weight"] - seed_w),
        -node["id"],
    )


def pick_active(feat: dict) -> tuple[dict, float]:
    pool = [NODOS[i] for i in orbit_of(feat["seed"])]
    seed_w = popcount(feat["seed"])
    best = pool[0]
    best_key = _rank_key(best, feat, seed_w)
    for node in pool[1:]:
        key = _rank_key(node, feat, seed_w)
        if key > best_key:
            best = node
            best_key = key
    return best, score_of(best, feat)


def trayectoria_de_score(score: float) -> str:
    band = W["umbral_trayectoria"]
    if score > band:
        return "ascendente"
    if score < -band:
        return "descendente"
    return "estable"


def _proyectada(node: dict, feat: dict, score: float) -> str:
    hist = trayectoria_de_score(score)
    if hist == "descendente":
        return "bajo presión"
    pressure = feat["detractores"] > 0.55 or feat["espias"] > 0.55 or feat["tension"] > 0.7
    if hist == "estable":
        return "bajo presión" if pressure else "estable"
    if pressure:
        return "estable" if node["layer"] == "alta" else "bajo presión"
    return "ascendente"


def evaluar(firma: dict) -> dict:
    """Clasifica una firma. Devuelve posición estructural, no un pronóstico."""
    feat = features_of(firma)
    node, score = pick_active(feat)
    orbita = orbit_of(node["id"])
    s_n = conjugar(node["id"])
    piernas_ok = conjugacion_coherente(node["id"])
    if feat["incongruencia"] or feat["cruce"]:
        veredicto = "incongruente"
    else:
        veredicto = "coherente"
    hist = trayectoria_de_score(score)
    return {
        "nodo": node["id"],
        "bits": node["bits"],
        "score": round(score, 12),
        "histórica": hist,
        "proyectada": _proyectada(node, feat, score),
        "veredicto": veredicto,
        "órbita": orbita,
        "aritmética": {
            "L": node["left"],
            "L_tipo": node["leftType"],
            "R": node["right"],
            "R_tipo": node["rightType"],
            "L_bin": format(node["left"], "04b"),
            "R_bin": format(node["right"], "04b"),
            "S_n": s_n,
            "stab": node["stabilizerOrder"],
            "peso": node["weight"],
            "capa": node["layer"],
            "grado": node["degree"],
            "densidad": node["density"],
        },
        "semilla": feat["seed"],
        "g": word_from_to(feat["seed"], node["id"]),
        "conjugación_coherente": piernas_ok,
        "incongruencia_conciliacion": feat["incongruencia"],
        "cruce_calidad_caja": feat["cruce"],
        "nombre": feat["firma"].get("nombre", ""),
    }
