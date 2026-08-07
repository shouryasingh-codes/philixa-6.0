import asyncio
from deepgram import DeepgramClient, PrerecordedOptions
import os

async def main():
    deepgram = DeepgramClient(api_key="4c19be06ceeadd28ffdd477106bc50c40191a845")
    
    with open('data/debug_live.wav', 'rb') as f:
        buffer = f.read()

    payload = {
        "buffer": buffer,
    }

    options = PrerecordedOptions(
        model="nova-2",
        language="hi",
        smart_format=True,
    )

    response = await deepgram.listen.asyncprerecorded.v("1").transcribe_file(payload, options)
    print("Transcript:", response.results.channels[0].alternatives[0].transcript)

asyncio.run(main())
