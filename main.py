from deta import Deta
from discord.ext import commands
from keep_alive import keep_alive
import os
bot = commands.Bot(command_prefix='$')

deta = Deta(os.getenv("DTOKEN"))


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def CC(ctx, arg):
    # check if useer in mentioned
    if not ctx.message.mentions:
        await ctx.send("Please mention a user")
    #     return
    # check if the user is admin
    if ctx.author.guild_permissions.administrator:
        # initialize deta Base
        db = deta.Base("points")
        # check of key exists in database
        if db.get(str(ctx.message.mentions[0].id)) == None:
            db.put({"user": str(ctx.message.mentions[0].id),
                   "points": 0, "key": str(ctx.message.mentions[0].id)})

        db.update({"points": db.util.increment(int(arg))},
                  str(ctx.message.mentions[0].id))

        # send a message to the channel
        await ctx.send("points += " + str(arg))
    else:
        await ctx.send('You are not an admin :angry:')

# send msg with the points of mentioned user


@bot.command()
async def points(ctx):
    # check ifuser in mentioned
    if not ctx.message.mentions:
        return await ctx.send("Please mention a user")
    # initialize deta Base
    db = deta.Base("points")

    if db.get(str(ctx.message.mentions[0].id)) == None:
        db.put({"user": str(ctx.message.mentions[0].id),
               "points": 0, "key": str(ctx.message.mentions[0].id)})
    # get the points of the user
    points = db.get(str(ctx.message.mentions[0].id))["points"]
    # send a message to the channel
    await ctx.send(points)
keep_alive()
bot.run(os.getenv("TOKEN"))
