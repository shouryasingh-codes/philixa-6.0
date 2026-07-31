import asyncio
from datetime import date
from app.ai.provider import get_ai_provider

async def test():
    provider = get_ai_provider("groq")
    raw_notes = "Mr. Sanjay se aaj unke naye godown par meeting hui. Unka business kaafi expand ho raha hai aur unhe naye machineries ke liye lagbhag 3 Crore ka term loan chahiye. Sabse pehle, unhone mujhse kaha ki main loan processing ki sari formalities clear kar du. Maine unhe assure kiya ki main unko loan documentation ki puri checklist aaj shaam tak WhatsApp kar dunga. Dusri baat, unka ek business current account kisi aur bank branch me hai jise wo hamari branch me shift karna chahte hain. Unhone request ki hai ki main account transfer ka ek blank form unhe aaj dopehar tak email kar du taaki wo sign kar sakein. Teesra, unhe ek naya credit card chahiye jisme achhi travel benefits ho. Main unke CA se baat karke unki ITR details aaj raat tak collect kar lunga taaki card process ho sake. Akhir me, unki ek choti si complaint thi ki unka mobile banking app theek se login nahi ho raha hai. Maine unhe bola hai ki main backend team se ek technical ticket raise karke uska resolution status unhe aaj 5 baje tak confirm kar dunga."
    result = provider.extract_meeting_intelligence(raw_notes, date(2026, 7, 31))
    print("COMMITMENTS:", len(result.payload.get("commitments", [])))
    for c in result.payload.get("commitments", []):
        print("-", c["description"])
    print("CONCERNS:", len(result.payload.get("concerns", [])))
    for c in result.payload.get("concerns", []):
        print("-", c["description"])

if __name__ == "__main__":
    asyncio.run(test())
