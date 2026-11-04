"""Regresiones de importación offline y límites temporales, sin servicios web."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from utilidades_medios import audios_locales, tiempos_legibles, exportar_ligero
import producir_alarma

class MediosTests(unittest.TestCase):
    def test_rutas_relativas_y_espacios(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);(p/'voz personal.wav').write_bytes(b'ejemplo')
            (p/'audios.json').write_text(json.dumps({'frase':'voz personal.wav'}))
            self.assertEqual(audios_locales(p/'audios.json',['frase'])['frase'],p/'voz personal.wav')

    def test_importacion_incompleta_rechazada(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'audios.json';p.write_text('{}')
            with self.assertRaises(ValueError):audios_locales(p,['falta'])

    def test_lectura_mas_larga_sin_tapar_siguiente(self):
        eventos=[{'inicio':0,'fin':.3,'texto':'Eso dijiste ayer'},
                 {'inicio':1,'fin':1.3,'texto':'Vamos'}]
        salida=tiempos_legibles(eventos,[{'inicio':0,'duracion':2}],2)
        self.assertGreater(salida[0]['fin_subtitulo'],.3)
        self.assertLess(salida[0]['fin_subtitulo'],1)
        self.assertEqual(salida[1]['fin_subtitulo'],2)

    def test_no_oculta_solapamiento_o_voz_fuera_de_escena(self):
        with self.assertRaises(ValueError):
            tiempos_legibles([{'inicio':0,'fin':1.2,'texto':'a'},
                              {'inicio':1,'fin':1.5,'texto':'b'}],[{'inicio':0,'duracion':2}],2)
        with self.assertRaises(ValueError):
            tiempos_legibles([{'inicio':.5,'fin':1.2,'texto':'a'}],[{'inicio':0,'duracion':1}],2)

    def test_no_sobrescribe_original(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'video.mp4';p.write_bytes(b'original')
            with self.assertRaises(ValueError):exportar_ligero(p,p)
            self.assertEqual(p.read_bytes(),b'original')

    def test_modo_local_no_ejecuta_generador_remoto(self):
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder);(p/'voz.wav').write_bytes(b'ejemplo')
            cfg=json.loads((producir_alarma.ROOT/'configuracion/alarma_historia.json').read_text())
            manifest=p/'audios.json'
            manifest.write_text(json.dumps({d['archivo']:'voz.wav' for d in cfg['dialogos']}))
            calls=[]
            with patch('sys.argv',['producir_alarma.py','--audios-locales',str(manifest)]), \
                 patch.object(producir_alarma.shutil,'which',return_value='/usr/bin/blender'), \
                 patch.object(producir_alarma,'ready',return_value=True), \
                 patch.object(producir_alarma,'run',side_effect=lambda args:calls.append(args)):
                producir_alarma.main()
            self.assertFalse(any('alarma_historia_voz.py' in ' '.join(c) for c in calls))
            self.assertTrue(any('--audios-locales' in c for c in calls))

if __name__=='__main__':unittest.main()
