import hikari
import lightbulb
import secret

my_intents = hikari.Intents.GUILDS

bot = lightbulb.BotApp(
    token=secret.Secret.TOKEN,
    intents=my_intents,
    default_enabled_guilds=[995023091065426011]
)

# START/END COMMAND
@bot.command
@lightbulb.command("start", "Starts the pomodoro timer")
@lightbulb.implements(lightbulb.SlashCommand)

async def start_timer(ctx: lightbulb.Context) -> None:
    await ctx.respond("Timer has started!")

# COMMAND TO KNOW TIME REMAINING

# NOTIFICATIONS FOR TIME INTERVALS


if __name__ == "__main__": bot.run()