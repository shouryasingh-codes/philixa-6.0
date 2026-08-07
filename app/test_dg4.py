import asyncio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
import os

async def main():
    deepgram = DeepgramClient(api_key="4c19be06ceeadd28ffdd477106bc50c40191a845")
    dg_connection = deepgram.listen.asynclive.v("1")

    def on_message(self_conn, result, **kwargs):
        print(f"Result: {result}")
        
    def on_error(self_conn, error, **kwargs):
        print(f"Error: {error}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)
    dg_connection.on(LiveTranscriptionEvents.Error, on_error)

    options = LiveOptions(
        encoding="linear16",
        channels=1,
        sample_rate=48000,
        diarize=False,
        interim_results=False
    )
    success = await dg_connection.start(options)
    print("Started:", success)
    
    await dg_connection.send(b"\x00" * 96000) 
    await asyncio.sleep(1)
    await dg_connection.finish()
    print("Done")

asyncio.run(main())
