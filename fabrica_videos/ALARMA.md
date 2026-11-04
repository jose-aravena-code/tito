# La alarma cobra vida

Episodio de microcomedia, 22 segundos. Protagonista dormilón, alarma impaciente,
persecución, escondite detrás de una almohada, llegada al trabajo en pijama y
revelación de la alarma gigante del jefe. El cierre invita a reconocer el hábito
de posponer el despertador. No se publica automáticamente en ninguna plataforma.

Estado de esta entrega: episodio exportado y validado en ambas resoluciones.
Pasaron la decodificación completa, los 528 fotogramas de vídeo, el audio sin
picos fuera de escala, los 12 bloques de subtítulos y el movimiento de las seis
escenas. La copia ligera puede declarar 22.016 s por el empaquetado de audio AAC.
El flujo `producir_alarma.py` se ejecutó de principio a fin aprovechando los
fotogramas y voces ya generados. Falta la aprobación artística del usuario.

## Archivos

- `exportaciones/alarma_final/la_alarma_cobra_vida.mp4`: salida 720×1280, H.264/AAC.
- `/workspace/la_alarma_cobra_vida_ligera.mp4`: copia 360×640 para descargar fácilmente.
- `configuracion/alarma_historia.json`: escenas, textos, voces y horarios.
- `subtitulos/alarma_final.srt`: subtítulos externos, además de los incrustados.
- `registros/alarma_historia_validacion.json`: resultados técnicos de esta ejecución.

La imagen 3D se renderiza a 360×640. El máster se amplía a 720×1280: no equivale
a un render nativo de 720p. La apertura conserva 24 fotogramas de animación por
segundo de la prueba aprobada; las escenas nuevas usan 12 poses por segundo,
duplicadas a 24 fps al exportar. Esto reduce el costo de CPU y da una animación
limitada de caricatura. No se afirma calidad de estudio ni sincronización labial
fonética: los personajes actúan y las voces y subtítulos siguen sus intervalos.

## Reproducir el flujo en esta nube

Blender 4.3.2, FFmpeg y FFprobe ya estaban instalados. Las dependencias Python
se encuentran en `/workspace/.venvs/wow`. Se utiliza el checkout existente;
no crear worktrees adicionales. Desde `/workspace/tito/fabrica_videos`:

```
/workspace/.venvs/wow/bin/python scripts/producir_alarma.py
```

El comando conserva voces y fotogramas completos, genera los pendientes,
monta y valida ambas salidas. Si se cambia el diseño, apartar la carpeta de
fotogramas de la escena afectada antes de volver a renderizar; si se cambia
un diálogo o su voz, apartar únicamente su MP3. No reutilizar cachés de otro
diseño como prueba de un cambio que aún no se ha renderizado.

La instalación reproducible de dependencias, cuando sea necesaria y esté
autorizada, es `python3 -m venv /workspace/.venvs/wow` y después
`/workspace/.venvs/wow/bin/python -m pip install -r requirements.txt`.
No instalar Blender ni modelos pesados en el PC del usuario. La instalación
local, el rendimiento de render allí y la restauración en otra tarea no se
presentan como verificados por esta ejecución.

## Sonido y recursos

Geometría, materiales, animación y música/efectos generados dentro del proyecto.
No se utilizan personajes, clips, texturas o canciones descargadas de terceros.
Voces sintéticas: Jorge (protagonista y alarma gigante), Dalia (alarma pequeña),
Álvaro (jefe), con tono normal. Edge TTS es un cliente no oficial de un servicio
externo gratuito sujeto a condiciones y disponibilidad del proveedor.
No se garantiza acceso futuro ni se concede una licencia adicional del proveedor.
El código envía solo el diálogo a `speech.platform.bing.com`, mediante el proxy
configurado y con TLS verificado. No requiere cuentas personales en redes sociales.

La mezcla atenúa el fondo durante los diálogos. Los subtítulos se calculan
con la duración real del audio recortado y ajustado, no mediante tiempos
inventados por palabra. Se comprueba audio, formato, duración, 528 fotogramas,
movimiento de las seis escenas y decodificación completa; la revisión humana
de interpretación y humor sigue formando parte de la aprobación del vídeo.
