import os
import logging
from typing import Optional
from videosdk.agents import Agent, AgentSession, Pipeline, JobContext
from videosdk.agents.plugins import (
    OpenAIRealtime,
    OpenAIRealtimeConfig,
    OpenAISTT,
    OpenAILLM,
    OpenAITTS,
    SileroVAD,
    GeminiRealtime,
    GeminiLiveConfig,
    GoogleSTT,
    GoogleLLM,
    GoogleTTS,
    SarvamAISTT,
    SarvamAILLM,
    SarvamAITTS,
    DeepgramSTT,
    AnthropicLLM,
    ElevenLabsTTS
)

from .types import VoiceAgentConfig, AgentSessionInfo
from .repository import VoiceAgentRepository

logger = logging.getLogger(__name__)

class VideoSDKVoiceAgent(Agent):
    def __init__(self, instructions: str):
        super().__init__(instructions=instructions)

    async def on_enter(self) -> None:
        await self.session.say("Hello, I am your voice assistant. How can I help you today?")


class VoiceAgentService:
    def __init__(self, repository: VoiceAgentRepository):
        self.repository = repository

    async def start_agent_session(self, config: VoiceAgentConfig, ctx: JobContext) -> AgentSessionInfo:
        try:
            openai_key = config.openai_api_key or os.getenv("OPENAI_API_KEY", "")
            google_key = config.google_api_key or os.getenv("GOOGLE_API_KEY", "")
            sarvam_key = config.sarvam_api_key or os.getenv("SARVAM_API_KEY", "")
            deepgram_key = config.deepgram_api_key or os.getenv("DEEPGRAM_API_KEY", "")
            elevenlabs_key = config.elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY", "")
            anthropic_key = config.anthropic_api_key or os.getenv("ANTHROPIC_API_KEY", "")

            if config.pipeline_mode == "google_realtime":
                gemini_config = GeminiLiveConfig(
                    api_key=google_key,
                    model="gemini-2.0-flash-exp"
                )
                model = GeminiRealtime(config=gemini_config)
                pipeline = Pipeline(llm=model)

            elif config.pipeline_mode == "google_cascade":
                stt = GoogleSTT(api_key=google_key)
                llm = GoogleLLM(api_key=google_key, instructions=config.instructions)
                tts = GoogleTTS(api_key=google_key)
                pipeline = Pipeline(
                    stt=stt,
                    llm=llm,
                    tts=tts,
                    vad=SileroVAD()
                )

            elif config.pipeline_mode == "sarvam_cascade":
                stt = SarvamAISTT(api_key=sarvam_key)
                llm = SarvamAILLM(api_key=sarvam_key, instructions=config.instructions)
                tts = SarvamAITTS(api_key=sarvam_key)
                pipeline = Pipeline(
                    stt=stt,
                    llm=llm,
                    tts=tts,
                    vad=SileroVAD()
                )

            elif config.pipeline_mode == "custom_cascade":
                stt = DeepgramSTT(api_key=deepgram_key)
                llm = AnthropicLLM(api_key=anthropic_key, instructions=config.instructions)
                tts = ElevenLabsTTS(api_key=elevenlabs_key)
                pipeline = Pipeline(
                    stt=stt,
                    llm=llm,
                    tts=tts,
                    vad=SileroVAD()
                )

            elif config.pipeline_mode == "cascade":
                stt = OpenAISTT(api_key=openai_key)
                llm = OpenAILLM(api_key=openai_key, model="gpt-4o-mini", instructions=config.instructions)
                tts = OpenAITTS(api_key=openai_key, voice=config.voice_name)
                pipeline = Pipeline(
                    stt=stt,
                    llm=llm,
                    tts=tts,
                    vad=SileroVAD()
                )

            else:
                model_config = OpenAIRealtimeConfig(
                    api_key=openai_key,
                    voice=config.voice_name,
                    model=config.model_name
                )
                model = OpenAIRealtime(config=model_config)
                pipeline = Pipeline(llm=model)

            agent = VideoSDKVoiceAgent(instructions=config.instructions)
            await ctx.connect()
            session = AgentSession(agent=agent, pipeline=pipeline, context=ctx)
            await session.start()
            session_info = AgentSessionInfo(
                session_id=ctx.job_id,
                meeting_id=config.meeting_id,
                status="running"
            )
            self.repository.save_session(session_info)
            return session_info
        except Exception as e:
            session_info = AgentSessionInfo(
                session_id=ctx.job_id if hasattr(ctx, 'job_id') else "unknown",
                meeting_id=config.meeting_id,
                status="failed",
                error_message=str(e)
            )
            return session_info
