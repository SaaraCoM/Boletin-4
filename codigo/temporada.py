from __future__ import annotations

from dataclasses import dataclass, field

from equipo import Equipo


@dataclass
class Temporada:
    identificador: str
    equipos: dict[str, Equipo] = field(default_factory=dict)

    def agregar_equipo(self, equipo: Equipo) -> None:
        self.equipos[equipo.nombre] = equipo

    @property
    def nombre(self) -> str:
        return self.identificador

    @property
    def anyo_inicio(self) -> int:
        return self.año_inicio

    @property
    def año_inicio(self) -> int:
        return int(self.identificador.split("-", 1)[0])

    @property
    def num_equipos(self) -> int:
        return len(self.equipos)

    @property
    def num_partidos(self) -> int:
        if self.num_equipos < 2:
            return 0
        return self.num_equipos * (self.num_equipos - 1)

    @property
    def goles_totales(self) -> int:
        return sum(equipo.goles_marcados for equipo in self.equipos.values())

    @property
    def media_goles_por_partido(self) -> float:
        if self.num_partidos == 0:
            return 0.0
        return self.goles_totales / self.num_partidos
