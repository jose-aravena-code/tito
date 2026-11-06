# Marco Polo: proyecto de5segundos para Claude y Codex

Contenido de esta carpeta:

- `narracion.txt`: guion hablado,10palabras.
- `GUION_Y_ESCENAS.md`: plan de5s,hechos y límites.
- `proyecto.json`: resolución,tiempos,estilo yfuente.
- `animar.py` y `dibujo_base.py`: animación2Dreproducible, basada en el flujoPillow/FFmpegde`tito`.
- `generar_voz.py`: adaptador de la vozSupertonic3M1 que ya usamos; no llamaAPI ni descarga modelos.
- `recursos/`: tipografías conlicencia ycartografíaNaturalEarth(dominio público).
- `salida/marco_polo_5s_con_M1.mp4`: prueba de5s convoz,sinmúsica/efectos.
- `salida/marco_polo_5s_sin_audio.mp4`: misma imagen muda.
- `salida/voz_m1_5s.wav`: voz lista para usar sin descargarTTS.
- `salida/validacion.json`: resultados medidos.

## Uso en el repositorio tito

La ruta de trabajo es `fabrica_videos/proyectos/marco_polo_5s_v1/`. Puede copiarse como carpeta independiente: lleva sus recursos visuales. NecesitaPython,Pillow,NumPy yFFmpeg enPATH. No requiere navegador niGPU.

Con el entorno ya preparado aquí:

```text
/workspace/.venvs/qwen-voz/bin/python fabrica_videos/proyectos/marco_polo_5s_v1/animar.py
```

En otra máquina, desde esta carpeta, usando unPythonconlasdependenciasya disponibles:

```text
python animar.py
```

No se han ejecutado instalaciones nuevas. `requirements.txt` describe las dependencias visuales; instalarlas en otro entorno es una acción separada. Elscript anima y puede regenerar las salidas deesta carpeta; copiar a v2 antes de modificar una versión aprobada.

## Voz y bloqueo de red

**El entorno que creó este ZIP ya tenía Supertonic3 yWhisperTiny descargados. La voz M1 de esta muestra se generó y verificó realmente aquí sin red.** Eso no prueba que estén disponibles en el entorno deClaude.

La síntesis devoz y la transcripción son componentes distintos: que falle descargarWhisper no demuestra que falleSupertonic, ni viceversa. Comprobar archivos/importaciones locales antes de intentar descargar. `generar_voz.py --comprobar` revisa rutas locales; la inferencia se verifica al generar.

El adaptador usa por defecto estas rutas existentes de`tito`:

```text
/workspace/modelos/supertonic3
/workspace/supertonic3_fuente
```

Se pueden indicar otras con `SUPERTONIC_MODEL` y `SUPERTONIC_SOURCE`. Pesos/modelos yentornosPython no se incluyen en elZIP, para evitar cientos deMB ypresuponer accesoared. Eladaptador no sobrescribe una voz ya creada.

**Si enClaude están bloqueadas las descargas:** usar `salida/voz_m1_5s.wav` ya incluido y continuar la animación/montaje; para esta prueba no hace faltaWhisper. Los subtítulos editoriales están incluidos. Para producir otra narración, generarM1enelentornoquetienelosrecursos ytransferirelWAV. No cambiar a unaAPIdepago ni prometer que una alternativa gratuita tiene licencia comercial sin revisarla.

## Entrega entre agentes

Claude puede modificar una copia v2 delproyecto y devolver ZIP o cambios deGit para revisión. Compartir objetivo,cambios yarchivo devoz, no todo elhistorial. No modificar videos aprobados ni hacerpush/publicación por defecto. Este ZIP no otorga acceso a la cuentaYouTube y no contiene claves.

Nota para publicación futura:«Narración generada mediante inteligencia artificial con Supertonic3. Imágenes recreadas». LicenciaOpenRAIL-Mdelmodelo conservada enrecursos/LICENCIA_MODELO_M1.txt;elcódigodelmotororiginal usaMIT. La naturalidad y el estilo requieren revisión humana. No es un vídeo final para publicar.
