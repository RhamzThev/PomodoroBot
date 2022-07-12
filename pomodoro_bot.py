import hikari
import lightbulb
import secret
import time
from threading import Thread, Event
import logging
from enum import Enum

S_TO_MS = 1000

class PomoStatus(Enum):
    SHORT_BREAK = 5
    LONG_BREAK = 15
    POMODORO = 25


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
        self.timer = PomoStatus.POMODORO.value
        self.round = 1

        self.thread = None
        self.event = Event()

    def get_status(self):
        return self.status

    def get_timer(self):
        return self.timer

    # BUSINESS FUNCTIONS
    def start(self):
        logging.info("Timer started.")

        self.status = Status.RUNNING

        self.thread = Thread(target=self._countdown)

        self.event.set()
        self.thread.start()

    def stop(self):
        logging.info("Timer stopped.")
        self.status = Status.STOPPED
        self.event.clear()


    def pause(self):
        logging.info("Timer paused.")
        self.status = Status.PAUSED
        self.event.clear()

    def resume(self):
        logging.info("Timer resume.")
        self.status = Status.RUNNING
        self.event.set()

    def reset(self): pass

    def _set_time(self, pomo_status: PomoStatus):
        self.pomo_status = pomo_status
        self.timer = pomo_status.value

    def _reset_countdown(self):
        self.status = Status.STOPPED
        if self.pomo_status == PomoStatus.POMODORO:
            # THANKS AYUESHI
            if self.round % 2 == 1:
                # SET TO SHORT TIME
                self._set_time(PomoStatus.SHORT_BREAK)
                pass
            else:
                # SET TO LONG TIME
                self._set_time(PomoStatus.LONG_BREAK)
        else:
            # SET TO POMODORO
            self._set_time(PomoStatus.POMODORO)
            # INCREMENT ROUND
            self.round += 1

    def _countdown(self):
        self.event.set()
        while self.timer > 0 and self.status != Status.STOPPED:

            self.event.wait()
            logging.info("There is %d second(s) remaining.", self.timer)
            time.sleep(1)
            self.timer -= 1
        self._reset_countdown()
        

timer = Timer()

# START/STOP COMMAND
@bot.command
@lightbulb.command("start", "Starts the pomodoro timer.")
@lightbulb.implements(lightbulb.SlashCommand)

async def start_timer(ctx: lightbulb.Context) -> None:
    global timer
    match timer.get_status():
        case Status.RUNNING:
            await ctx.respond("You can't start the timer when it's running.")
        case Status.PAUSED:
            await ctx.respond("You can't start the timer when it's paused. I think `/resume` is what you're looking for.")
        case Status.STOPPED:
            timer.start()
            await ctx.respond("Timer has started!")

@bot.command
@lightbulb.command("stop", "Stops the pomodoro timer.")
@lightbulb.implements(lightbulb.SlashCommand)

async def Stop_timer(ctx: lightbulb.Context) -> None:
    global timer
    match timer.get_status():
        case Status.STOPPED:
            await ctx.respond("You can't stop a stopped timer.")
        case _:
            timer.stop()
            await ctx.respond("Timer has been stopped.")

# PAUSE/RESUME COMMAND
@bot.command
@lightbulb.command("resume", "Resumes the timer when paused.")
@lightbulb.implements(lightbulb.SlashCommand)

async def resume_timer(ctx: lightbulb.Context) -> None:
    global timer
    match timer.get_status():
        case Status.RUNNING:
            await ctx.respond("Timer is already running.")
        case Status.PAUSED:
            timer.resume()
            await ctx.respond("Timer has resumed.")
        case Status.STOPPED:
            await ctx.respond("You can't resume when it's stopped. I think `/start` is what you're looking for.")

@bot.command
@lightbulb.command("pause", "Pauses the timer when running.")
@lightbulb.implements(lightbulb.SlashCommand)

async def pause_timer(ctx: lightbulb.Context) -> None:
    global timer
    match timer.get_status():
        case Status.RUNNING:
            timer.pause()
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
    global timer
    match timer.get_status():
        case Status.RUNNING:
            await ctx.respond(f"There is { timer.get_timer() } second(s) left.")
        case Status.PAUSED:
            await ctx.respond(f"There is { timer.get_timer() } second(s) left.")
        case Status.STOPPED:
            await ctx.respond("Timer is not running.")

@bot.command
@lightbulb.command("reset", "Resets timer.")
@lightbulb.implements(lightbulb.SlashCommand)
async def reset_timer(ctx: lightbulb.Context) -> None:
    global timer
    timer.reset()

# NOTIFICATIONS FOR TIME INTERVALS


if __name__ == "__main__":
    bot.run()