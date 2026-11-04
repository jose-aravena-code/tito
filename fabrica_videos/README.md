# Fábrica de vídeos — prototipos

El episodio de comedia 3D **La alarma cobra vida** está terminado y validado.
Sus instrucciones, límites de calidad y comando de producción están en `ALARMA.md`.
Incluye salida 720×1280 y copia ligera 360×640 para descarga. El proyecto también
conserva el prototipo científico Wow! descrito a continuación.

Produce un MP4 vertical con cinco escenas animadas, narración por escenas,
subtítulos incrustados, archivo SRT, música y efectos originales. No publica
en redes sociales ni conecta cuentas. Sin APIs de pago ni suscripciones.

## Estado

Se exportó y validó `exportaciones/wow_final.mp4`: 19.7 segundos, 720×1280,
H.264/AAC, voz masculina es-MX-JorgeNeural, música con atenuación durante la
narración y cinco bloques de subtítulos ligados a los fragmentos de voz.
La decodificación completa, niveles de audio, ausencia de negros accidentales
y movimiento en todas las escenas pasaron. Informe: `registros/validacion_final.json`.
Queda la escucha y aprobación editorial del usuario; no se presenta una prueba
automática de audio como evaluación humana de naturalidad.

La previsualización `wow_PREVIA_SIN_VOZ.mp4` es explícitamente una prueba visual
con música y SIN narración. No es el vídeo terminado. `wow_final.mp4` solo se
genera cuando existen narración y tiempos reales. La voz gratuita depende de
un servicio externo no oficial y de que la política de red permita su acceso.
El dominio utilizado es `speech.platform.bing.com`. Cuando existe SSL_CERT_FILE,
el script carga esa CA en el contexto de edge-tts, manteniendo verificación TLS.
Los fragmentos completos se conservan ante fallos transitorios del proveedor.

## En esta nube

Las dependencias están aisladas en `/workspace/.venvs/wow`. Se usa el checkout
existente `/workspace/tito`; no crear worktrees adicionales.

Desde `/workspace/tito/fabrica_videos`:

```
/workspace/.venvs/wow/bin/python scripts/voz.py
/workspace/.venvs/wow/bin/python scripts/montar.py
/workspace/.venvs/wow/bin/python scripts/comprobar.py
```

Para revisar solo las animaciones mientras no está disponible la voz:

```
/workspace/.venvs/wow/bin/python scripts/montar.py --preview
/workspace/.venvs/wow/bin/python scripts/comprobar.py --preview
```

La instalación autorizada en esta nube fue:

```
python3 -m venv /workspace/.venvs/wow
/workspace/.venvs/wow/bin/python -m pip install -r requirements.txt
```

No se necesita un servidor permanente. Los procesos terminan al exportar.
No se modifican TLS, certificados, autenticación ni la política de red mediante
estos scripts. La voz envía solo el texto del guion al proveedor. No se incluyen
contraseñas ni claves en archivos.

## Uso futuro en Windows

Python, FFmpeg y FFprobe ya arrancaron en el equipo del usuario. El montaje
completo de este proyecto aún requiere prueba allí. No instalar más paquetes
ni mover programas sin explicar el tamaño y obtener autorización.

Los scripts aceptan `FFMPEG` y `FFPROBE` con rutas completas a los ejecutables,
sin necesidad de cambiar el PATH del sistema. En Windows las fuentes propuestas
son Arial y Consolas. `WOW_FONT` y `WOW_FONT_MONO` permiten elegir archivos TTF.
El codificador utiliza dos hilos y evita modelos de imagen locales. Se recomienda
el montaje en nube para el AMD A6-9225 con 8 GB de RAM.

## Revisión del resultado

`comprobar.py` comprueba H.264/AAC, 720×1280, 15–20 s, decodificación completa,
audio no vacío, niveles sin saturación digital y ausencia de intervalos negros
salvo el corte final. También compara fotogramas separados por 0.4 segundos
para verificar movimiento en cada escena. Los subtítulos se muestran por escena durante su voz;
no se promete sincronización palabra por palabra. Las imágenes `escena_*.jpg`
permiten comprobar encuadre y legibilidad. La aprobación final exige escuchar
y reproducir el MP4: las comprobaciones automáticas no valoran naturalidad.

Fuentes, alcance de las recreaciones y derechos: `guiones/wow.md`.
No borrar ni reemplazar una narración ya aprobada automáticamente. Para cambiar
voz o texto se deben apartar los `voz_*.mp3` antiguos antes de regenerarlos.
