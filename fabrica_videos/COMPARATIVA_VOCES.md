# Investigación de voces — 3 de noviembre de 2026

Estado: investigación parcial. No se instalaron modelos, no se generaron nuevas
voces, no se abrieron cuentas ni se activaron pagos. Se guardaron ocho dominios
autorizados en el borrador, preservando los seis anteriores. Las consultas a
MiniMax, ElevenLabs, Fish Audio web y Azure siguen devolviendo 403 del proxy;
no se conocen sus tarifas o cuotas vigentes a partir de esta ejecución.

## Documentación oficial consultada

- Kokoro: https://github.com/hexgrad/kokoro
  README leído: 82 millones de parámetros, idioma español mediante `lang_code='e'`,
  código y licencia Apache 2.0; el README también declara pesos Apache.
  No se han probado las voces en español. No se promete mayor naturalidad que
  Edge sin comparación de audio. No hay cuota por carácter al autoalojarlo,
  pero sí consumo de CPU y almacenamiento. Se propone evaluar en nube.
- Chatterbox: https://github.com/resemble-ai/chatterbox
  README y LICENSE leídos. Código MIT. El README presenta Multilingual V3 de
  500 millones de parámetros, soporte de español y un modelo especializado
  es-mx-latam; incluye recomendaciones de control expresivo. Turbo y Nano se
  listan para inglés, no deben recomendarse como sustituto español por su menor
  tamaño. Falta verificar licencia y requisitos del checkpoint seleccionado
  antes de descargarlo. No se ha medido velocidad o calidad en esta nube.
- Fish Speech: https://github.com/fishaudio/fish-speech
  README y LICENSE leídos. La licencia comunitaria versión 1.0, 13 de octubre
  de 2026, permite ciertos usos comerciales limitados bajo sus condiciones y
  umbral de ingresos; no es una autorización comercial universal. El README
  separa los pesos S2-Pro bajo una licencia de investigación. Esta licencia del
  modelo no establece que la web o API de Fish Audio sean gratuitas.

## Pendiente

Comprobar en MiniMax la diferencia entre web y API, existencia de créditos de
prueba o cuota recurrente, caducidad, límites, descarga y condiciones comerciales.
Comprobar los mismos puntos en ElevenLabs y Fish Audio, y si la cuota gratuita
de Azure cubre la voz/modelo expresivo elegido. No inventar cuotas ni precios.

Las páginas públicas de precios no bastan para certificar naturalidad. El paso
siguiente es comparar la misma muestra corta: cansancio, sorpresa, enfado cómico
y pregunta irónica. Escuchar antes de integrar y conservar la voz anterior.
La suscripción de ChatGPT no incluye créditos de estos servicios externos.
