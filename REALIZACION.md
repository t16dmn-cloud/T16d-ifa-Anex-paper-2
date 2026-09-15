# Realización única de ⟨R, G, S⟩

15 septiembre 2026 · Paper 1 + anexo Paper 2

No hay dos grupos. Había dos *nombres* para mapas distintos.

## Canón (escritura, Paper 1, `paper1_rama_d.py`)

Coordenadas: derecha {0,1,2,3}, izquierda {4,5,6,7}.

```
S = (0 4)(1 5)(2 6)(3 7)     intercambiar piernas
R = (0 1 2 3)(4 5 6 7)     rotar las dos columnas igual
G = (1 3)(5 7)               reflexión diagonal
```

Orden 16 ≅ SmallGroup(16,11) ≅ C₂ × D₄. Rama I (columnas independientes) = 128: parada.
El complemento bit a bit **no** es generador. Es el operador afín externo.

## Qué era el `S` del motor

`conjugar` en `motor_inercia.py` aplica `rev8`:

```
S_motor(L, R) = (rev4(R), rev4(L)) = rev8
```

Ese mapa **está en el grupo del Paper 1**:

```
rev8 = G ∘ R ∘ S
```

(composición a izquierda: primero S, luego R, luego G).

No es un segundo generador. Es la palabra `GRS`.
`conjugar(23) = 232` se mantiene: 232 = rev8(23) = (GRS)(23).

## Qué no se mezcla

| nombre en el motor | objeto real |
|---|---|
| `S` / `rev8` / `conjugar` | elemento GRS del grupo del Paper 1 |
| `R` / `rot8(·,2)` | otra rotación de 8 bits; **no** es el R diagonal |
| `G` / `inv8` | complemento `xor 0xFF`; operador afín externo, no el G del Paper 1 |

`inv8` intercambia los polos. Por eso **no** puede ser generador del Paper 1: rompería el criterio de los dos fijos puntuales (Eyiogbe y Z).

## Regla de ahora

1. S significa intercambio de piernas.
2. La conjugación que corre el motor se llama σ = GRS = rev8.
3. El complemento se llama complemento, no G.

El álgebra del Paper 1 no cambia. El puerto Python no cambia de salida (`conjugar(23)` sigue siendo 232). Cambia el nombre para que no parezcan dos grupos.
