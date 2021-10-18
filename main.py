# Made By Leho | github.com/lehoooo | leho.dev
import json
import sys
from os.path import exists
import requests
import discord
import os
from discord.ext import commands

print("Starting")

try:
    with open("config.json", "r") as configfile:
        config = json.load(configfile)

except Exception as e:
    print("Error Loading Config " + str(e))
    sys.exit(9)

bot = commands.Bot(command_prefix='>')

rclone_config_name = config['rclone_config_name']
rclone_folder_name = config["rclone_folder_name"]

targetchannelid = config['targetchannelid']


TOKEN = config['token']

@bot.event
async def on_message(message):

    serverid = str(message.guild.id)
    channelid = str(message.channel.id)

    if channelid != targetchannelid:
        print("Not in target channel!")
    else:
        messageid = str(message.id)
        channel = str(message.channel)
        channelreply = message.channel
        attachments = message.attachments
        server = str(message.guild).replace("'", "").replace('"', "").replace(" ", "-")
        finalfolderpath = "./images/" + str(server) + "/" + str(channel)

        if not message.attachments:
            print("no attachments")
        else:
            # File detected and download
            link = attachments[0]
            if str(link).startswith("https://cdn.discordapp.com"):



                if not os.path.isdir(finalfolderpath): # yes theres probably a better way to do this but windows hates me :(
                    try:
                        os.mkdir("./images/")
                    except:
                        print("Error making first folder")
                    try:
                        os.mkdir("./images/" + str(server))
                    except:
                        print("Error making second folder")
                    try:
                        os.mkdir("./images/" + str(server) + "/" + str(channel))
                    except:
                        print("Error making third folder")
                    print("made folder")


                print("downloading file now")
                await channelreply.send("Photo detected! Starting Backup!", delete_after=5)

                file = requests.get(str(link))
                print("file downloaded")
                if file.status_code == 200:
                    open(str(finalfolderpath) + "/" + str(messageid) + ".jpg", 'wb').write(file.content)
                    print("file saved")
                    try:
                        os.system("rclone.exe copy " + str(finalfolderpath) + "/" + str(messageid) + ".jpg " + str(rclone_config_name) + ":" + str(rclone_folder_name) + "/")
                        print("Uploaded Successfully!")
                        embed = discord.Embed(title="Uploaded Successfully!")
                        embed.add_field(name="File Name:", value=str(messageid) + ".jpg/.png", inline=False)
                        embed.add_field(name="Link:", value=str(config['publiclink']), inline=False)
                        embed.set_footer(text="BackupBot | Made With 💖 By Leho")
                        await channelreply.send(embed=embed, delete_after=20)
                    except Exception as e:
                        print("Error! ", e)
                        await channelreply.send("Error! " + str(e))


                else:
                    print("Error downloading :(")
                    await channelreply.send("Error!")



            else:
                print("Link does not seem to be valid :(")
                await channelreply.send("Error!")

bot.run(TOKEN)
