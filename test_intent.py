import asyncio, json
from app.core.config import get_settings
from app.ai.provider import get_ai_provider

async def main():
    settings = get_settings()
    provider = get_ai_provider(settings.ai_economy_provider, settings)
    
    intent_schema = {
        'intent': 'string',
        'client_name': 'string'
    }
    
    res = await asyncio.to_thread(
        provider.generate_json,
        settings.ai_economy_model,
        f"User just said: 'राजेश शर्मा से मिला'.\nAnalyze the user's voice input (which might be in Hindi/Hinglish) and extract intent. If they are talking about a client meeting to save, return SAVE_MEETING and extract the client's name. If they are asking a question about a specific person, client, past discussion, or ANY portfolio metrics/data (like 'how many meetings', 'who asked for discount'), return QUERY and extract the person's name if applicable. If they want to send an email, message, or reminder to a client, return SEND_REMINDER and extract the client's name. If they say 'yes', 'send it', 'haan bhej do', 'correct' and are confirming a previous action, return CONFIRM_ACTION. If they say 'no', 'cancel', 'stop', 'mat bhej', return REJECT_ACTION. Otherwise, return GENERAL_CHAT. (TRANSLATE AND SPELL HINDI NAMES IN ENGLISH, e.g. 'मनोज' -> 'Manoj').",
        intent_schema
    )
    print(res)

asyncio.run(main())
