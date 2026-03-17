from dataclasses import dataclass


@dataclass
class Jugador:
    jugador_id: str
    nombre: str
    equipo: str
    temporada: str
    anyo_inicio: int
    pjugados: int
    pcompletos: int
    ptitular: int
    psuplente: int
    minutos: int
    lesiones: int
    tarjetas: int
    expulsiones: int
    goles: int
    pen_fallados: int

    @property
    def tarjetas_totales(self) -> int:
        return self.tarjetas + self.expulsiones

    @property
    def veces_sustituido(self) -> int:
        return max(self.pjugados - self.pcompletos, 0)

    @property
    def goles_por_minuto(self) -> float:
        if self.minutos <= 0:
            return 0.0
        return self.goles / self.minutos

    @property
    def es_revulsivo(self) -> bool:
        return self.psuplente > self.ptitular
