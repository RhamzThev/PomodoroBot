import hikari
import lightbulb
import secret
import time
import threading
import logging
from enum import Enum

S_TO_MS = 1000

class PomoStatus(Enum):
    POMODORO = 25 * 60
    SHORT_BREAK = 5 * 60
    LONG_BREAK = 15 * 60


class Status(Enum):
    RUNNING = 1
    PAUSED = 2
    STOPPED = 3

my_intents = hikari.Intents.GUILDS

bot = lightbulb.BotApp(
    token=secret.Secret.TOKEN,
    intents=my_intents,
    default_enabled_guilds=[995023091065426011]
)

class Timer:
    def __init__(self) -> None:
        self.status = Status.STOPPED
        self.pomo_status = PomoStatus.POMODORO
        self.timer = PomoStatus.POMODORO

    def countdown(self):
        while self.timer > 0:
            time.sleep(1)
            self.timer -= 1
            logging.info("There is %d second(s) remaining.", self.timer)

    def time_remaining(self):
        return self.timer

status = Status.STOPPED
timer = PomoStatus.POMODORO

# START/STOP COMMAND
@bot.command
@lightbulb.command("start", "Starts the pomodoro timer.")
@lightbulb.implements(lightbulb.SlashCommand)

async def start_timer(ctx: lightbulb.Context) -> None:
    global status
    match status:
        case Status.RUNNING:
            await ctx.respond("You can't start the timer when it's running.")
        case Status.PAUSED:
            await ctx.respond("You can't start the timer when it's paused. I think `/resume` is what you're looking for.")
        case Status.STOPPED:
            status = Status.RUNNING
            await ctx.respond("Timer has started!")

@bot.command
@lightbulb.command("stop", "Stops the pomodoro timer.")
@lightbulb.implements(lightbulb.SlashCommand)

async def Stop_timer(ctx: lightbulb.Context) -> None:
    global status
    match status:
        case Status.STOPPED:
            await ctx.respond("You can't stop a stopped timer.")
        case _:
            status = Status.STOPPED
            await ctx.respond("Timer has been stopped.")

# PAUSE/RESUME COMMAND
@bot.command
@lightbulb.command("resume", "Resumes the timer when paused.")
@lightbulb.implements(lightbulb.SlashCommand)

async def resume_timer(ctx: lightbulb.Context) -> None:
    global status
    match status:
        case Status.RUNNING:
            await ctx.respond("Timer is already running.")
        case Status.PAUSED:
            status = Status.RUNNING
            await ctx.respond("Timer has resumed.")
        case Status.STOPPED:
            await ctx.respond("You can't resume when it's stopped. I think `/start` is what you're looking for.")

@bot.command
@lightbulb.command("pause", "Pauses the timer when running.")
@lightbulb.implements(lightbulb.SlashCommand)

async def pause_timer(ctx: lightbulb.Context) -> None:
    global status
    match status:
        case Status.RUNNING:
            status = Status.PAUSED
            await ctx.respond("Timer is paused.")
        case Status.PAUSED:
            await ctx.respond("Time is already paused.")
        case Status.STOPPED:
            await ctx.respond("You can't pause a stopped timer.")

# COMMAND TO KNOW TIME REMAINING
@bot.command
@lightbulb.command("time", "Displays time remaining when counting.")
@lightbulb.implements(lightbulb.SlashCommand)

async def time_remaining(ctx: lightbulb.Context) -> None:
    global status
    match status:
        case Status.RUNNING:
            await ctx.respond("You can't start the timer when it's running.")
        case Status.PAUSED:
            await ctx.respond("You can't start the timer when it's paused. I think `/resume` is what you're looking for.")
        case Status.STOPPED:
            status = Status.RUNNING
            await ctx.respond("Timer has started!")

# NOTIFICATIONS FOR TIME INTERVALS

if __name__ == "__main__": bot.run()