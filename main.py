import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

potato_counter = 0

def generate_potato_message(counter):
    actions_gain = [
        "dug out", "discovered", "found", "harvested", "collected", "unearthed", "stumbled upon",
        "gathered", "extracted", "secured", "happened upon", "rescued"
    ]
    actions_loss = [
        "lost", "sacrificed", "gave away", "misplaced", "spoiled", "paid as tax", "dropped",
        "let rot", "accidentally discarded", "traded away"
    ]
    results_gain = [
        "a small potato", "a handful of potatoes", "a large potato", "an entire sack of potatoes",
        "a potato treasure chest", "a rare golden potato", "a mysterious bag of potatoes",
        "an abandoned potato cart", "a tiny potato plant"
    ]
    results_loss = [
        "a sack of potatoes", "a small bag of potatoes", "a collection of potatoes", "several potatoes",
        "half a potato harvest", "a precious golden potato", "a spoiled potato plant",
        "an old crate of potatoes"
    ]

    is_loss = random.choices([True, False], weights=[15, 85], k=1)[0]

    amount_category = random.choices([
        (0, 5), (6, 25), (26, 100), (101, 250)
    ], weights=[70, 20, 7.5, 2.5], k=1)[0]
    amount = random.randint(*amount_category)

    if is_loss:
        counter -= amount
        action = random.choice(actions_loss)
        result = random.choice(results_loss)
        message = f"Unfortunately, {action} {result}, losing {amount} potatoes. Total is now {counter}."
    else:
        counter += amount
        action = random.choice(actions_gain)
        result = random.choice(results_gain)
        message = f"You {action} {result}, gaining {amount} potatoes! Total is now {counter}."

    return message, counter

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")

@bot.event
async def on_message(message):
    global potato_counter

    if message.author == bot.user:
        return

    if random.random() < 0.05:
        reply, potato_counter = generate_potato_message(potato_counter)
        await message.reply(reply)

    await bot.process_commands(message)

@bot.command()
async def reset_counter(ctx):
    global potato_counter
    potato_counter = 0
    await ctx.send("The potato counter has been reset to 0!")

@bot.command()
async def add_potatoes(ctx, amount: int):
    global potato_counter
    potato_counter += amount
    await ctx.send(f"Added {amount} potatoes. Total is now {potato_counter}.")

@bot.command()
async def subtract_potatoes(ctx, amount: int):
    global potato_counter
    potato_counter -= amount
    await ctx.send(f"Subtracted {amount} potatoes. Total is now {potato_counter}.")

@bot.command()
async def set_potatoes(ctx, amount: int):
    global potato_counter
    potato_counter = amount
    await ctx.send(f"Set the potato counter to {potato_counter}.")


bot.run(str(os.getenv("DISCORD_TOKEN")))