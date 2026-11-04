# Contexto e instrucciones del proyecto

Este archivo conserva las decisiones importantes de la conversación para poder
continuar en otra sesión. Actualizarlo cuando cambie el estado real del proyecto.
No confundir una propuesta, un script preparado o una instalación con una
función ejecutada y validada. Las instrucciones nuevas del usuario prevalecen.

## Objetivo

Construir una fábrica semiautomática de vídeos cortos para YouTube Shorts,
Instagram Reels y TikTok. El usuario supervisará, revisará y aprobará resultados
desde su ordenador o teléfono. Empezar por prototipos funcionales y ampliar
después. El usuario prefiere historias entretenidas, personajes y acciones;
no presentaciones de diapositivas ni narraciones monótonas.

Usar herramientas gratuitas o de muy bajo costo. Para las pruebas de voz el
usuario ha exigido explícitamente **costo cero**: sus autorizaciones de acceso
o instalación están condicionadas a no generar cargos. No contratar planes,
activar suscripciones, alquilar GPU ni consumir servicios facturables sin
explicar el costo y recibir autorización específica.

## Cómo colaborar con el usuario

- Hablar en español sencillo y enseñar paso a paso: no tiene experiencia avanzada.
- Dar una acción concreta cada vez cuando se trabaje con Windows o formularios.
  Distinguir claramente navegador, Explorador de archivos y terminal.
- En comandos para principiantes, no mostrar etiquetas como `bat` dentro del
  texto que deba copiar: en una ocasión escribió esa etiqueta como comando.
- Antes de instalaciones, descargas o cambios importantes, explicar propósito,
  tamaño aproximado y efecto en el rendimiento; obtener autorización. Reutilizar
  autorizaciones ya dadas para la misma acción, sin pedirlas repetidamente.
- No sustituir una entrega por fragmentos de código: crear archivos reales,
  ejecutar lo autorizado y comprobar los resultados.
- No afirmar haber escuchado o visto material que solo se ha analizado mediante
  métricas o fotogramas. La revisión humana de naturalidad y humor sigue pendiente
  hasta que el usuario la haga.
- No conectar cuentas personales, pedir contraseñas o solicitar claves en el
  chat. Una consulta sobre API no autoriza su contratación o consumo.
- No publicar el entorno ni subir contenido a redes sociales sin instrucción.
  Guardar un borrador de configuración, hacer push a GitHub y publicar el
  entorno son operaciones distintas.
- Se pueden mantener las conversaciones relacionadas en este chat. Conservar
  las decisiones también en archivos para no depender solo del historial.

## Equipo del usuario y entorno de trabajo

PC: AMD A6-9225, 8 GB de RAM, SSD de 480 GB. La captura de `winver` confirmó
Windows 10 Home Single Language 1809, compilación 17763.107. El usuario creyó
haber actualizado, pero la instalación de 22H2 falló con `0xC1900101`. No
suponer una versión más reciente sin evidencia nueva.

En Windows se instalaron o extrajeron y se comprobó su ejecución:

- Python 3.13.13 de 64 bits: `python --version` respondió correctamente.
- FFmpeg y FFprobe 9.0.2, paquete Essentials de Gyan. Se usaron por ruta
  completa; no se añadió FFmpeg al PATH del sistema.
- Ruta observada de los ejecutables:
  `%USERPROFILE%\Downloads\ffmpeg-9.0.2-essentials_build\ffmpeg-9.0.2-essentials_build\bin`.
- Python se instaló para el usuario con la opción de añadirlo al PATH. No se
  pidió activar «Disable path length limit» ni modificar otros ajustes.

El trabajo pesado se hace en Linux en la nube, separado de ese PC. No hay
acceso directo a la pantalla o archivos de Windows. En la nube se observaron
Python 3.12.14, FFmpeg/FFprobe 7.1.5 y Blender 4.3.2. Hubo aproximadamente
33 GiB de RAM y decenas de GB libres: volver a medir antes de un trabajo pesado.
PyTorch de la prueba Qwen es CPU y detectó CUDA no disponible.

Repositorio: `jose-aravena-code/tito`, checkout `/workspace/tito`, rama `main`.
Inicialmente estaba vacío; ya se hizo un primer push de código y documentación,
commit `ba43af5cba9026993989ac02f96a10622429aa0b`. GitHub se verificó mediante
Git HTTPS y la autenticación suministrada por la plataforma. No se necesitó
pedir un token personal. No tratar ese commit histórico como el HEAD perpetuo.
Utilizar el checkout existente; no crear worktrees salvo petición del usuario.

## Herramientas, habilidades y complementos

- ChatGPT/Codex como asistente de programación. El usuario tiene Plus; eso no
  implica créditos incluidos para APIs de ElevenLabs, MiniMax u otros servicios.
- Terminal, Git, edición de archivos y análisis local de medios en la nube.
- Python, NumPy, Pillow, FFmpeg, FFprobe y Blender para imágenes, animación,
  mezcla, exportación y validación. No se instalaron editores pesados en el PC.
- Habilidades utilizadas: `cloud-environment-onboarding:setup` y
  `cloud-environment:cloud-environment-runtime`. Leer sus instrucciones aplicables
  al preparar o diagnosticar el entorno; usar las herramientas de estado y
  borrador para distinguir configuración deseada y acceso efectivo.
- El generador de imágenes está disponible como herramienta de la sesión,
  pero los vídeos entregados se hicieron con recursos programáticos. Su
  disponibilidad no demuestra gratuidad ni uso previo.
- Edge TTS: cliente no oficial de un servicio externo, sin cuenta del usuario
  conectada. Depende de red y disponibilidad; no prometer acceso ilimitado.
- Kokoro ONNX: modelo abierto instalado y utilizado en CPU.
- Qwen VoiceDesign: dependencias preparadas; modelo e inferencia pendientes.
- No hay un complemento de ElevenLabs, MiniMax o Instagram conectado. Tampoco
  se conectaron YouTube, Instagram o TikTok para publicar o ver estadísticas.

## Organización y comandos

Carpeta principal: `fabrica_videos/`. Contiene `scripts/`, `configuracion/`,
`guiones/`, `recursos/{imagenes,videos,audios,musica}/`, `subtitulos/`,
`exportaciones/` y `registros/`.

Entorno principal de Python: `/workspace/.venvs/wow`. Entorno Qwen separado:
`/workspace/.venvs/qwen-voz`. Los modelos están fuera del checkout, en
`/workspace/modelos/`. Los procesos y la autenticación no deben darse por
persistidos al restaurar una instantánea. Tampoco asumir que esos caminos y
dependencias existirán en una clonación nueva.

Desde `/workspace/tito/fabrica_videos`:

```text
/workspace/.venvs/wow/bin/python scripts/producir_alarma.py
/workspace/.venvs/wow/bin/python scripts/comparar_voces.py
/workspace/.venvs/wow/bin/python scripts/comparar_kokoro.py
/workspace/.venvs/wow/bin/python scripts/mezclar_kokoro.py
```

Consultar `README.md`, `fabrica_videos/README.md`, `ALARMA.md`, `KOKORO.md` y
`QWEN_ESTADO.md` antes de reproducir o modificar un flujo. Si cambia el diseño
o texto, no reutilizar su caché antigua como evidencia del cambio. Conservar
las voces y fotogramas completos cuando el diseño no haya cambiado.

## Entregas realizadas

### La señal Wow!

Prototipo científico de 19.7 segundos: MP4 vertical, 720×1280, H.264/AAC,
narración masculina española, subtítulos por escena, animaciones, ambientación
y efectos originales. Se verificaron formato, audio, movimiento, decodificación
y ausencia de negros accidentales. Fuentes y límites en `guiones/wow.md`.
Los sonidos y las imágenes son recreaciones, no pruebas o grabaciones históricas.
No presentar el origen extraterrestre como demostrado.

Salida de esta instancia: `fabrica_videos/exportaciones/wow_final.mp4`.
El ejemplo previo «5 datos sorprendentes sobre el universo» quedó como propuesta;
no se produjo ese vídeo.

### La alarma cobra vida

El usuario aprobó una prueba de cuatro segundos con personajes 3D y después
pidió completar el episodio. Se produjo una microcomedia de 22 segundos con:
botón «posponer», despertador impaciente, persecución, escondite tras una
almohada, llegada a la oficina en pijama y alarma gigante del jefe.

Geometría, materiales, música y efectos propios. Voces originales de la entrega:
Jorge, Dalia y Álvaro de Edge TTS. No se usaron modelos 3D o canciones descargadas.
El render nativo es 360×640, ampliado a 720×1280. La apertura tiene 24 poses/s;
las escenas nuevas, 12 poses/s duplicadas a salida 24 fps. No prometer render
nativo 720p, sincronización labial fonética ni calidad de estudio.

Se validaron las dos versiones completas: duración, 528 fotogramas, H.264/AAC,
12 diálogos y bloques de subtítulos, audio, movimiento por escena y decodificación.
Se corrigió un pico AAC bajando la mezcla antes de la entrega final.

Archivos entregados en esta instancia:

- `/workspace/la_alarma_cobra_vida_ligera.mp4` — unos 1.7 MB.
- `fabrica_videos/exportaciones/alarma_final/la_alarma_cobra_vida.mp4` — 720×1280.
- `/workspace/fabrica_alarma_proyecto.zip` — código e instrucciones descargables.

El usuario no podía abrir los enlaces locales anteriores. Los enlaces con
`sandbox:/workspace/...` y las copias ligeras sí le funcionaron. Comprobar que
el archivo existe antes de enlazarlo y no inventar vistas previas localhost.

## Estilo audiovisual y referencias

Preferir microhistorias con gancho visual inmediato, acciones, expresiones,
cambios de plano, pocos diálogos y remate cómico. La segunda de las primeras
referencias adjuntas tenía personajes 3D de bloques; fue la dirección elegida,
con diseños propios. La primera era un personaje 2D con tarjetas explicativas.
Las afirmaciones promocionales y métricas de esos vídeos no fueron verificadas.

Se recibieron además seis reels de Instagram: `DfNxUfkJZu_`, `DfQFjxvA8Tc`,
`DfPvfQWx61s`, `De9ROc5IlxL`, `DfCgz9vqRT7` y `DfQrZnsBlRr`. No se han
analizado sus contenidos: el intento de acceso fue bloqueado. Pedir archivos
adjuntos o grabaciones de pantalla si el acceso web sigue sin funcionar.

Google Trends, TikTok Creative Center y el blog de YouTube llegaron a responder
HTTP 200 cuando se aplicaron esos permisos, pero no se obtuvo un ranking
verificable que pruebe que este estilo sea viral. No prometer viralidad.

## Voces: preferencias y resultados reales

El usuario quiere una voz masculina adulta joven, cálida, cercana, de registro
medio, fluida y con energía. No quiere voz de anciano, locutor solemne, gravedad
forzada ni consonantes exageradas. Importan las pausas y la actuación cómica.

- Se generó una comparación real de seis voces Edge TTS: Jorge, Álvaro,
  Lorenzo, Dalia, Elvira y Catalina. Solo Álvaro y Lorenzo le parecieron
  aceptables, como alternativas provisionales; no quedó satisfecho.
- Kokoro: motor `kokoro-onnx==0.6.1`, ONNX Runtime 1.31.1 y
  espeakng-loader 0.2.4. Pesos y voces de la publicación oficial de
  `thewh1teagle/kokoro-onnx`, unos 338 MB, más dependencias.
- Se generaron muestras españolas masculinas `em_alex` y `em_santa`. El usuario
  las percibió fluidas, pero mayores y demasiado moduladas.
- Se interpolaron sus estilos en 75/25, 50/50 y 25/75. El usuario consideró
  que sonaban iguales. No insistir en que el cambio numérico equivalga a una
  mejora perceptible, ni repetir esa estrategia como solución ya demostrada.
- Las comparaciones usaron la misma frase, sin música y sin cambio de tono:
  «¿Cinco minutitos más? ¡Eso dijiste ayer! Vamos, que llegamos tarde».
- El usuario ofreció enviar su propia voz; no identificar como suya la muestra
  de un locutor de ElevenLabs que adjuntó posteriormente.

### Selección preferida de ElevenLabs

El usuario eligió expresamente estas seis voces para proyectos futuros:

1. `aYbngTsp5kp0sibI3Z0T`
2. `htFfPSZGJwjBv1CL0aMD`
3. `DdKbXdRlBmj7Ty7N0FVr`
4. `vPrtQbTwtAoP87VnQmID`
5. `Wl3O9lmFSMgGFTTwuS6f`
6. `XJPGNjKfwXiN0kGtutbV`

Enlaces: `https://elevenlabs.io/voices/<voice_id>`.
Datos conservados en `configuracion/voces_elevenlabs.json`. No inventar sus
nombres ni afirmar haberlas escuchado por esos enlaces: fueron bloqueados.
El usuario adjuntó `voice_preview_javi rojas - rich, polished and elegant.mp3`;
una captura confirmó «Javi Rojas - Rico, refinado y elegante» en su biblioteca.
Eso demuestra disponibilidad en la interfaz, no derechos de publicación,
monetización, redistribución o uso como referencia de clonación.

No hay cuenta ni clave API de ElevenLabs configurada. No se ha generado audio
de ElevenLabs desde este proyecto. La cuota gratuita y las condiciones vigentes
siguen sin verificar por el bloqueo de acceso. No citar cifras antiguas de
créditos o atribuir permisos por estar una voz en una sección gratuita.

Separar siempre: escuchar una muestra, generar texto propio, editar/publicar
el audio y usarlo como referencia en otro modelo. Son permisos distintos.
Una API puede consumir créditos; la autorización creativa del usuario no
autoriza cobros. No solicitar una clave hasta que haya una integración concreta,
condiciones verificadas y un método seguro de introducirla fuera del chat.

### Voz original mediante Qwen: objetivo pendiente

Se investigó `Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign`: la documentación oficial
describe generación por instrucciones y admite español. El código declara
Apache 2.0; falta verificar la ficha/licencia del checkpoint antes de usarlo.
El flujo documentado «Voice Design then Clone» permitiría reutilizar una voz
diseñada como referencia propia. No garantiza exclusividad ni calidad concreta.

El usuario autorizó generar voces originales únicamente si es gratuito:

- Entorno separado `/workspace/.venvs/qwen-voz`, unos 1.8 GB instalados.
- PyTorch y torchaudio 2.8.0+cpu; qwen-tts 0.1.1. Importación comprobada y
  `pip check` sin dependencias rotas.
- CUDA no disponible; FlashAttention y SoX del sistema ausentes. No se instaló
  CUDA ni se alquiló GPU. La ruta preparada es CPU/float32/atención eager.
- Tres perfiles: Cercana, Ágil y Cálida, con instrucciones de estilo generales,
  sin MP3 de ElevenLabs ni imitación exacta de un locutor.
- Script `scripts/qwen_voz_original.py` y configuración
  `configuracion/qwen_voces_originales.json` preparados, **no validados en inferencia**.
- **No se descargaron los pesos y no se ha generado ninguna voz de Qwen.**
  Hugging Face y ModelScope devolvieron 403 del proxy. Tamaño total de 5–8 GB
  fue una estimación, no una descarga medida ni un costo facturado.

Antes de continuar: comprobar acceso, licencia del checkpoint y recursos;
descargar desde fuente oficial con TLS y comprobaciones disponibles; generar
muestras reales, validar audio y dejar elegir al usuario. No prometer mayor
naturalidad o funcionamiento en CPU sin probarlos. El modelo abierto evita
cuotas de API, no garantiza cómputo gratuito ilimitado en una plataforma.

## Red, publicación y lista exacta guardada

Ha persistido este error de interfaz:
«No se pudo publicar el entorno. Se guardó tu configuración. Intenta publicar
de nuevo». Los cambios pueden estar en el borrador sin aplicarse al entorno.
No se ha determinado la causa. Se aconsejó reportarlo al soporte; el formulario
del usuario no permite adjuntar capturas. No afirmar que ya exista un ticket.

La última observación de ejecución solo incluía seis dominios adicionales y
las consultas nuevas devolvían 403. El estado de aplicación apareció a veces
como `unknown`; eso no certifica ni aplicación ni salud. Volver a consultar
estado y probar la operación requerida tras un cambio real, sin reintentar
indefinidamente lo mismo ni pedir autorizaciones ya dadas.

El repositorio inicialmente vacío fue una hipótesis del usuario sobre el error,
no una causa confirmada. El código ya está en GitHub. No asegurar que eso
resuelva la publicación. No borrar o recrear el entorno ni resetear archivos
para intentar solucionarlo sin diagnóstico y preservación del trabajo.

**Estos son los 15 dominios adicionales exactamente guardados en el borrador
al crear este archivo. No son una afirmación de que los 15 estén activos.**
Los dominios de presets para gestores de paquetes son una lista separada.

```text
ads.tiktok.com
azure.microsoft.com
blog.youtube
docs.fish.audio
elevenlabs.io
fish.audio
huggingface.co
minimax.audio
phl.upr.edu
platform.minimax.io
speech.platform.bing.com
trends.google.com
www.minimax.audio
www.minimax.io
www.seti.org
```

No se añadió Instagram a esta lista: se explicó al usuario cómo hacerlo, pero
no se verificó un guardado de ese dominio. No reemplazar la lista desconocida
de una sesión futura con esta copia histórica: leer primero el borrador actual
y preservar sus entradas. El usuario ya autorizó las consultas a los servicios
anteriores y el intento de Qwen gratuito; comprobar alcance antes de ampliarlo.

El proxy es la salida de red gestionada por la plataforma. No editar su archivo
de política para intentar conceder acceso, no evitar el proxy, no desactivar
TLS y no extraer credenciales de Git o del entorno. Permitir Instagram tampoco
garantizaría acceso a reels: puede exigir sesión o bloquear automatización.

## Seguridad, Git y comprobaciones

- No subir `.env`, claves, cookies, contraseñas, modelos, entornos Python,
  grabaciones personales ni cachés. `.gitignore` protege esos archivos y las
  carpetas de audio, música, registros y exportaciones generadas.
- Los identificadores públicos de voces no son claves API, pero no incluir
  material de referencia de terceros en Git sin comprobar sus derechos.
- Mantener el código ligero. Los vídeos y ZIP entregados por chat están fuera
  de Git; una clonación nueva no los incluye y debe regenerarlos.
- Antes de subir cambios, revisar estado, diff y posibles secretos. No forzar
  pushes, borrar trabajo, sobrescribir el remoto ni publicar el entorno como
  efecto secundario de un push. Verificar el SHA remoto tras subir.
- Para una modificación documental basta validar contenido y enlaces relevantes;
  no volver a renderizar vídeos por cambios de documentación.
- Para medios, validar existencia, duración, dimensiones, códecs, audio real y
  decodificación completa. Distinguir controles automáticos de escucha humana.
  Investigar errores y no bajar umbrales solo para hacerlos pasar.

## Funciones futuras todavía no implementadas

Generación masiva, biblioteca general de recursos, temáticas/canales múltiples,
panel de control, aprobación desde móvil, programación y publicación en redes,
estadísticas e integraciones con cuentas. No presentarlas como disponibles.
Primero resolver acceso y elegir una voz que convenza al usuario; continuar
con prototipos verificables y mejoras de actuación/animación según su revisión.
