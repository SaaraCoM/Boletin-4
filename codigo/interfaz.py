from __future__ import annotations

import os
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox

import customtkinter as ctk

from liga import Liga
from factoria_futbol import FactoriaFutbol

try:
    from PIL import Image, ImageEnhance, ImageTk
except Exception:
    Image = None
    ImageEnhance = None
    ImageTk = None


class AppFutbol(ctk.CTk):

    ENCABEZADOS_RESULTADOS = {
        1: ("Jugador (Equipo - Temporada)", "Partidos / Goles"),
        2: ("Jugador", "Goles totales"),
        3: ("Jugador", "Equipos"),
        4: ("Jugador - Equipo", "Partidos"),
        5: ("Jugador", "Minutos"),
        6: ("Jugador", "Equipos"),
        7: ("Jugador - Equipo", "Temporadas seguidas"),
        8: ("Pareja - Equipo", "Minutos juntos"),
        9: ("Jugador", "Partidos enteros"),
        10: ("Equipo (Temporada)", "Tarjetas"),
        11: ("Revulsivo", "Goles / Min-Gol"),
        12: ("Jugador", "Años en activo"),
        13: ("Jugador", "Partidos impolutos"),
        14: ("Jugador", "Cambios"),
        15: ("Jugador", "Goles / Temporada"),
        16: ("Jugador", "Goles / Min-Gol"),
        17: ("Jugador", "Partidos sin gol"),
        18: ("Jugador", "Décadas con gol"),
        19: ("Temporada", "Descensos"),
        20: ("Equipo", "Descensos"),
        21: ("Temporada", "Ascensos"),
        22: ("Equipo", "Ascensos"),
        23: ("Equipo", "Temporadas"),
        24: ("Equipo", "Temporadas"),
        25: ("Equipo", "Goles"),
        26: ("Equipo", "Goles"),
        27: ("Temporada", "Goles / Partidos / Media"),
        28: ("Temporada", "Equipos máximos"),
        29: ("Equipo", "Racha máximo goleador"),
        30: ("Equipos", "Jugadores compartidos"),
        31: ("Jugador", "Promedio / Total"),
        32: ("Jugador - Equipo", "Años fuera"),
        33: ("Jugador", "Racha consecutiva"),
    }

    def __init__(self, liga_inicial: Liga | None = None, ruta_inicial: str | None = None) -> None:
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")

        self.liga: Liga | None = liga_inicial
        self.ruta_excel_actual = ruta_inicial
        self._worker_activo = False
        self._ultimo_size_fondo: tuple[int, int] = (0, 0)
        self._fondo_original = None
        self._fondo_label: tk.Label | None = None
        self._fondo_photo = None
        self._resize_after_id = None

        self.title("Análisis de Datos de Fútbol")
        self.minsize(900, 600)
        self.geometry("1365x768")
        self.configure(fg_color=Liga.FONDO_PRINCIPAL)

        self._crear_fondo_opcional()
        self.fuentes = self._crear_fuentes()
        self._crear_layout()
        self._rellenar_selector()
        self._actualizar_k_desde_selector()
        self._set_orden(False)

        self.bind("<Configure>", self._al_redimensionar)

        if self.liga is not None:
            self._actualizar_estado_cargado()

    # -----------------------------------------------------------------
    # Fondo y fuentes
    # -----------------------------------------------------------------
    def _ruta_asset(self, nombre: str) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", nombre)

    def _crear_fondo_opcional(self) -> None:
        ruta_imagen = self._ruta_asset("interfaz_referencia.png")
        if Image is None or ImageTk is None or not os.path.isfile(ruta_imagen):
            return

        try:
            imagen = Image.open(ruta_imagen).convert("RGB")
            if ImageEnhance is not None:
                imagen = ImageEnhance.Brightness(imagen).enhance(0.42)
                imagen = ImageEnhance.Contrast(imagen).enhance(1.15)
            self._fondo_original = imagen
            self._fondo_label = tk.Label(self, bd=0, highlightthickness=0)
            self._fondo_label.place(x=0, y=0, relwidth=1, relheight=1)
            self._actualizar_fondo(self.winfo_width() or 1365, self.winfo_height() or 768)
            self._fondo_label.lower()
        except Exception:
            self._fondo_original = None
            self._fondo_label = None

    def _actualizar_fondo(self, ancho: int, alto: int) -> None:
        if self._fondo_original is None or self._fondo_label is None or ImageTk is None:
            return
        ancho = max(900, int(ancho))
        alto = max(600, int(alto))
        if (ancho, alto) == self._ultimo_size_fondo:
            return
        self._ultimo_size_fondo = (ancho, alto)
        try:
            imagen = self._fondo_original.resize((ancho, alto), Image.LANCZOS)
            self._fondo_photo = ImageTk.PhotoImage(imagen)
            self._fondo_label.configure(image=self._fondo_photo)
        except Exception:
            pass

    def _al_redimensionar(self, event) -> None:
        if event.widget is not self:
            return
        if self._resize_after_id is not None:
            try:
                self.after_cancel(self._resize_after_id)
            except Exception:
                pass
        self._resize_after_id = self.after(80, lambda: self._actualizar_fondo(self.winfo_width(), self.winfo_height()))

    def _crear_fuentes(self) -> dict[str, ctk.CTkFont]:
        carpeta_fonts = self._ruta_asset("")
        titulo_fallback = "Consolas"
        texto_fallback = "Segoe UI"
        etiqueta_fallback = "Tahoma"
        if not os.path.isdir(carpeta_fonts):
            titulo_fallback = "Courier New"
            texto_fallback = "DejaVu Sans"
            etiqueta_fallback = "Helvetica"

        return {
            "titulo": ctk.CTkFont(family=titulo_fallback, size=34, weight="bold"),
            "titulo_medio": ctk.CTkFont(family=titulo_fallback, size=22, weight="bold"),
            "subtitulo": ctk.CTkFont(family=titulo_fallback, size=18, weight="bold"),
            "texto": ctk.CTkFont(family=texto_fallback, size=16),
            "texto_bold": ctk.CTkFont(family=texto_fallback, size=16, weight="bold"),
            "texto_tabla": ctk.CTkFont(family=texto_fallback, size=17, weight="bold"),
            "etiqueta": ctk.CTkFont(family=etiqueta_fallback, size=13),
            "k": ctk.CTkFont(family=titulo_fallback, size=30, weight="bold"),
            "numero_fila": ctk.CTkFont(family=titulo_fallback, size=18, weight="bold"),
        }

    # -----------------------------------------------------------------
    # Layout principal
    # -----------------------------------------------------------------
    def _crear_layout(self) -> None:
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self._crear_cabecera()
        self._crear_panel_lateral()
        self._crear_panel_resultados()

        self._mostrar_lineas(["Carga un Excel y ejecuta un ejercicio."])

    def _crear_cabecera(self) -> None:
        self.cabecera = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=18,
            border_width=2,
            border_color="#d9d9d9",
        )
        self.cabecera.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=24, pady=(20, 12))
        self.cabecera.grid_columnconfigure(1, weight=1)

        self.icono_label = ctk.CTkLabel(
            self.cabecera,
            text="⚽",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color=Liga.TEXTO_PRIMARIO,
        )
        self.icono_label.grid(row=0, column=0, rowspan=2, sticky="w", padx=(22, 12), pady=16)

        self.titulo_label = ctk.CTkLabel(
            self.cabecera,
            text="ANÁLISIS DE DATOS DE FÚTBOL",
            font=self.fuentes["titulo"],
            text_color=Liga.TEXTO_PRIMARIO,
        )
        self.titulo_label.grid(row=0, column=1, sticky="w", padx=4, pady=(18, 2))

        self.estado_label = ctk.CTkLabel(
            self.cabecera,
            text="⚠️ No hay Excel cargado.",
            font=self.fuentes["texto"],
            text_color=Liga.TEXTO_SECUNDARIO,
        )
        self.estado_label.grid(row=1, column=1, sticky="w", padx=4, pady=(0, 16))

        self.boton_cargar = ctk.CTkButton(
            self.cabecera,
            text="📄  Cargar Excel",
            command=self._dialogo_cargar_excel,
            font=self.fuentes["texto_bold"],
            fg_color="#e8f5e9",
            hover_color="#dcedc8",
            text_color="#111111",
            border_width=2,
            border_color="#c8e6c9",
            corner_radius=14,
            width=220,
            height=56,
        )
        self.boton_cargar.grid(row=0, column=2, rowspan=2, sticky="e", padx=(12, 20), pady=18)

    def _crear_panel_lateral(self) -> None:
        self.panel_lateral = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=22,
            border_width=2,
            border_color="#d9d9d9",
            width=380,
        )
        self.panel_lateral.grid(row=1, column=0, sticky="nsew", padx=(24, 14), pady=(0, 20))
        self.panel_lateral.grid_propagate(False)
        self.panel_lateral.grid_columnconfigure(0, weight=1)

        self.panel_titulo = ctk.CTkLabel(
            self.panel_lateral,
            text="SELECCIONAR EJERCICIO",
            font=self.fuentes["titulo_medio"],
            text_color=Liga.TEXTO_PRIMARIO,
        )
        self.panel_titulo.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 12))

        self.tarjeta_selector = ctk.CTkFrame(
            self.panel_lateral,
            fg_color="#ffffff",
            corner_radius=16,
            border_width=2,
            border_color="#d9d9d9",
        )
        self.tarjeta_selector.grid(row=1, column=0, sticky="ew", padx=22, pady=(0, 16))
        self.tarjeta_selector.grid_columnconfigure(0, weight=1)

        self.selector_ejercicio = ctk.CTkOptionMenu(
            self.tarjeta_selector,
            values=["Ejercicio 01 - ..."],
            command=lambda _valor: self._al_cambiar_ejercicio(),
            font=self.fuentes["texto_bold"],
            dropdown_font=self.fuentes["texto"],
            fg_color="#f5f5f5",
            button_color="#c8e6c9",
            button_hover_color="#aed581",
            text_color=Liga.TEXTO_PRIMARIO,
            corner_radius=12,
            height=42,
            dynamic_resizing=False,
        )
        self.selector_ejercicio.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))

        self.descripcion_ejercicio_label = ctk.CTkLabel(
            self.tarjeta_selector,
            text="(Partidos y goles)",
            font=self.fuentes["subtitulo"],
            text_color="#2e7d32",
        )
        self.descripcion_ejercicio_label.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        self.k_titulo = ctk.CTkLabel(
            self.panel_lateral,
            text="Seleccionar K :",
            font=self.fuentes["titulo_medio"],
            text_color=Liga.TEXTO_PRIMARIO,
        )
        self.k_titulo.grid(row=2, column=0, sticky="w", padx=22, pady=(2, 8))

        self.k_contenedor = ctk.CTkFrame(self.panel_lateral, fg_color="transparent")
        self.k_contenedor.grid(row=3, column=0, sticky="ew", padx=22, pady=(0, 10))
        self.k_contenedor.grid_columnconfigure(0, weight=1)

        self.slider_k = ctk.CTkSlider(
            self.k_contenedor,
            from_=1,
            to=20,
            number_of_steps=19,
            command=self._al_mover_slider,
            progress_color="#66bb6a",
            button_color="#d9d9d9",
            button_hover_color="#ffffff",
            fg_color="#ffffff",
            height=18,
        )
        self.slider_k.grid(row=0, column=0, sticky="ew", padx=(4, 14), pady=6)
        self.slider_k.set(1)

        self.valor_k_label = ctk.CTkLabel(
            self.k_contenedor,
            text="1",
            width=84,
            height=58,
            corner_radius=12,
            fg_color="#ffffff",
            text_color="#111111",
            font=self.fuentes["k"],
        )
        self.valor_k_label.grid(row=0, column=1, sticky="e", padx=(0, 0))

        self.rango_k_frame = ctk.CTkFrame(self.panel_lateral, fg_color="transparent")
        self.rango_k_frame.grid(row=4, column=0, sticky="ew", padx=22, pady=(0, 12))
        self.rango_k_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            self.rango_k_frame,
            text="1",
            font=self.fuentes["texto_bold"],
            text_color=Liga.TEXTO_PRIMARIO,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            self.rango_k_frame,
            text="20",
            font=self.fuentes["texto_bold"],
            text_color=Liga.TEXTO_PRIMARIO,
        ).grid(row=0, column=2, sticky="e")

        self.orden_titulo = ctk.CTkLabel(
            self.panel_lateral,
            text="Ordenar:",
            font=self.fuentes["titulo_medio"],
            text_color=Liga.TEXTO_PRIMARIO,
        )
        self.orden_titulo.grid(row=5, column=0, sticky="w", padx=22, pady=(0, 10))

        self.orden_ascendente = False

        self.boton_desc = ctk.CTkButton(
            self.panel_lateral,
            text="⬆  Mayor a Menor",
            command=lambda: self._set_orden(False),
            fg_color="#e8f5e9",
            hover_color="#dcedc8",
            text_color="#111111",
            font=self.fuentes["titulo_medio"],
            corner_radius=12,
            border_width=2,
            border_color="#c8e6c9",
            height=60,
        )
        self.boton_desc.grid(row=6, column=0, sticky="ew", padx=22, pady=(0, 10))

        self.boton_asc = ctk.CTkButton(
            self.panel_lateral,
            text="⬇  Menor a Mayor",
            command=lambda: self._set_orden(True),
            fg_color="#f5f5f5",
            hover_color="#eeeeee",
            text_color=Liga.TEXTO_PRIMARIO,
            font=self.fuentes["titulo_medio"],
            corner_radius=12,
            border_width=2,
            border_color="#d9d9d9",
            height=60,
        )
        self.boton_asc.grid(row=7, column=0, sticky="ew", padx=22, pady=(0, 18))

        self.boton_ejecutar = ctk.CTkButton(
            self.panel_lateral,
            text="▶  Ejecutar Ejercicio",
            command=self._ejecutar_actual,
            fg_color="#e8f5e9",
            hover_color="#dcedc8",
            text_color="#111111",
            font=self.fuentes["titulo_medio"],
            corner_radius=14,
            border_width=2,
            border_color="#c8e6c9",
            height=72,
        )
        self.boton_ejecutar.grid(row=8, column=0, sticky="ew", padx=22, pady=(6, 18))

        self.texto_progreso = ctk.CTkLabel(
            self.panel_lateral,
            text="",
            font=self.fuentes["texto"],
            text_color=Liga.TEXTO_SECUNDARIO,
        )
        self.texto_progreso.grid(row=9, column=0, sticky="w", padx=22, pady=(0, 6))

        self.progressbar = ctk.CTkProgressBar(
            self.panel_lateral,
            mode="indeterminate",
            progress_color="#66bb6a",
            fg_color="#ffffff",
        )
        self.progressbar.grid(row=10, column=0, sticky="ew", padx=22, pady=(0, 18))
        self.progressbar.grid_remove()

        self.nota_inferior = ctk.CTkLabel(
            self.panel_lateral,
            text="⚽ Históricos de Primera División · Offline",
            font=self.fuentes["etiqueta"],
            text_color=Liga.TEXTO_SECUNDARIO,
        )
        self.nota_inferior.grid(row=11, column=0, sticky="sw", padx=22, pady=(8, 18))

    def _crear_panel_resultados(self) -> None:
        self.panel_resultados = ctk.CTkFrame(
            self,
            fg_color="#ffffff",
            corner_radius=22,
            border_width=2,
            border_color="#d9d9d9",
        )
        self.panel_resultados.grid(row=1, column=1, sticky="nsew", padx=(0, 24), pady=(0, 20))
        self.panel_resultados.grid_columnconfigure(0, weight=1)
        self.panel_resultados.grid_rowconfigure(2, weight=1)

        self.resultados_titulo = ctk.CTkLabel(
            self.panel_resultados,
            text="Resultados",
            font=self.fuentes["titulo"],
            text_color=Liga.TEXTO_PRIMARIO,
        )
        self.resultados_titulo.grid(row=0, column=0, sticky="n", pady=(18, 6))

        self.estado_resultados = ctk.CTkLabel(
            self.panel_resultados,
            text="Selecciona un ejercicio y ejecútalo.",
            font=self.fuentes["texto"],
            text_color=Liga.TEXTO_SECUNDARIO,
        )
        self.estado_resultados.grid(row=1, column=0, sticky="ew", padx=18, pady=(0, 8))

        self.tabla_frame = ctk.CTkFrame(
            self.panel_resultados,
            fg_color="#ffffff",
            corner_radius=16,
            border_width=2,
            border_color="#d9d9d9",
        )
        self.tabla_frame.grid(row=2, column=0, sticky="nsew", padx=18, pady=(0, 14))
        self.tabla_frame.grid_columnconfigure(0, weight=1)
        self.tabla_frame.grid_rowconfigure(1, weight=1)

        self.tabla_header = ctk.CTkFrame(
            self.tabla_frame,
            fg_color="#e8f5e9",
            corner_radius=12,
        )
        self.tabla_header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 8))
        self.tabla_header.grid_columnconfigure(1, weight=1)

        self.header_pos = ctk.CTkLabel(
            self.tabla_header,
            text="#",
            width=48,
            font=self.fuentes["subtitulo"],
            text_color="#111111",
        )
        self.header_pos.grid(row=0, column=0, padx=(10, 6), pady=10)

        self.header_desc = ctk.CTkLabel(
            self.tabla_header,
            text="Resultado",
            anchor="w",
            font=self.fuentes["subtitulo"],
            text_color="#111111",
        )
        self.header_desc.grid(row=0, column=1, sticky="ew", padx=6, pady=10)

        self.header_vals = ctk.CTkLabel(
            self.tabla_header,
            text="Valores",
            width=220,
            font=self.fuentes["subtitulo"],
            text_color="#111111",
        )
        self.header_vals.grid(row=0, column=2, padx=(6, 16), pady=10)

        self.scroll_resultados = ctk.CTkScrollableFrame(
            self.tabla_frame,
            fg_color="#ffffff",
            corner_radius=12,
        )
        self.scroll_resultados.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.scroll_resultados.grid_columnconfigure(1, weight=1)

        self.boton_guardar = ctk.CTkButton(
            self.panel_resultados,
            text="⬇  Guardar Resultados",
            command=self._guardar_resultados,
            fg_color="#e8f5e9",
            hover_color="#dcedc8",
            text_color="#111111",
            font=self.fuentes["titulo_medio"],
            corner_radius=14,
            border_width=2,
            border_color="#c8e6c9",
            height=60,
            width=360,
        )
        self.boton_guardar.grid(row=3, column=0, pady=(0, 18))

    # -----------------------------------------------------------------
    # Selector y estado
    # -----------------------------------------------------------------
    def _rellenar_selector(self) -> None:
        opciones = [
            f"Ejercicio {numero:02d} - {Liga.descripcion_ejercicio(numero)}"
            for numero in range(1, 34)
        ]
        self.selector_ejercicio.configure(values=opciones)
        self.selector_ejercicio.set(opciones[0])
        self._actualizar_texto_ejercicio()

    def _numero_ejercicio_actual(self) -> int:
        coincidencia = re.search(r"Ejercicio\s+(\d+)", self.selector_ejercicio.get())
        if coincidencia is None:
            return 1
        return int(coincidencia.group(1))

    def _actualizar_texto_ejercicio(self) -> None:
        numero = self._numero_ejercicio_actual()
        descripcion = Liga.descripcion_ejercicio(numero)
        self.descripcion_ejercicio_label.configure(text=f"({descripcion})")

    def _al_mover_slider(self, valor: float) -> None:
        entero = int(round(float(valor)))
        self.valor_k_label.configure(text=str(entero))

    def _set_orden(self, ascendente: bool) -> None:
        self.orden_ascendente = bool(ascendente)
        if self.orden_ascendente:
            self.boton_asc.configure(
                fg_color="#e8f5e9",
                hover_color="#dcedc8",
                text_color="#111111",
                border_color="#c8e6c9",
            )
            self.boton_desc.configure(
                fg_color="#f5f5f5",
                hover_color="#eeeeee",
                text_color=Liga.TEXTO_PRIMARIO,
                border_color="#d9d9d9",
            )
        else:
            self.boton_desc.configure(
                fg_color="#e8f5e9",
                hover_color="#dcedc8",
                text_color="#111111",
                border_color="#c8e6c9",
            )
            self.boton_asc.configure(
                fg_color="#f5f5f5",
                hover_color="#eeeeee",
                text_color=Liga.TEXTO_PRIMARIO,
                border_color="#d9d9d9",
            )

    def _al_cambiar_ejercicio(self) -> None:
        self._actualizar_texto_ejercicio()
        self._actualizar_k_desde_selector()
        if self.liga is None:
            self.estado_resultados.configure(text="Selecciona un ejercicio y ejecútalo.")
            return
        numero = self._numero_ejercicio_actual()
        k = int(round(self.slider_k.get()))
        clave = (numero, k, self.orden_ascendente)
        if clave in self.liga._cache_resultados:
            self._mostrar_lineas(self.liga._cache_resultados[clave])

    def _actualizar_k_desde_selector(self) -> None:
        numero = self._numero_ejercicio_actual()
        k = Liga.get_default_k(numero)
        k = max(1, min(20, k))
        self.slider_k.set(k)
        self.valor_k_label.configure(text=str(k))

    def _actualizar_estado_cargado(self) -> None:
        if self.liga is None:
            self.estado_label.configure(text="⚠️ No hay Excel cargado.", text_color=Liga.TEXTO_SECUNDARIO)
            return
        numero_filas = len(self.liga._filas)
        numero_temporadas = len(self.liga.temporadas_ordenadas)
        numero_equipos = len(self.liga._por_equipo)
        mensaje = f"✅ Cargado: {numero_filas} filas · {numero_temporadas} temporadas · {numero_equipos} equipos"
        self.estado_label.configure(text=mensaje, text_color=Liga.ACENTO_VERDE)
        self.estado_resultados.configure(text=mensaje, text_color=Liga.TEXTO_PRIMARIO)

    # -----------------------------------------------------------------
    # Carga del Excel
    # -----------------------------------------------------------------
    def _dialogo_cargar_excel(self) -> None:
        if self._worker_activo:
            messagebox.showwarning("Carga en curso", "Ya hay una carga en curso.")
            return
        ruta = filedialog.askopenfilename(
            title="Selecciona el Excel",
            filetypes=[("Excel", "*.xls *.xlsx"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return
        self._iniciar_carga(ruta)

    def _iniciar_carga(self, ruta: str) -> None:
        self._worker_activo = True
        self.ruta_excel_actual = ruta
        self.texto_progreso.configure(text="Cargando...")
        self.progressbar.grid()
        self.progressbar.start()
        self.boton_cargar.configure(state="disabled")
        hilo = threading.Thread(target=self._worker_cargar_excel, args=(ruta,), daemon=True)
        hilo.start()

    def _worker_cargar_excel(self, ruta: str) -> None:
        try:
            liga = FactoriaFutbol.cargar_excel(ruta)
            self.after(0, lambda: self._fin_carga_correcta(liga, ruta))
        except Exception as error:
            self.after(0, lambda: self._fin_carga_error(error))

    def _fin_carga_correcta(self, liga: Liga, ruta: str) -> None:
        self.liga = liga
        self.ruta_excel_actual = ruta
        self._worker_activo = False
        self.progressbar.stop()
        self.progressbar.grid_remove()
        self.texto_progreso.configure(text="")
        self.boton_cargar.configure(state="normal")
        self._actualizar_estado_cargado()
        messagebox.showinfo("Carga completada", self.estado_label.cget("text"))
        self._ejecutar_actual(mostrar_errores=False)

    def _fin_carga_error(self, error: Exception) -> None:
        self._worker_activo = False
        self.progressbar.stop()
        self.progressbar.grid_remove()
        self.texto_progreso.configure(text="")
        self.boton_cargar.configure(state="normal")
        messagebox.showerror("Error al cargar", str(error))

    # -----------------------------------------------------------------
    # Render de resultados
    # -----------------------------------------------------------------
    def _extraer_datos_visuales(self, linea: str) -> tuple[str, list[str]]:
        limpia = linea.strip()
        if limpia.startswith("- "):
            limpia = limpia[2:].strip()

        if "|" in limpia:
            partes = [parte.strip() for parte in limpia.split("|") if parte.strip()]
            descripcion = partes[0]
            datos: list[str] = []
            for parte in partes[1:]:
                if ":" in parte:
                    _, valor = parte.split(":", 1)
                    datos.append(valor.strip())
                else:
                    datos.append(parte.strip())
            return descripcion, datos

        if ": " in limpia:
            izquierda, derecha = limpia.split(": ", 1)
            datos_numericos = re.findall(r"\d+(?:[.,]\d+)?", derecha)
            if datos_numericos:
                return izquierda.strip(), datos_numericos

        datos_linea = re.findall(r"\d+(?:[.,]\d+)?", limpia)
        if datos_linea:
            return limpia, datos_linea[:3]
        return limpia, []

    def _configurar_header_tabla(self, numero_ejercicio: int) -> None:
        descripcion = Liga.descripcion_ejercicio(numero_ejercicio)
        encabezado_izq, encabezado_der = self.ENCABEZADOS_RESULTADOS.get(
            numero_ejercicio,
            ("Resultado", "Valores"),
        )
        self.resultados_titulo.configure(text=f"Resultados · Ejercicio {numero_ejercicio:02d}")
        self.header_desc.configure(text=encabezado_izq)
        self.header_vals.configure(text=encabezado_der)
        self.estado_resultados.configure(
            text=f"Ejercicio {numero_ejercicio:02d} · {descripcion}",
            text_color=Liga.TEXTO_SECUNDARIO,
        )

    def _mostrar_lineas(self, lineas: list[str]) -> None:
        for widget in self.scroll_resultados.winfo_children():
            widget.destroy()

        if not lineas:
            lineas = ["No hay resultados para mostrar."]

        numero_ejercicio = self._numero_ejercicio_actual()
        self._configurar_header_tabla(numero_ejercicio)

        for indice, linea in enumerate(lineas, start=1):
            fila = ctk.CTkFrame(
                self.scroll_resultados,
                fg_color="#ffffff" if indice % 2 else "#fafafa",
                corner_radius=10,
                border_width=1,
                border_color="#e0e0e0",
            )
            fila.grid(row=indice - 1, column=0, sticky="ew", padx=8, pady=4)
            fila.grid_columnconfigure(1, weight=1)

            posicion = ctk.CTkLabel(
                fila,
                text=f"{indice}.",
                width=54,
                font=self.fuentes["numero_fila"],
                text_color=Liga.TEXTO_PRIMARIO,
            )
            posicion.grid(row=0, column=0, padx=(12, 8), pady=10)

            descripcion, datos = self._extraer_datos_visuales(linea)

            desc_label = ctk.CTkLabel(
                fila,
                text=descripcion,
                font=self.fuentes["texto_tabla"],
                text_color=Liga.TEXTO_PRIMARIO,
                justify="left",
                anchor="w",
                wraplength=700,
            )
            desc_label.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=10)

            datos_frame = ctk.CTkFrame(fila, fg_color="transparent")
            datos_frame.grid(row=0, column=2, sticky="e", padx=(0, 12), pady=10)

            if not datos:
                datos = ["—"]

            for columna, dato in enumerate(datos[:3]):
                badge = ctk.CTkLabel(
                    datos_frame,
                    text=dato,
                    font=self.fuentes["texto_tabla"],
                    text_color=Liga.ACENTO_DORADO if re.search(r"\d", dato) else Liga.TEXTO_PRIMARIO,
                    fg_color="#ffffff",
                    corner_radius=10,
                    padx=14,
                    pady=8,
                )
                badge.grid(row=0, column=columna, padx=4)

    # -----------------------------------------------------------------
    # Ejecución y guardado
    # -----------------------------------------------------------------
    def _ejecutar_actual(self, mostrar_errores: bool = True) -> None:
        if self.liga is None:
            if mostrar_errores:
                messagebox.showwarning("Sin datos", "Primero debes cargar un Excel.")
            return
        try:
            numero = self._numero_ejercicio_actual()
            k = int(round(self.slider_k.get()))
            metodo = getattr(self.liga, f"ejercicio_{numero:02d}")
            resultados = metodo(k, self.orden_ascendente)
            self._mostrar_lineas(resultados)
            sentido = "Menor a Mayor" if self.orden_ascendente else "Mayor a Menor"
            descripcion = Liga.descripcion_ejercicio(numero)
            self.estado_resultados.configure(
                text=f"Ejercicio {numero:02d} · {descripcion} · K={k} · Orden: {sentido}",
                text_color=Liga.TEXTO_PRIMARIO,
            )
        except Exception as error:
            if mostrar_errores:
                messagebox.showerror("Error al ejecutar", str(error))

    def _guardar_resultados(self) -> None:
        if self.liga is None:
            messagebox.showwarning("Sin resultados", "Carga el Excel y ejecuta al menos un ejercicio antes de guardar.")
            return
        if not self.liga._cache_resultados:
            messagebox.showwarning("Sin resultados", "No hay ejercicios ejecutados para exportar.")
            return

        confirmar = messagebox.askyesno(
            "Confirmación",
            "Esto escribirá un archivo .txt con los ejercicios ya ejecutados. ¿Quieres continuar?",
        )
        if not confirmar:
            return

        ruta = filedialog.asksaveasfilename(
            title="Guardar resultados",
            defaultextension=".txt",
            filetypes=[("Texto", "*.txt"), ("Todos los archivos", "*.*")],
        )
        if not ruta:
            return

        try:
            bloques: list[str] = []
            for numero, k, ascendente in sorted(self.liga._cache_resultados.keys()):
                bloques.append(f"═══ EJERCICIO {numero:02d} ═══")
                bloques.extend(self.liga._cache_resultados[(numero, k, ascendente)])
                bloques.append("")
            with open(ruta, "w", encoding="utf-8") as fichero:
                fichero.write("\n".join(bloques).rstrip() + "\n")
            messagebox.showinfo("Guardado", f"✅ Resultados guardados en:\n{ruta}")
        except Exception as error:
            messagebox.showerror("Error al guardar", str(error))
