# T16D–Ifá · Paper 1 · 15 septiembre 2026

**PROGRAMA T16D–IFÁ**  
El cubo {0,1}⁸ de Ifá bajo ⟨R, G, S⟩ ≅ C₂ × D₄: W de peso 4, 34 órbitas y unicidad acotada

**Maikel Núñez**

Anexo: [paper1_rama_d.py](paper1_rama_d.py)  
Repo: https://github.com/t16dmn-cloud/T16d-ifa-Anex-paper-2

## Resumen

Escritura —no ontología física— sobre el cubo {0,1}⁸. Cada vértice es un Odù: b = r ‖ l. El grupo ⟨R, G, S⟩ tiene orden 16 e isomorfismo SmallGroup(16,11) ≅ C₂ × D₄. El corte pierna-fija da la firma 2 D₄ + 12 C₂ + 2 V₄. W (peso 4) tiene 70 estados y 10 órbitas; ningún punto de W es fijo puntual. Los únicos fijos puntuales son Eyiogbe y Z := Oyeku Méjì (pesos 0 y 8). Hay 34 órbitas en V. Bajo complemento de órbitas hay 22 tipos, no 23 = 15+8.

Ifá entra como sistema de conocimiento con estructura medible. Nombrar un estado no es anunciar un precio.

## Grupo (Rama D)

```
S = (0 4)(1 5)(2 6)(3 7)     intercambio de piernas
R = (0 1 2 3)(4 5 6 7)     rotar las dos columnas igual
G = (1 3)(5 7)               reflexión diagonal
```

Orden 16, no abeliano. Rama I (columnas independientes) orden 128: parada.
El complemento (`inv8`) no es G. `rev8` no es S: `rev8 = G ∘ R ∘ S`.

## Firma, W, órbitas

Firma bajo corte pierna-fija: 2 D₄ + 12 C₂ + 2 V₄.
W = 70 estados, 10 órbitas (tamaños 2,2,2,4,4,8,8,8,16,16), 0 fijos en W.
Fix V = {Eyiogbe, Z}. 34 órbitas en V.

## Frontera

Afirma el grupo, la firma, 34, W/10, los dos polos.
No afirma κ, F, carrier físico, que los polos vivan en W, ni 15+8 como conteo independiente.

Errata: la primera emisión mezclaba Z y Eyiogbe con W.

Programa T16D–Ifá · Paper 1 · fin
