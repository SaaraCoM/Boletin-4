from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from openpyxl import load_workbook

from equipo import Equipo
from experto_futbol import ExpertoFutbol
from jugador import Jugador
from temporada import Temporada

try:
    import xlrd  # type: ignore
except Exception:
    xlrd = None


class FactoriaFutbol:
    COLUMNAS_ESPERADAS = [
        "TEMPORADA", "LIGA", "EQUIPO", "JUGADOR", "PJUGADOS", "PCOMPLETOS",
        "PTITULAR", "PSUPLENTE", "MINUTOS", "LESIONES", "TARJETAS",
        "EXPULSIONES", "GOLES", "PENALTIES FALLADOS",
    ]

    @staticmethod
    def resolver_ruta_excel(ruta: str) -> str:
        candidatos: list[str] = []
        if os.path.isabs(ruta):
            candidatos.append(ruta)
        else:
            base = os.path.dirname(os.path.abspath(__file__))
            candidatos.extend([
                ruta,
                os.path.join(base, ruta),
                os.path.join(base, "..", "data", ruta),
                os.path.join(os.getcwd(), ruta),
                os.path.join(os.getcwd(), "data", ruta),
                os.path.join(os.getcwd(), "EJERCICIO_4", "data", ruta),
            ])

        for candidato in candidatos:
            ruta_normalizada = os.path.abspath(candidato)
            if os.path.exists(ruta_normalizada):
                return ruta_normalizada
        return os.path.abspath(ruta)

    @staticmethod
    def _normalizar_texto(valor) -> str:
        if valor is None:
            return ""
        return str(valor).strip()

    @staticmethod
    def _a_entero(valor) -> int:
        if valor is None:
            return 0
        if isinstance(valor, bool):
            return int(valor)
        if isinstance(valor, int):
            return valor
        if isinstance(valor, float):
            return int(valor)
        texto = str(valor).strip()
        if texto == "":
            return 0
        texto = texto.replace(",", ".")
        try:
            return int(float(texto))
        except Exception:
            return 0

    @staticmethod
    def _extraer_anyo_inicio(temporada: str) -> int:
        encontrado = re.search(r"(\d{4})", temporada)
        if not encontrado:
            raise ValueError(f"No se pudo extraer el año inicial de la temporada: {temporada}")
        return int(encontrado.group(1))

    @staticmethod
    def _leer_xlsx(ruta: str) -> list[dict[str, object]]:
        libro = load_workbook(filename=ruta, data_only=True, read_only=True)
        hoja = libro.active
        filas_iter = hoja.iter_rows(values_only=True)
        try:
            cabecera = next(filas_iter)
        except StopIteration:
            return []

        columnas = [FactoriaFutbol._normalizar_texto(valor) for valor in cabecera]
        filas: list[dict[str, object]] = []

        for fila in filas_iter:
            if fila is None:
                continue
            registro: dict[str, object] = {}
            vacia = True
            for indice, columna in enumerate(columnas):
                valor = fila[indice] if indice < len(fila) else None
                registro[columna] = valor
                if valor not in (None, ""):
                    vacia = False
            if not vacia:
                filas.append(registro)

        libro.close()
        return filas

    @staticmethod
    def _leer_xls_con_xlrd(ruta: str) -> list[dict[str, object]]:
        if xlrd is None:
            raise ImportError("xlrd no está disponible")
        libro = xlrd.open_workbook(ruta)
        hoja = libro.sheet_by_index(0)
        columnas = [FactoriaFutbol._normalizar_texto(hoja.cell_value(0, c)) for c in range(hoja.ncols)]
        filas: list[dict[str, object]] = []

        for fila_idx in range(1, hoja.nrows):
            registro: dict[str, object] = {}
            vacia = True
            for col_idx, columna in enumerate(columnas):
                valor = hoja.cell_value(fila_idx, col_idx)
                if valor != "":
                    vacia = False
                registro[columna] = valor
            if not vacia:
                filas.append(registro)

        return filas

    @staticmethod
    def _convertir_xls_a_xlsx_temporal(ruta: str) -> str:
        ejecutable = shutil.which("soffice") or shutil.which("libreoffice")
        if ejecutable is None:
            raise ImportError(
                "No se puede abrir .xls porque falta xlrd y no hay conversor local disponible. "
                "Instala xlrd o usa un archivo .xlsx."
            )

        carpeta_temporal = tempfile.mkdtemp(prefix="boletin4_xls_")
        comando = [
            ejecutable,
            "--headless",
            "--convert-to",
            "xlsx",
            "--outdir",
            carpeta_temporal,
            ruta,
        ]
        resultado = subprocess.run(comando, capture_output=True, text=True)
        if resultado.returncode != 0:
            raise RuntimeError(
                "No se pudo convertir el archivo .xls a .xlsx. "
                f"Salida: {resultado.stdout} {resultado.stderr}"
            )

        nombre_salida = Path(ruta).with_suffix(".xlsx").name
        ruta_convertida = os.path.join(carpeta_temporal, nombre_salida)
        if not os.path.exists(ruta_convertida):
            raise FileNotFoundError("La conversión a .xlsx terminó sin generar el archivo esperado.")
        return ruta_convertida

    @staticmethod
    def _leer_excel(ruta: str) -> list[dict[str, object]]:
        extension = os.path.splitext(ruta)[1].lower()
        if extension == ".xlsx":
            return FactoriaFutbol._leer_xlsx(ruta)
        if extension == ".xls":
            if xlrd is not None:
                return FactoriaFutbol._leer_xls_con_xlrd(ruta)
            ruta_convertida = FactoriaFutbol._convertir_xls_a_xlsx_temporal(ruta)
            return FactoriaFutbol._leer_xlsx(ruta_convertida)
        raise ValueError(f"Formato no soportado: {ruta}")

    @staticmethod
    def _validar_columnas(filas_crudas: list[dict[str, object]]) -> None:
        if not filas_crudas:
            raise ValueError("El Excel no contiene datos.")
        columnas_presentes = set(filas_crudas[0].keys())
        for columna in FactoriaFutbol.COLUMNAS_ESPERADAS:
            if columna not in columnas_presentes:
                raise ValueError(f"Falta la columna obligatoria: {columna}")

    @staticmethod
    def _limpiar_filas(filas_crudas: list[dict[str, object]]) -> list[dict[str, object]]:
        filas_limpias: list[dict[str, object]] = []

        for registro in filas_crudas:
            nombre = FactoriaFutbol._normalizar_texto(registro.get("JUGADOR"))
            if "TONTO" in nombre.upper():
                continue

            temporada = FactoriaFutbol._normalizar_texto(registro.get("TEMPORADA"))
            fila = {
                "TEMPORADA": temporada,
                "LIGA": FactoriaFutbol._normalizar_texto(registro.get("LIGA")),
                "EQUIPO": FactoriaFutbol._normalizar_texto(registro.get("EQUIPO")),
                "JUGADOR": nombre,
                "PJUGADOS": FactoriaFutbol._a_entero(registro.get("PJUGADOS")),
                "PCOMPLETOS": FactoriaFutbol._a_entero(registro.get("PCOMPLETOS")),
                "PTITULAR": FactoriaFutbol._a_entero(registro.get("PTITULAR")),
                "PSUPLENTE": FactoriaFutbol._a_entero(registro.get("PSUPLENTE")),
                "MINUTOS": FactoriaFutbol._a_entero(registro.get("MINUTOS")),
                "LESIONES": FactoriaFutbol._a_entero(registro.get("LESIONES")),
                "TARJETAS": FactoriaFutbol._a_entero(registro.get("TARJETAS")),
                "EXPULSIONES": FactoriaFutbol._a_entero(registro.get("EXPULSIONES")),
                "GOLES": FactoriaFutbol._a_entero(registro.get("GOLES")),
                "PENALTIES FALLADOS": FactoriaFutbol._a_entero(registro.get("PENALTIES FALLADOS")),
            }
            if fila["PCOMPLETOS"] > fila["PJUGADOS"]:
                fila["PCOMPLETOS"] = fila["PJUGADOS"]
            fila["anyo_inicio"] = FactoriaFutbol._extraer_anyo_inicio(temporada)
            filas_limpias.append(fila)

        filas_limpias.sort(key=lambda fila: (fila["anyo_inicio"], fila["TEMPORADA"], fila["EQUIPO"], fila["JUGADOR"]))
        return filas_limpias

    @staticmethod
    def _asignar_jugador_id(filas_limpias: list[dict[str, object]]) -> None:
        agrupadas: dict[str, list[dict[str, object]]] = {}
        for fila in filas_limpias:
            nombre = str(fila["JUGADOR"])
            if nombre not in agrupadas:
                agrupadas[nombre] = []
            agrupadas[nombre].append(fila)

        for nombre, grupo in agrupadas.items():
            grupo.sort(key=lambda fila: (fila["anyo_inicio"], fila["EQUIPO"], fila["TEMPORADA"]))
            cluster = 1
            fila_previa: dict[str, object] | None = None

            for fila in grupo:
                if fila_previa is not None:
                    gap = int(fila["anyo_inicio"]) - int(fila_previa["anyo_inicio"])
                    cambia_cluster_por_gap = gap > 5
                    cambia_cluster_por_misma_temporada = (
                        fila["TEMPORADA"] == fila_previa["TEMPORADA"] and fila["EQUIPO"] != fila_previa["EQUIPO"]
                    )
                    if cambia_cluster_por_gap or cambia_cluster_por_misma_temporada:
                        cluster += 1

                fila["jugador_id"] = f"{nombre}#{cluster}"
                fila_previa = fila

    @staticmethod
    def _crear_objetos(filas_limpias: list[dict[str, object]]) -> tuple[list[Temporada], list[Jugador]]:
        filas_objeto: list[Jugador] = []
        for fila in filas_limpias:
            filas_objeto.append(
                Jugador(
                    jugador_id=str(fila["jugador_id"]),
                    nombre=str(fila["JUGADOR"]),
                    equipo=str(fila["EQUIPO"]),
                    temporada=str(fila["TEMPORADA"]),
                    anyo_inicio=int(fila["anyo_inicio"]),
                    pjugados=int(fila["PJUGADOS"]),
                    pcompletos=int(fila["PCOMPLETOS"]),
                    ptitular=int(fila["PTITULAR"]),
                    psuplente=int(fila["PSUPLENTE"]),
                    minutos=int(fila["MINUTOS"]),
                    lesiones=int(fila["LESIONES"]),
                    tarjetas=int(fila["TARJETAS"]),
                    expulsiones=int(fila["EXPULSIONES"]),
                    goles=int(fila["GOLES"]),
                    pen_fallados=int(fila["PENALTIES FALLADOS"]),
                )
            )

        temporadas: list[Temporada] = []
        vistas: list[tuple[str, int]] = []
        for fila in filas_objeto:
            par = (fila.temporada, fila.anyo_inicio)
            if par not in vistas:
                vistas.append(par)

        vistas.sort(key=lambda par: (par[1], par[0]))

        for nombre_temporada, anyo_inicio in vistas:
            filas_temporada = [fila for fila in filas_objeto if fila.temporada == nombre_temporada]
            nombres_equipos: list[str] = []
            for fila in filas_temporada:
                if fila.equipo not in nombres_equipos:
                    nombres_equipos.append(fila.equipo)
            nombres_equipos.sort()

            equipos: list[Equipo] = []
            for nombre_equipo in nombres_equipos:
                filas_equipo = [fila for fila in filas_temporada if fila.equipo == nombre_equipo]
                equipos.append(Equipo(nombre=nombre_equipo, filas=filas_equipo))

            temporadas.append(Temporada(nombre=nombre_temporada, anyo_inicio=anyo_inicio, equipos=equipos))

        temporadas.sort(key=lambda temporada: (temporada.anyo_inicio, temporada.nombre))
        return temporadas, filas_objeto

    @staticmethod
    def cargar_excel(ruta: str) -> ExpertoFutbol:
        ruta_resuelta = FactoriaFutbol.resolver_ruta_excel(ruta)
        if not os.path.exists(ruta_resuelta):
            raise FileNotFoundError(f"No se encontró el Excel: {ruta_resuelta}")

        filas_crudas = FactoriaFutbol._leer_excel(ruta_resuelta)
        FactoriaFutbol._validar_columnas(filas_crudas)
        filas_limpias = FactoriaFutbol._limpiar_filas(filas_crudas)
        FactoriaFutbol._asignar_jugador_id(filas_limpias)
        temporadas, filas_objeto = FactoriaFutbol._crear_objetos(filas_limpias)
        return ExpertoFutbol(temporadas=temporadas, filas=filas_objeto)
