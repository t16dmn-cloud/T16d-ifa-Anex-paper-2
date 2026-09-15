# Nota sobre motor.py y grafo.json

El anexo canónico (README.md) indica que `motor.py` (465 líneas) y `grafo.json` (256 nodos, 342 aristas) van en el zip del anexo y no se reimprimen en el texto.

Cuando tengas esos dos archivos, pégalos aquí o mándamelos y los subo en el siguiente commit.

Verificación esperada:

```bash
python3 -c "from motor import evaluar, conjugar; print(conjugar(23), evaluar({'crecimiento':'acelerado','calidad':'declarada','flujoCaja':'alineado'})['veredicto'])"
```

Esperado: `232 coherente`.
