import asyncio
import edge_tts


class TextToSpeech:
    def speak(self, text, voice="en-GB-RyanNeural"):
        """Generates real-time audio bytes using Microsoft's JARVIS (Ryan) Voice."""
        cleaned = (text or "").strip()

        if not cleaned:
            return None

        async def _generate_stream():
            communicate = edge_tts.Communicate(cleaned, voice)
            audio_bytes = bytearray()
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    audio_bytes.extend(chunk["data"])
            return bytes(audio_bytes)

        # Run the async generator synchronously to preserve your app's architecture
        try:
            return asyncio.run(_generate_stream())
        except RuntimeError:
            loop = asyncio.get_event_loop()
            return loop.run_until_complete(_generate_stream())