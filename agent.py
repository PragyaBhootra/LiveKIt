from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent
from livekit.plugins import openai, noise_cancellation

load_dotenv()

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(instructions="You are a helpful voice AI assistant.")

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        llm=openai.realtime.RealtimeModel(voice="nova")
    )
    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options={
            "noise_cancellation": noise_cancellation.BVC()
        },
    )
    await ctx.connect()
    await session.generate_reply("Hello! How can I help you today?")

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
