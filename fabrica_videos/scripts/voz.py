"""Genera voz por escenas; no sustituye fallos por una pista silenciosa."""
import asyncio
import json
import os
from pathlib import Path
import shutil
import subprocess

import edge_tts
import edge_tts.communicate as edge_communicate

ROOT = Path(__file__).resolve().parents[1]
CFG = json.loads((ROOT / 'configuracion/wow.json').read_text(encoding='utf-8'))


def tool(name):
    return os.environ.get(name.upper()) or shutil.which(name) or name


def duration(path):
    return float(subprocess.check_output([
        tool('ffprobe'), '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=nw=1:nk=1', str(path)], text=True).strip())


async def main():
    # edge-tts fija certifi en su contexto TLS. Añadimos la CA ya confiada
    # por el entorno, sin desactivar validación de certificados o del hostname.
    ca_file = os.environ.get('SSL_CERT_FILE')
    if ca_file and Path(ca_file).is_file():
        edge_communicate._SSL_CTX.load_verify_locations(cafile=ca_file)
    target = ROOT / 'recursos/audios'
    target.mkdir(parents=True, exist_ok=True)
    for i, segment in enumerate(CFG['segments']):
        path = target / f'voz_{i}.mp3'
        if not path.exists() or path.stat().st_size < 1000:
            # El servicio puede cerrar una petición sin audio. Conservamos las
            # escenas completas y solo reintentamos el fragmento fallido.
            temporary = path.with_suffix('.partial.mp3')
            for attempt in range(3):
                comm = edge_tts.Communicate(
                    segment['text'], voice=CFG['voice'], rate=CFG['rate'],
                    pitch=CFG['pitch'], proxy=os.environ.get('HTTPS_PROXY'),
                    connect_timeout=15, receive_timeout=30,
                )
                try:
                    await comm.save(str(temporary))
                    if duration(temporary) <= 0:
                        raise RuntimeError('Audio vacío')
                    temporary.replace(path)
                    break
                except edge_tts.exceptions.NoAudioReceived:
                    temporary.unlink(missing_ok=True)
                    if attempt == 2:
                        raise
                    print(f'Escena {i+1}: servicio sin audio; reintento {attempt+1}/2', flush=True)
                    await asyncio.sleep(1 + attempt)
        if duration(path) <= 0:
            raise RuntimeError(f'Audio inválido: {path}')
        print(f'Escena {i+1}: {duration(path):.2f} s', flush=True)

    # Se mantiene el tono al ajustar ligeramente el ritmo para encajar a 19.8 s.
    raw = sum(duration(target / f'voz_{i}.mp3') for i in range(5))
    gaps = [0.10, 0.12, 0.12, 0.32, 0.28]
    speed = raw / (19.8 - sum(gaps))
    if not 0.80 <= speed <= 1.30:
        raise RuntimeError(f'El ajuste de ritmo {speed:.2f} es excesivo; revisar guion o voz')
    timeline = []
    start = 0.0
    for i, gap in enumerate(gaps):
        wav = target / f'escena_{i}.wav'
        subprocess.run([
            tool('ffmpeg'), '-y', '-v', 'error', '-i', str(target / f'voz_{i}.mp3'),
            '-af', f'atempo={speed:.8f},apad=pad_dur={gap}', '-ar', '48000',
            '-ac', '1', str(wav)], check=True)
        length = duration(wav)
        timeline.append({'start': start, 'end': start + length,
                         'speech_end': start + length - gap, **CFG['segments'][i]})
        start += length
    files = target / 'concat.txt'
    files.write_text(''.join(f"file 'escena_{i}.wav'\n" for i in range(5)), encoding='utf-8')
    subprocess.run([tool('ffmpeg'), '-y', '-v', 'error', '-f', 'concat', '-safe', '0',
                    '-i', str(files), '-c:a', 'pcm_s16le', str(target / 'narracion.wav')], check=True)
    (target / 'timeline.json').write_text(json.dumps(timeline, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'Voz final: {start:.3f} s. Ajuste temporal: {speed:.3f}')


if __name__ == '__main__':
    asyncio.run(main())
