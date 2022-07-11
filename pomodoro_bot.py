import hikari
import lightbulb
import secret
import time
from enum import Enum

my_intents = hikari.Intents.GUILDS

bot = lightbulb.BotApp(
    token=secret.Secret.TOKEN,
    intents=my_intents,
    default_enabled_guilds=[995023091065426011]
)

class Status(Enum):
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3

status = Status.STOPPED

# START/END COMMAND
@bot.command
@lightbulb.command("start", "Starts the pomodoro timer.")
@lightbulb.implements(lightbulb.SlashCommand)

async def start_timer(ctx: lightbulb.Context) -> None:
    # match status:
    #     case Status.RUNNING:
    #     case Status.PAUSED:
    #     case Status.STOPPED:

    if status == Status.STOPPED:
        await ctx.respond("Timer has started!")
    else:
        await ctx.respond("You can't start the timer when")

@bot.command
@lightbulb.command("end", "Ends the pomodoro timer.")
@lightbulb.implements(lightbulb.SlashCommand)

async def end_timer(ctx: lightbulb.Context) -> None:
    await ctx.respond("Timer has ended.")

# PAUSE/RESUME COMMAND
@bot.command
@lightbulb.command("resume", "Resumes the timer when paused.")
@lightbulb.implements(lightbulb.SlashCommand)

async def resume_timer(ctx: lightbulb.Context) -> None:
    await ctx.respond("Timer has resumed!")

@bot.command
@lightbulb.command("pause", "Pauses the timer when running.")
@lightbulb.implements(lightbulb.SlashCommand)

async def pause_timer(ctx: lightbulb.Context) -> None:
    await ctx.respond("Timer has paused.")

# COMMAND TO KNOW TIME REMAINING
@bot.command
@lightbulb.command("time", "Displays time remaining when counting.")
@lightbulb.implements(lightbulb.SlashCommand)

async def time_remaining(ctx: lightbulb.Context) -> None:
    await ctx.respond("There is [TBD] time left.")

# NOTIFICATIONS FOR TIME INTERVALS


if __name__ == "__main__": bot.run()