# Voz original Qwen — preparación

Autorización: instalar y generar únicamente con herramientas gratuitas, sin API
de pago, sin alquilar GPU y sin instalar programas en el PC del usuario.

Se prepara un entorno separado `/workspace/.venvs/qwen-voz`, conservando intacto
el entorno de Kokoro y los vídeos anteriores. PyTorch y torchaudio 2.8.0+cpu,
qwen-tts 0.1.1; inferencia propuesta en CPU float32 con atención eager. No se
instala FlashAttention ni CUDA. No se garantiza velocidad adecuada en CPU.

El repositorio oficial Qwen3-TTS y su código declaran Apache 2.0. Antes de usar
los pesos se debe consultar la ficha/licencia del checkpoint oficial; esa ficha
está bloqueada por la política de red actual. No se afirma haberla verificado.

`huggingface.co` se añadió al borrador autorizado, sin quitar dominios existentes.
Las peticiones al sitio oficial de pesos y a ModelScope devolvieron 403 del proxy.
Guardar el borrador no activa el acceso ni publica una instantánea. Si la
descarga redirige a otro host, diagnosticar el host exacto y autorizarlo mediante
la configuración; no evitar el proxy ni desactivar TLS.

Se prepararon tres perfiles de diseño, con descripciones distintas de timbre y
actuación, sin nombres de locutores ni archivos de referencia de ElevenLabs.
Configuración: `configuracion/qwen_voces_originales.json`.
Script: `scripts/qwen_voz_original.py`.

Primero, con acceso activo y licencia verificada:

```
/workspace/.venvs/qwen-voz/bin/python scripts/qwen_voz_original.py --descargar
```

La descarga/inferencia aún no está validada. No presentar este script preparado
como una voz generada, ni las dependencias instaladas como un modelo listo.
Las muestras solo se entregarán tras generar y comprobar los WAV reales.
Tamaño estimado total de dependencias y modelo: 5–8 GB; no es un tamaño medido
de la descarga final. El cómputo depende de los límites de la plataforma.

Comprobación real: dependencias instaladas en 1.8 GB. PyTorch 2.8.0+cpu importa
y detecta CUDA no disponible. Qwen3TTSModel importa y `pip check` no detecta
dependencias rotas. Hay avisos por SoX del sistema y FlashAttention ausentes.
La ruta prevista usa CPU/eager; no se instaló CUDA ni se alquiló GPU.
No se ha probado inferencia, por lo que estos chequeos no certifican una voz lista.
