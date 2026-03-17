README_TXT

1. ESTRUCTURA GENERAL

EJERCICIO_4/
├── codigo/
│   ├── jugador.py
│   ├── equipo.py
│   ├── temporada.py
│   ├── factoria_futbol.py
│   ├── liga.py
│   ├── interfaz.py
│   └── ejecucion.py
└── data/
    └── Plantillas1D-2017-18.xls

2. ARCHIVO: jugador.py
   Clase: Jugador
   - Qué hace:
     Representa una fila ya limpia del Excel para un jugador concreto en un equipo y temporada.
   - Cómo funciona:
     Guarda todos los atributos numéricos y textuales necesarios para los 33 ejercicios.
   - Ejemplo:
     Jugador("MESSI#1", "MESSI", "F.C. Barcelona", "2011-12", 2011, 37, 37, 37, 0, 3240, 0, 3, 0, 50, 0)

3. ARCHIVO: equipo.py
   Clase: Equipo
   - Qué hace:
     Agrupa las filas Jugador que pertenecen al mismo equipo.
   - Cómo funciona:
     Guarda el nombre del equipo y la lista de jugadores/fichas de ese equipo.
   - Ejemplo:
     Equipo("Real Madrid C.F.", lista_de_filas)

4. ARCHIVO: temporada.py
   Clase: Temporada
   - Qué hace:
     Representa una temporada histórica del dataset.
   - Cómo funciona:
     Guarda el nombre, el año inicial y los equipos que aparecen en esa temporada.
   - Ejemplo:
     Temporada("2011-12", 2011, lista_de_equipos)

5. ARCHIVO: liga.py
   Clase: Liga
   - Qué hace:
     Representa la raíz del modelo (Liga -> Temporadas -> Equipos -> Jugadores) e integra los ejercicios 01..33.
   - Cómo funciona:
     Recorre la jerarquía con `_iterar_historial`, construye índices internos y expone métodos de estadísticas históricas.
   - Funciones principales:
     - agregar_temporada
     - _iterar_historial
     - get_default_k / descripcion_ejercicio
     - ejercicio_01 ... ejercicio_33
   - Ejemplo:
     liga = Factoria.cargar_excel(ruta_excel)
     top = liga.ejercicio_02(1, False)

6. ARCHIVO: factoria_futbol.py
   Clase: FactoriaFutbol
   - Qué hace:
     Carga el Excel, limpia los datos y construye el objeto Liga.
   - Cómo funciona:
     1) localiza el archivo;
     2) abre .xls con xlrd o, si no está disponible, convierte offline a .xlsx;
     3) valida columnas;
     4) elimina filas con TONTO;
     5) corrige PCOMPLETOS;
     6) extrae anyo_inicio;
     7) desambigua homónimos;
     8) crea Jugador, Equipo y Temporada.
   - Funciones principales:
     - resolver_ruta_excel
     - _leer_excel
     - _limpiar_filas
     - _asignar_jugador_id
     - _crear_objetos
     - cargar_excel
   - Ejemplo:
     liga = FactoriaFutbol.cargar_excel("../data/Plantillas1D-2017-18.xls")

7. ARCHIVO: interfaz.py
   Clase: AppFutbol
   - Qué hace:
     Construye la interfaz gráfica offline con customtkinter.
   - Cómo funciona:
     Tiene cabecera, carga de Excel, panel lateral de control, panel principal con resultados, caché y exportación a TXT.
   - Funciones principales:
     - __init__
     - _crear_fuentes
     - _crear_layout
     - _rellenar_selector
     - _actualizar_k_desde_selector
     - cargar_excel
     - _cargar_excel_worker
     - ejecutar_ejercicio
     - guardar_resultados
   - Ejemplo:
     app = AppFutbol(liga_inicial=liga, ruta_inicial=ruta_excel)
     app.mainloop()

8. ARCHIVO: ejecucion.py
   - Qué hace:
     Ejecuta tests internos obligatorios y, si pasan, arranca la interfaz.
   - Cómo funciona:
     Carga el Excel desde la carpeta data, ejecuta los 33 ejercicios con K por defecto y valida referencias canónicas mínimas.
   - Funciones:
     - ejecutar_tests
   - Ejemplo:
     python ejecucion.py

9. DEPENDENCIAS
   - Python 3.10+
   - customtkinter
   - openpyxl
   - xlrd
   - pillow

10. EJECUCIÓN
   - Desde la carpeta codigo:
     python ejecucion.py

11. NOTA DE INTERFAZ
   - La interfaz sigue el layout del boletín y la estética solicitada.
   - Si faltan fuentes locales en ./fonts, usa fuentes de respaldo del sistema.


12. ACTUALIZACIÓN BOLETÍN 5
   - Se incorpora la clase Liga (archivo: liga.py) con estructura jerárquica Liga -> Temporadas -> Equipos -> Jugadores.
   - Jugador añade propiedades derivadas: tarjetas_totales, veces_sustituido, goles_por_minuto, es_revulsivo.
   - Equipo añade agregar_jugador y propiedades derivadas del equipo.
   - Temporada pasa a almacenar equipos en diccionario y añade agregar_equipo y propiedades derivadas.
   - Factoria (en factoria_futbol.py) valida datos y devuelve un objeto Liga.
   - Se añade el generador _iterar_historial en Liga y wrappers de ejercicios para mantener compatibilidad con la lógica histórica.
