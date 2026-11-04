# Comparación gratuita Edge TTS / Kokoro

Se instaló Kokoro ONNX 0.6.1 en el entorno aislado de la nube, con ONNX Runtime
1.31.1 y espeakng-loader 0.2.4. Motor con licencia MIT; el modelo Kokoro-82M
se distribuye con licencia Apache 2.0 según el repositorio oficial de hexgrad.
No se utilizó una API de pago, ni suscripciones ni cuentas externas.

Archivos descargados desde la publicación oficial `model-files-v1.1` de
https://github.com/thewh1teagle/kokoro-onnx/releases :

- `kokoro-v1.0.onnx`: 325505369 bytes. SHA256 calculado localmente:
  `beb0d1848dee9a49da392cc3df26958d46cfa35d321edf434f52949153f0df3a`.
- `voices-v1.0.bin`: 28214398 bytes. SHA256 calculado localmente:
  `bca610b8308e8d99f32e6fe4197e7ec01679264efed0cac9140fe9c29f1fbf7d`.

Las descargas utilizaron HTTPS con verificación TLS; los hashes son un registro
local, no una comparación con checksums independientes publicados.
Los modelos están en `/workspace/modelos/kokoro`, fuera del repositorio.

La comparación contiene Álvaro y Lorenzo (Edge, muestras anteriores) y las dos
voces masculinas españolas del archivo de Kokoro: `em_alex` y `em_santa`.
Se utilizó `lang='es'` y velocidad 1.0, sin modificar el tono. Se ajustó solo
volumen y silencio entre muestras, sin música. No se evaluó perceptualmente
la naturalidad: esa decisión corresponde a la escucha del usuario.

Repetir en la misma nube, con muestras Edge y modelos conservados:

```
/workspace/.venvs/wow/bin/python scripts/comparar_kokoro.py
```

Salida: `/workspace/comparacion_edge_kokoro.mp4`, 26.69 segundos, 360×640,
H.264/AAC. Se verificaron decodificación completa, cuatro muestras no vacías
y pico de audio inferior a escala completa. Las dependencias opcionales están
en `requirements-kokoro.txt`. No se probó la instalación en Windows ni se
instalaron modelos o programas en el equipo del usuario. El uso del modelo
no tiene cuota por carácter; la capacidad de cómputo de la nube depende de la
plataforma y no se promete acceso ilimitado.
