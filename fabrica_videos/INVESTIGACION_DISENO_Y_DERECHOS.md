# Investigación: condiciones y diseño original de voces

## Evidencia y límites

Se intentaron consultar las páginas oficiales de precios, términos y Voice
Design de ElevenLabs. El proxy devolvió 403. El dominio está autorizado en el
borrador, pero no aparece en la lista observada del entorno activo. No se
verificaron cuotas actuales, derechos del plan gratuito, redistribución de
previews ni autorización de clonación. No atribuir permisos legales al mero
hecho de poder descargar un MP3. No se accedió a la cuenta del usuario.

Separar cuatro preguntas: acceso gratuito a la muestra, crédito para sintetizar
texto propio, licencia del audio para publicación/comercialización y autorización
para usar una grabación como entrada de otro modelo. Ninguna implica las demás.
El contrato del proveedor no sustituye las leyes aplicables a voces identificables.

## Diseño por instrucciones: hallazgo confirmado

Fuente oficial consultada:
https://github.com/QwenLM/Qwen3-TTS
README, LICENSE, pyproject.toml y clase de inferencia.

`Qwen3-TTS-12Hz-1.7B-VoiceDesign` acepta `text`, `language` e `instruct`,
con descripción en lenguaje natural del timbre y de la interpretación.
La tabla oficial incluye español. El repositorio declara Apache 2.0.
Todavía hay que verificar la licencia del checkpoint exacto y sus dependencias
antes de descargarlo o desplegarlo; la licencia del código por sí sola no
resuelve derechos sobre cualquier material de referencia o exclusividad.

El flujo oficial «Voice Design then Clone» diseña primero una voz y emplea
esa muestra sintética como referencia reutilizable con un modelo Base.
Esto sirve para personajes consistentes, sin copiar la voz descargada de
ElevenLabs ni incorporar una voz ajena como referencia de identidad.
Una descripción de rasgos generales no garantiza un timbre exacto o exclusivo.

## Alternativas y recursos

- Kokoro: ya instalado y probado. Interpolación de estilos posible, pero las
  tres mezclas no produjeron diferencias útiles para el usuario. No tratarlo
  como diseño de voz libre por prompt.
- Chatterbox: documentación multilingüe y controles de expresividad revisados.
  Es candidato para interpretación/referencia; no equiparar esos controles
  con el diseño detallado por texto documentado en Qwen VoiceDesign.
- Qwen VoiceDesign: modelo de 1.7 mil millones de parámetros. Los ejemplos
  oficiales usan CUDA y bfloat16. No se ha confirmado una GPU utilizable ni
  se ha medido rendimiento en CPU de esta nube. No recomendado para el PC
  AMD A6 con 8 GB del usuario.

No se descargaron modelos adicionales ni se instalaron dependencias de Qwen.
Autoalojar un modelo abierto evita cobro por caracteres al proveedor, pero no
garantiza cómputo gratuito ilimitado. Antes de instalar, presentar tamaño de
descarga real o estimado, uso de disco y viabilidad; obtener autorización.

## Perfil propuesto para el primer ensayo

Voz masculina adulta joven; español latinoamericano claro; timbre cálido de
registro medio, cercano y conversacional; consonantes claras sin sobreactuar;
pausas naturales y energía; evitar solemnidad, gravedad forzada y vibrato
marcado. No pedir imitación exacta del locutor de la muestra ElevenLabs.

Prueba futura: diseñar tres voces con variaciones claras de timbre y probar
la misma frase en tono neutral, sorpresa y reproche cómico. Escucha del usuario
antes de integrar. No prometer mejora sobre ElevenLabs sin muestras reales.
