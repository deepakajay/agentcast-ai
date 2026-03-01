import asyncio
import edge_tts
import os
import uuid

VOICE_A = "en-US-AvaMultilingualNeural"
VOICE_B = "en-US-AnaNeural"


async def generate_audio(dialogue):
    os.makedirs("audio", exist_ok=True)

    final_filename = f"podcast_{uuid.uuid4().hex}.mp3"
    final_path = os.path.join("audio", final_filename)

    temp_files = []

    try:
        # -------- INTRO --------
        intro_text = "Welcome to AgentCast. Let's dive into today's topic."
        intro_file = os.path.join("audio", f"temp_{uuid.uuid4().hex}.mp3")
        temp_files.append(intro_file)

        intro = edge_tts.Communicate(
            intro_text,
            VOICE_A,
            rate="-5%",
        )
        await intro.save(intro_file)

        # -------- DIALOGUE --------
        for item in dialogue:
            speaker = item["speaker"]
            text = item["text"]

            voice = VOICE_A if speaker == "A" else VOICE_B

            # Add small conversational pause
            natural_text = text + " ... "

            temp_file = os.path.join("audio", f"temp_{uuid.uuid4().hex}.mp3")
            temp_files.append(temp_file)

            tts = edge_tts.Communicate(
                natural_text,
                voice,
                rate="-3%" if speaker == "A" else "-1%",
            )
            await tts.save(temp_file)

        # -------- OUTRO --------
        outro_text = "That was today's episode. Thanks for listening. See you next time."
        outro_file = os.path.join("audio", f"temp_{uuid.uuid4().hex}.mp3")
        temp_files.append(outro_file)

        outro = edge_tts.Communicate(
            outro_text,
            VOICE_B,
            rate="-5%",
        )
        await outro.save(outro_file)

        # -------- MERGE FILES --------
        with open(final_path, "wb") as outfile:
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    with open(temp_file, "rb") as infile:
                        outfile.write(infile.read())

        return final_path

    except Exception as e:
        print("TTS ERROR:", str(e))
        raise e

    finally:
        # Clean temp files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)


def generate_audio_sync(dialogue):
    try:
        return asyncio.run(generate_audio(dialogue))
    except RuntimeError:
        # Fix for event loop already running issue
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(generate_audio(dialogue))