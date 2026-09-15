# T16D–Ifá · Errata de álgebra
**15 septiembre 2026** · Maikel Núñez

Había dos realizaciones distintas etiquetadas con los mismos nombres R, G, S. Queda una.

## Qué estaba mal

`paper1_rama_d.py` (Anexo Paper 1) genera el grupo de la escritura:

```
S = (0 4)(1 5)(2 6)(3 7)     # intercambio de piernas
R = (0 1 2 3)(4 5 6 7)       # rotación de filas, igual en las dos columnas
G = (1 3)(5 7)               # reflexión de filas, igual en las dos columnas
```

Orden 16 en S₈. No abeliano. ≅ SmallGroup(16,11) ≅ C₂ × D₄.
34 órbitas en V. 10 en W. Polos 0 y 255 fijos y separados. Firma 2 D₄ + 12 C₂ + 2 V₄.

`motor_inercia.py` usaba otros mapas con los mismos nombres:

```
R_app = rot8(·, 2)     # orden 8 junto con rev8: solo D₄
S_app = rev8           # no es el swap de piernas
G_app = inv8 = XOR FF  # complemento bit a bit, afín, no vive en S₈
```

Ese G_app es el operador que el Paper 1 declaró **externo**. Con él, 0 y 255 caen en la misma órbita y el cubo se parte en **27** órbitas, no 34. Mismo grupo abstracto C₂ × D₄, **otra acción**.

El par 23 ↔ 232 del app es `rev8(23) = 232`. Bajo la S del Paper 1, S(23) = 113. 232 sí vive en la órbita Rama D de 23; no es S(23).

## Regla que queda

1. Los nombres R, G, S significan solo Rama D (`paper1_rama_d.py`).
2. El complemento se llama complemento. No se llama G.
3. `rev8` se llama espejo del app. No se llama S.
4. La anotación Palantir 023 / 0.866 / conjugado 232 pertenece al instrumento desplegado (rev8), no a la S de la escritura.
5. Si el puerto Python unifica `orbit_of` a Rama D, hay que regenerar `grafo.json` y reescribir el ejemplo nodo 74 / score 0.901 del Paper 3. Hasta que eso ocurra, `evaluar()` sigue siendo el puerto del app, no la demostración del Paper 1.

## Verificación mínima

```
python paper1_rama_d.py
# orden 16, firma D4:2 C2:12 V4:2, orbitas_W 10, rama_I_orden 128 STOP
```

Repositorio: https://github.com/t16dmn-cloud/T16d-ifa-Anex-paper-2
