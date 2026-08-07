import asyncio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions
import os

async def main():
    deepgram = DeepgramClient(api_key="4c19be06ceeadd28ffdd477106bc50c40191a845")
    dg_connection = deepgram.listen.asynclive.v("1")

    def on_message(self_conn, result, **kwargs):
        print(f"Result: {result}")

    dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

    options = LiveOptions(
        encoding="linear16",
        channels=1,
        sample_rate=16000,
        interim_results=False
    )
    success = await dg_connection.start(options)
    print("Started:", success)
    
    await dg_connection.send(b"\x00" * 32000) 
    print("Sent. Now finishing immediately...")
    await dg_connection.finish()
    print("Finished connection. Now sleeping 1s...")
    await asyncio.sleep(1)
    print("Done")

asyncio.run(main())
