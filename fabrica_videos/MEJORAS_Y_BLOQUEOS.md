# Mejoras con el acceso actual

Se hicieron consultas reales a cada destino; no se dedujo acceso únicamente
de la lista guardada. El servicio de estado sigue mostrando seis dominios
adicionales y estado de aplicación desconocido. No se cambió la configuración
ni se intentó publicar el entorno durante este trabajo.

| Recurso | Resultado de lectura |
|---|---|
| Documentación oficial Qwen en GitHub | HTTP 200 |
| Blog de YouTube | HTTP 200 |
| Google Trends | HTTP 200 |
| TikTok Creative Center | HTTP 200 |
| ElevenLabs, página de precios | El proxy rechaza CONNECT con 403 |
| Hugging Face, configuración del modelo Qwen | El proxy rechaza CONNECT con 403 |
| MiniMax | El proxy rechaza CONNECT con 403 |
| Instagram, primer reel de referencia | El proxy rechaza CONNECT con 403 |

HTTP 200 en una página general no demuestra acceso a todas sus APIs, datos
interactivos o vídeos. No se afirma que estos resultados midan tendencias ni
que el fallo de publicación tenga una causa ya identificada.

## Mejoras realizadas y verificadas

- **Lectura de subtítulos:** mantienen el inicio sincronizado con la voz y
  extienden el final cuando hay margen, sin invadir el diálogo siguiente ni
  cambiar de escena. Separados `fin` de audio y `fin_subtitulo`.
- **Montaje con audios locales:** manifiesto completo con rutas relativas o
  absolutas; el flujo no ejecuta el generador remoto. Verificado de principio
  a fin usando los doce audios originales existentes, no voces nuevas de
  ElevenLabs. Se reutilizaron las imágenes, sin volver a renderizar 3D.
- **Exportador ligero genérico:** herramienta sin conexión y sin paquetes
  adicionales, con protección del original y salida H.264/AAC. Probado con
  el episodio real, no solo con datos simulados.
- **Diagnóstico reproducible:** `scripts/diagnosticar_entorno.py --red`
  produce un informe sin leer claves, modificar permisos o generar audio.
  Sin `--red` solo comprueba recursos locales. Se probó en el entorno real.
- **Pruebas:** seis regresiones cubren rutas con espacios, manifiestos
  incompletos, límites de lectura, solapamientos, protección del original
  y omisión del generador remoto en modo local. Pasaron todas. La validación
  completa del episodio también pasó después del cambio de subtítulos.

Comando de las pruebas desde `fabrica_videos`:

```
/workspace/.venvs/wow/bin/python -m unittest discover -s scripts -p test_utilidades_medios.py -v
```

## Pendiente y motivo

- **Qwen VoiceDesign:** no se pudo descargar la configuración/pesos oficiales.
  Sigue sin inferencia ni voces generadas. Tras resolver el acceso habrá que
  comprobar licencia del checkpoint, posibles redirecciones y rendimiento CPU.
- **ElevenLabs/MiniMax:** siguen sin poder verificarse sus precios y condiciones
  actuales. Una vez resuelta la red, generar desde una cuenta también dependerá
  de autenticación autorizada, disponibilidad y cuota gratuita. Corregir la
  red no garantiza que todas esas operaciones sean gratuitas.
- **Reels enlazados:** bloqueados por red y posiblemente sujetos además a
  sesión/limitaciones de Instagram. Los archivos adjuntos sí pueden analizarse.
- **Calidad de voces:** este trabajo no reemplazó la voz rechazada ni inventó
  muestras nuevas. El usuario mantiene su elección artística pendiente.
- **Panel, métricas y publicación automática:** funciones futuras, no simples
  errores de red. No se implementaron ni se conectaron cuentas personales.

Todos los cambios usan herramientas instaladas. No se contrataron servicios,
se descargaron modelos nuevos ni se instaló nada en el PC del usuario.
