
import asyncio, os, tempfile
from app.services.minio_service import minio_service
from faster_whisper import WhisperModel

async def main():
    p = 'meetings/ee576e37-c033-4f4f-afe4-9c4b27ebd947.m4a'
    tf = tempfile.NamedTemporaryFile(delete=False, suffix='.m4a')
    t = tf.name
    r = minio_service.get_audio_file_stream(p)
    for d in r.stream(32*1024): tf.write(d)
    r.close(); r.release_conn()
    m = WhisperModel('small', compute_type='int8')
    segs, _ = m.transcribe(t, language='hi', task='translate', condition_on_previous_text=False)
    print('RES1:', ''.join([s.text for s in segs]))
    segs2, _ = m.transcribe(t)
    print('RES2:', ''.join([s.text for s in segs2]))
    os.remove(t)

asyncio.run(main())

