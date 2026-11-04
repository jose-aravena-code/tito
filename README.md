# Fábrica de vídeos cortos

Prototipo de producción de vídeos verticales mediante Python, FFmpeg y Blender,
orientado a herramientas gratuitas y trabajo en la nube. Este repositorio guarda
el código, configuraciones sin secretos, guiones, documentación y subtítulos.
Los modelos, dependencias, grabaciones y exportaciones se conservan fuera de Git.

## Qué está probado

- **La alarma cobra vida:** episodio 3D de 22 segundos, con personajes propios,
  diálogos sintéticos, música y efectos originales y subtítulos. Se validaron
  las versiones 720×1280 y ligera 360×640. El render nativo es de 360×640.
- **La señal Wow!:** prototipo científico de 19.7 segundos con animaciones,
  narración y subtítulos.
- **Pruebas de voz:** Edge TTS y Kokoro, incluidas mezclas de estilos de Kokoro.
  Las mezclas no produjeron la diferencia perceptible buscada por el usuario.

No hay publicación automática en redes sociales ni cuentas personales conectadas.
La evaluación de voces, interpretación y estilo requiere revisión del usuario.

## Por dónde empezar

1. Lee [las instrucciones del episodio de la alarma](fabrica_videos/ALARMA.md).
2. Consulta [la documentación general](fabrica_videos/README.md).
3. Los comandos se ejecutan desde `fabrica_videos/`. El flujo probado en la nube es:

```
/workspace/.venvs/wow/bin/python scripts/producir_alarma.py
```

Ese comando necesita las herramientas y dependencias descritas en las instrucciones.
Una clonación nueva no incluye los programas instalados, los modelos ni los
fotogramas previamente renderizados; deberá preparar las dependencias y generar
los recursos. No se ha verificado esta preparación en una tarea nueva o en Windows.

Para el PC AMD A6-9225 con 8 GB de RAM se recomienda usar el navegador para
supervisar y realizar el renderizado en la nube. No instalar modelos grandes
en ese equipo sin revisar antes los requisitos.

## Trabajo pendiente

- **Qwen VoiceDesign:** dependencias de CPU instaladas en un entorno separado,
  perfiles y script preparados. No se han descargado los pesos ni generado
  muestras: el alojamiento del modelo sigue bloqueado por la red del entorno.
  Ver [el estado documentado](fabrica_videos/QWEN_ESTADO.md).
- **ElevenLabs:** seis voces elegidas por el usuario, pendientes de comprobar
  disponibilidad, costos y derechos de uso. No se ha generado audio mediante
  una cuenta de ElevenLabs ni se ha incorporado una clave API.
- **Publicación del entorno:** falla en la interfaz. No se ha establecido su
  causa; subir este código a GitHub no demuestra que el fallo quede resuelto.

## Datos y seguridad

No guardar claves, contraseñas, archivos `.env`, certificados privados o cookies
en este repositorio. Los requisitos de autenticación deben configurarse mediante
secretos del entorno, nunca escribirse en el código. No subir grabaciones
personales o recursos de terceros sin revisar autorización y licencia.

Los MP4 y paquetes descargables entregados por chat no se incluyen en Git.
Las condiciones de servicios externos y las licencias de cada modelo deben
comprobarse antes de publicar contenido o iniciar una integración nueva.
