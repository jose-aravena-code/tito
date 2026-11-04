# La alarma cobra vida — prueba de actuación

Alcance aprobado: cuatro segundos, dos personajes propios de formas simples,
dormitorio 3D, acercamiento al botón y apertura hacia la reacción del protagonista.
No es todavía la historia completa ni la persecución del vídeo final.

- 0–1.5 s: el protagonista se acerca al despertador y dice «Cinco minutitos…».
- 1–2 s: el botón baja, se abren los ojos y se inclinan las cejas de la alarma.
- 1.7–3.3 s: la alarma responde «¡Eso dijiste ayer!» y salta.
- 2.5–4 s: el protagonista se sobresalta, levanta los brazos y retrocede.

Blender 4.3.2 ya estaba instalado. Se usa Cycles CPU con cuatro hilos y ocho
muestras por píxel para esta prueba, sin OpenImageDenoise porque no está incluido
en esta compilación. Render de prueba 360×640, escalado a 720×1280 al montar;
esto no equivale a un render nativo a 720p. Se aplica reducción suave de ruido
espacial y temporal con FFmpeg. Los primeros fotogramas conservan la prueba
inicial a 24 muestras; en una exportación limpia se vuelve a renderizar todo
con la misma configuración.

Personajes, geometría, materiales y efectos de audio propios. Diálogos de voz
sintética Edge TTS: Jorge (protagonista) y Dalia (alarma), sin modificar el tono.
No se descargaron modelos 3D ni texturas ni se instaló software adicional.

Reproducción en la nube:

```
blender -b -t 4 --python scripts/alarma_3d.py
/workspace/.venvs/wow/bin/python scripts/alarma_voz.py
/workspace/.venvs/wow/bin/python scripts/alarma_montar.py
```

La generación de voz requiere `speech.platform.bing.com` y los MP3
`recursos/audios/alarma_humano.mp3` y `alarma_reloj.mp3`.
