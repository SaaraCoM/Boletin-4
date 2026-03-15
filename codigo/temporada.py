from dataclasses import dataclass
from equipo import Equipo


@dataclass
class Temporada:
    nombre: str
    anyo_inicio: int
    equipos: list[Equipo]
