"""Motor de Inercia de Éxito T16D-S.

Puerto fiel del clasificador en
https://opal-fern-ocean-field.grok.me
(256 nodos, 342 aristas, ⟨R,G,S⟩ ≅ SmallGroup(16,11)).

No es oráculo. Lee una firma sobre {0,1}⁸, aterriza en una órbita
y comprueba si las dos piernas se conjugan por S.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

_DIR = Path(__file__).resolve().parent
