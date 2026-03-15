from dataclasses import dataclass
from jugador import Jugador


@dataclass
class Equipo:
    nombre: str
    filas: list[Jugador]
