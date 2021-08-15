from inspect import Traceback
from time import *
import logging
from logging import INFO, error, DEBUG, exception
import asyncio
import os
import datetime
import random
import aiofiles
from sys import exc_info
import json
from colorama import Fore, Back, Style

from discord.utils import get
import discord
from discord import message
from discord import permissions
from discord import *
from discord.channel import TextChannel
from discord.ext import commands
from discord.ext.commands import MissingPermissions, has_permissions
from discord.ext.commands.core import bot_has_permissions
from discord_components.interaction import InteractionType
from discord_slash import SlashCommand
from discord_slash.model import ButtonStyle
from dotenv import load_dotenv
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_components import DiscordComponents, Button, Interaction, component
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle

default_intents = discord.Intents.default()

all_intents: discord.Intents = discord.Intents.all()

bot = commands.Bot(command_prefix="!", intents=all_intents)
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True)

image_error="https://i.ibb.co/tHWL83V/acces-denied.png"

full_date = datetime.datetime.now()
date = full_date.strftime('%Y-%m-%d-%H-%M-%S')

ddb = DiscordComponents(bot)

bot.warnings = {} # guild_id : {user_id: [count, [(author_id, raison, preuve)]]}

try:
    logging.basicConfig(filename=f"logs/{date}.log", level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s')
except FileNotFoundError:
    os.mkdir('logs')
    logging.basicConfig(filename=f"logs/{date}.log", level=logging.INFO, 
        format='%(asctime)s:%(levelname)s:%(message)s')


load_dotenv(dotenv_path="token")

Neptun_bot = """
███╗   ██╗███████╗██████╗ ████████╗██╗   ██╗███╗   ██╗
████╗  ██║██╔════╝██╔══██╗╚══██╔══╝██║   ██║████╗  ██║
██╔██╗ ██║█████╗  ██████╔╝   ██║   ██║   ██║██╔██╗ ██║
██║╚██╗██║██╔══╝  ██╔═══╝    ██║   ██║   ██║██║╚██╗██║
██║ ╚████║███████╗██║        ██║   ╚██████╔╝██║ ╚████║
╚═╝  ╚═══╝╚══════╝╚═╝        ╚═╝    ╚═════╝ ╚═╝  ╚═══╝
        """


async def check_is_config(guild: discord.Guild):
    channel_logs_is_config = None
    channel_welcome_is_config = None
    invite_link_is_config = None
    try:
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
    except json.decoder.JSONDecodeError:
        with open(f'guilds/{guild.id}/config.json', "w") as infile:
            infile.write("{}")
    try:
        data['channel_welcome']
    except:
        logging.warning(f'{guild.id} Channel_welcome is not config')
        channel_welcome_is_config = False
    try:
        data['invite_link']
    except:
        logging.warning(f'{guild.id} Invite_link is not config')
        invite_link_is_config = False
    try:
        data['channel_logs']
    except:
        logging.warning(f'{guild.id} Channel_logs is not config')
        channel_logs_is_config = False
    
    if channel_welcome_is_config is False or invite_link_is_config is False or channel_logs_is_config is False:
        return False

async def check_is_config_on_ready(guild: discord.Guild):
    channel_logs_is_config = None
    channel_welcome_is_config = None
    invite_link_is_config = None
    try:
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
    except json.decoder.JSONDecodeError:
        with open(f'guilds/{guild.id}/config.json', "w") as infile:
            infile.write("{}")
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
    except FileNotFoundError:
        try:
            os.makedirs(f'guilds/{guild.id}')
            with open(f'guilds/{guild.id}/config.json') as infile:
                data = json.load(infile)
        except FileExistsError:
            pass
        except FileNotFoundError:
            with open(f'guilds/{guild.id}/config.json', 'a') as infile:
                infile.write('{}')
        
    try:
        data['channel_welcome']
        logging.info(f'{guild.id} Channel_welcome is config')
        print(f'{Fore.GREEN}{guild.id} ✓ Channel_welcome is config{Fore.RESET}')
        channel_welcome_is_config = True
    except:
        print(f"{Fore.RED}{guild.id} ✘ Channel_welcome n'a pas été configuré{Fore.RESET}")
        logging.warning(f'{guild.id} Channel_welcome is not config')
        channel_welcome_is_config = False
    try:
        data['invite_link']
        logging.info(f'{guild.id} Invite_link is config')
        print(f'{Fore.GREEN}{guild.id} ✓ Invite_link is config{Fore.RESET}')
        invite_link_is_config = True
    except:
        print(f"{Fore.RED}{guild.id} ✘ Invite_link n'a pas été configuré{Fore.RESET}")
        logging.warning(f'{guild.id} Invite_link is not config')
        invite_link_is_config = False
    try:
        data['channel_logs']
        logging.info(f'{guild.id} Channel_logs is config')
        print(f'{Fore.GREEN}{guild.id} ✓ Channel_logs is config')
        channel_logs_is_config = True
    except:
        print(f"{Fore.RED}{guild.id} ✘ Channel_logs n'a pas été configuré{Fore.RESET}")
        logging.warning(f'{guild.id} Channel_logs is not config')
        channel_logs_is_config = False

    if channel_welcome_is_config is False or invite_link_is_config is False or channel_logs_is_config is False:
        print(Fore.RED + f"\nLe serveur {guild.id} n'est pas configuré" + Fore.RESET)
        return False

    if channel_welcome_is_config is True or invite_link_is_config is True or channel_logs_is_config is True:
        print(Fore.GREEN + f"\nLe serveur {guild.id} est configuré" + Fore.RESET)
        return True
    

async def sanctions_files():
    for guild in bot.guilds:
        bot.warnings[guild.id] = {}
        
        try:
            async with aiofiles.open(f"guilds/{guild.id}/sanctions.txt", mode="a") as temp:
                pass
        except FileNotFoundError:
            os.makedirs(f"guilds/{guild.id}/")
            async with aiofiles.open(f"guilds/{guild.id}/sanctions.txt", mode="a") as temp:
                pass

        async with aiofiles.open(f"guilds/{guild.id}/sanctions.txt", mode="r") as file:
            lines = await file.readlines()

            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                sanction_id = int(data[2])
                reason = " ".join(data[3:]).strip("\n")

                try:
                    bot.warnings[guild.id][member_id][0] += 1
                    bot.warnings[guild.id][member_id][1].append((admin_id, sanction_id, reason))

                except KeyError:
                    bot.warnings[guild.id][member_id] = [1, [(admin_id, sanction_id, reason)]]

def get_color(color1, color2, color3):
    rand_numb = random.randint(1, 3)
    if rand_numb == 1:
        return color1
    elif rand_numb == 2:
        return color2
    elif rand_numb == 3:
        return color3

@bot.event
async def on_ready():
    print(Fore.CYAN + Neptun_bot + Fore.RESET)
    for guild in bot.guilds:
        print()
        print(Fore.CYAN + 'The bot is on the server : ' + guild.name + Fore.RESET)
        try:
            with open(f"guilds/{guild.id}/config.json", "r") as file:
                content = file.read()
        except FileNotFoundError:
            logging.warning(f"Le serveur {guild.id} n'est pas configuré")
            try:
                file = open(f"guilds/{guild.id}/config.json", "a")
            except FileNotFoundError:
                try:
                    os.mkdir(f"guilds/")
                    file = open(f"guilds/{guild.id}/config.json", "a")
                except FileNotFoundError:
                    try:
                        os.makedirs(f"guilds/{guild.id}/")
                        file = open(f"guilds/{guild.id}/config.json", "a")
                    except FileExistsError:
                        pass
                except FileExistsError:
                    pass
        except json.decoder.JSONDecodeError:
            file.write("{}")
        await check_is_config_on_ready(guild)
           
        try:
            await sanctions_files()
        except:
            pass

    logging.info("Bot pret !")


@bot.event
@bot_has_permissions(send_messages=True, read_messages=True, view_channel=True)
async def on_member_join(member: discord.Member):
    guild: discord.Guild = await bot.fetch_guild(member.guild.id)
    logging.info(f"{member} as join the discord")
    color = get_color(0x00ff4c, 0x00f7ff, 0xeb3495)
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    try:
        channel:TextChannel = await bot.fetch_channel(data['channel_welcome'])
    except:
        owner = await bot.fetch_user(guild.owner_id)
        await owner.send(embed=discord.Embed(
            title="Erreur", 
            description=f":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server`` sur votre discord **{guild.name}**", 
            color=get_color(0xf54531, 0xf57231, 0xf53145)))
    embed=discord.Embed(title="Bienvenue", description=f"{member.mention}, bienvenue sur le serveur **{guild.name}** !", color=color)
    embed.set_author(name="Neptun", icon_url=bot.user.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    await channel.send(embed=embed)


@slash.slash(name="clear", description="Effacer des messages", options=[
                create_option(
                    name="nombre",
                    description="Indiquer le nombre de message à clear",
                    option_type=4,
                    required=False),
             ])
@has_permissions(manage_messages=True)
@bot_has_permissions(send_messages=True, read_messages=True, manage_messages=True)
async def clear(ctx, *, nombre: int=None):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    if await check_is_config(guild=ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    color = get_color(0xfff04f, 0x554fff, 0xff6eff)
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    if nombre == None:
       await ctx.channel.purge(limit=1000000)
       nombre="Tout"
    else:
       await ctx.channel.purge(limit=nombre)
    embed = discord.Embed(title=f"Le channel {ctx.channel} a été clear !", color=color)
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed.add_field(name="Nombre de messages supprimés", value=nombre, inline=False)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    await channel_logs.send(embed=embed)
    await ctx.send(embed=discord.Embed(description=f"Le channel **{ctx.channel}** a été clear :white_check_mark:", color=0x34eb37), hidden=True)
    logging.info(f"{ctx.author} a clear {nombre} messages dans le channel {ctx.channel}")


@slash.slash(name="ban", description="Bannir un membre définitivement", options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être ban",
                    option_type=6,
                    required=True),
                create_option(
                    name="raison",
                    description="Indiquer la raison du ban",
                    option_type=3,
                    required=False),
             ])
@has_permissions(ban_members=True)
@bot_has_permissions(send_messages=True, read_messages=True, ban_members=True)
async def ban(ctx, user: discord.User, *, raison="Aucune raison fournie"):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    try:
        bot.warnings[ctx.guild.id][user.id][0] += 1
        bot.warnings[ctx.guild.id][user.id][1].append((ctx.author.id, 1,raison))
    except KeyError:
        bot.warnings[ctx.guild.id][user.id] = [1, [(ctx.author.id, 1,raison)]]
    async with aiofiles.open(f"{ctx.guild.id}/sanctions.txt", mode="a") as file:
        await file.write(f"{user.id} {ctx.author.id} 1 {raison}\n")
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    embed = discord.Embed(title=f"{user.name} a été **ban** !",
                          description="Cet utilisateur n'a pas respecté les règles du serveur !", color=0xcc0202)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
    embed.add_field(name="Raison", value=raison, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    embed_user = discord.Embed(title="Vous avez été banni !",
                               description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                           "Si la raison de votre bannissement vous semble incorrecte, "
                                           "vous pouvez contacter le modérateur qui vous a banni !", color=0xcc0202)
    embed_user.set_thumbnail(url=ctx.author.avatar_url)
    embed_user.add_field(name="Raison", value=raison, inline=True)
    embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
    await user.send(embed=embed_user)
    await ctx.guild.ban(user, reason=raison)
    logging.info(f"{ctx.author} a banni {user}, raison : {raison}") 
    await channel_logs.send(embed=embed)
    await ctx.send(embed=discord.Embed(description=f"Vous avez banni **{user}** :white_check_mark:", color=0x34eb37), hidden=True)


@slash.slash(name="kick", description="Exclure un membre", options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être kick",
                    option_type=6,
                    required=True),
                create_option(
                    name="reason",
                    description="Indiquer la raison du kick",
                    option_type=3,
                    required=False),
             ])
@has_permissions(kick_members=True)
@bot_has_permissions(send_messages=True, read_messages=True, kick_members=True)
async def kick(ctx, user: discord.User, *, reason="Aucune raison fournie"):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    try:
        bot.warnings[ctx.guild.id][user.id][0] += 1
        bot.warnings[ctx.guild.id][user.id][1].append((ctx.author.id, 3,reason))
    except KeyError:
        bot.warnings[ctx.guild.id][user.id] = [1, [(ctx.author.id, 3,reason)]]
    
    async with aiofiles.open(f"{ctx.guild.id}/sanctions.txt", mode="a") as file:
        await file.write(f"{user.id} {ctx.author.id} 3 {reason} Warn\n")
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    embed = discord.Embed(title=f"{user.name} a été **kick** !",
                          description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=0xa8324e)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Utilisateur kick", value=user.mention, inline=True)
    embed.add_field(name="Raison", value=reason, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    embed_user = discord.Embed(title="Vous avez été kick !",
                               description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                           "Si la raison de votre kick vous semble incorrecte, "
                                           "vous pouvez contacter le modérateur qui vous a kick"
                                           "vous pouvez revenir sur le serveur via le lien ci-dessous.", color=0xa8324e)
    embed_user.set_thumbnail(url=ctx.author.avatar_url)
    embed_user.add_field(name="Raison", value=reason, inline=True)
    embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed_user.add_field(name="Discord", value=data['invite_link'], inline=True)
    await user.send(embed=embed_user)
    await ctx.guild.kick(user, reason=reason)
    await channel_logs.send(embed=embed)
    await ctx.send(embed=discord.Embed(description=f"Vous avez kick **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    

@slash.slash(name="unban", description="dé-bannir un membre", options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être unban, sous cette forme exemple ``user#1234``",
                    option_type=3,
                    required=True),
                create_option(
                    name="raison",
                    description="Indiquer la raison de l'unban",
                    option_type=3,
                    required=False),
             ])
@has_permissions(ban_members=True)
@bot_has_permissions(send_messages=True, read_messages=True, manage_guild=True)
async def unban(ctx, user, *, raison="Aucune raison fournie"):
    await ctx.defer(hidden=True)
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    color = get_color(0x32a852, 0x5eff8a, 0x3fc463)
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    user_base = user
    banned_users = await ctx.guild.bans()
    try:
        user_name, user_discriminator = user.split('#')
    except ValueError:
        exc_type, value, traceback = exc_info()
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: L'option {user} doit être sous la forme suivante : ``user#1234``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé la commande '/unban {user}', ValueError: {value}")
    unban_logs = discord.Embed(title=f"**{user}** a été dé-banni", color=color)
    unban_logs.set_thumbnail(url=ctx.author.avatar_url)
    unban_logs.add_field(name="Raison", value=raison, inline=True)
    unban_logs.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    unban_logs.set_footer(text=f"Date • {datetime.datetime.now()}")
    async def is_banned():
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (user_name, user_discriminator):
                await ctx.guild.unban(user, reason=raison)
                await channel_logs.send(embed=unban_logs)
                await ctx.send(embed=discord.Embed(description=f"Vous avez dé-banni **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
                logging.info(f"{ctx.author} a dé-banni {user}, raison : {raison}")
                return True
    if await is_banned() != True:    
        await ctx.send(embed=discord.Embed(description=f":warning: Aucun membre banni ne correspond à : **{user_base}** :negative_squared_cross_mark: Faites **/ban_list** pour voir la liste des membres bannis."
        , color=get_color(0xf54531, 0xf57231, 0xf53145)), hidden=True)
        logging.warning(f"{ctx.author} a utilisé la commande '/unban {user_base}', Aucun membre correspondant à : {user_base}")


@slash.slash(name="ban_list", description="Permet d'obtenir la liste des membres bannis")
@has_permissions(ban_members=True)
@bot_has_permissions(send_messages=True, read_messages=True, manage_guild=True)
async def ban_list(ctx):
    await ctx.defer(hidden=True)
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    color = get_color(0xc43f3f, 0xc45e3f, 0xc43f72)
    guild: discord.Guild=ctx.guild
    banned_users_list = await guild.bans()
    if len(banned_users_list) == 0:
        embed=discord.Embed(title="Aucun membre n'est banni sur le serveur", color=color)
    else:
        embed = discord.Embed(title="Voici la liste des membres bannis du discord", color=color)
        for banned_users in banned_users_list:
            embed.add_field(name=f"{banned_users.user.name}#{banned_users.user.discriminator}",
            value=f"Raison du ban : **{banned_users.reason}**, ID : **{banned_users.user.id}**",
            inline=False)
    await ctx.send(embed=embed, hidden=True)
    logging.info(f"{ctx.author} a utilisé la commande /ban_list")

@slash.slash(name="tempban", description="Bannir temporairement un membre", options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être ban",
                    option_type=6,
                    required=True),
                create_option(
                    name="duration",
                    description="Cette option doit être un nombre",
                    option_type=4,
                    required=True),
                create_option(
                    name="time",
                    description="seconde / minute / heure / mois",
                    option_type=3,
                    required=True,
                    choices=[
                 create_choice(
                    name="seconde",
                    value="s"
                  ),
                create_choice(
                    name="minute",
                    value="m"
                  ),
                create_choice(
                    name="heure",
                    value="h"
                  ),
                create_choice(
                    name="jour",
                    value="j"
                  ),
                create_choice(
                    name="mois",
                    value="mois"),
                ]),
                create_option(
                    name="raison",
                    description="Indiquer la raison du ban",
                    option_type=3,
                    required=False),
             ])
@has_permissions(ban_members=True)
@bot_has_permissions(send_messages=True, read_messages=True, ban_members=True)
async def tempban(ctx, user: discord.User, duration: int, time: str, *, raison="Aucune raison fournie"):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    try:
        bot.warnings[ctx.guild.id][user.id][0] += 1
        bot.warnings[ctx.guild.id][user.id][1].append((ctx.author.id, 4,raison))
    except KeyError:
        bot.warnings[ctx.guild.id][user.id] = [1, [(ctx.author.id, 4,raison)]]

    
    color = get_color(0xd459d9, 0x5973d9, 0xd95959)
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    author = ctx.author
    if "s" == time:
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} seconde(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed.set_thumbnail(url=user.avatar_url)
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni."
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=color)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} seconde(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        embed_user.add_field(name="Discord", value=data['invite_link'], inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=raison)
        logging.info(f"{ctx.author} a banni temporairement {user} : {duration} {time}, raison : {raison}")
        await ctx.send(embed=discord.Embed(description=f"Vous avez banni temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await asyncio.sleep(duration)
        await ctx.guild.unban(user)
    elif "m" == time:
        duration_min = duration * 60
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} minute(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni."
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=color)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} minute(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        embed_user.add_field(name="Discord", value=data['invite_link'], inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=raison)
        logging.info(f"{ctx.author} a banni temporairement {user} : {duration} {time}, raison : {raison}")
        await ctx.send(embed=discord.Embed(description=f"Vous avez banni temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await asyncio.sleep(duration_min)
        await ctx.guild.unban(user)
    elif "h" == time:
        duration_heure = duration * 3600
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} heure(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni."
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=color)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} heure(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        embed_user.add_field(name="Discord", value=data['invite_link'], inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=raison)
        logging.info(f"{ctx.author} a banni temporairement {user} : {duration} {time}, raison : {raison}")
        await ctx.send(embed=discord.Embed(description=f"Vous avez banni temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await asyncio.sleep(duration_heure)
        await ctx.guild.unban(user)
    elif "j" == time:
        duration_jour = duration * 86400
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} jour(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni."
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=color)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} jour(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        embed_user.add_field(name="Discord", value=data['invite_link'], inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=raison)
        logging.info(f"{ctx.author} a banni temporairement {user} : {duration} {time}, raison : {raison}")
        await ctx.send(embed=discord.Embed(description=f"Vous avez banni temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await asyncio.sleep(duration_jour)
        await ctx.guild.unban(user)
    elif "mois" == duration:
        duration_mois = duration * 86400 * 30
        embed = discord.Embed(title=f"{user.name} a été **ban temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Utilisateur banni", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} mois", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user = discord.Embed(title="Vous avez été banni temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre ban vous semble incorrecte, "
                                               "vous pouvez contacter le modérateur qui vous a banni. "
                                               "**Vous pourrez revenir sur le serveur via le lien ci-dessous une fois que votre ban "
                                               "sera terminé.**",
                                   color=color)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} mois", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        embed_user.add_field(name="Discord", value=data['invite_link'], inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        await user.send(embed=embed_user)
        await ctx.guild.ban(user, reason=raison)
        logging.info(f"{ctx.author} a banni temporairement {user} : {duration} {time}, raison : {raison}")
        await ctx.send(embed=discord.Embed(description=f"Vous avez banni temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await asyncio.sleep(duration_mois)
        await ctx.guild.unban(user)
    else:
        author = ctx.author
        embed = discord.Embed(title="Valeur de l'argument **[temps]** est inconnue",
                              description=f"{author.mention} L'argument [temps] doit être : **[s, m, j, mois]**", color=0xf09400)
        embed.set_thumbnail(url=image_error)
        embed.add_field(name="s", value="seconde(s)", inline=True)
        embed.add_field(name="h", value="heure(s)", inline=True)
        embed.add_field(name="j", value="jour(s)", inline=True)
        embed.add_field(name="mois", value="mois", inline=True)
        await ctx.send(embed=embed, hidden=True)
    async with aiofiles.open(f"{ctx.guild.id}/sanctions.txt", mode="a") as file:
        await file.write(f"{user.id} {ctx.author.id} 4 {raison}\n")


async def createRoleMute(ctx):
    role_mute = await ctx.guild.create_role(name = "mute",
                                            permissions= discord.Permissions(send_messages= False, speak= False))
    for channel in ctx.guild.channels:
        await channel.set_permissions(role_mute, send_messages=False, speak= False)


async def getRoleMute(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "mute":
            return role

    return await createRoleMute(ctx)


@slash.slash(name="tempmute", description="Rendre muet temporairement un membre", options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être mute",
                    option_type=6,
                    required=True),
                create_option(
                    name="duration",
                    description="Cette option doit être un nombre",
                    option_type=4,
                    required=True),
                create_option(
                    name="time",
                    description="seconde / minute / heure / mois",
                    option_type=3,
                    required=True,
                    choices=[
                 create_choice(
                    name="seconde",
                    value="s"
                  ),
                create_choice(
                    name="minute",
                    value="m"
                  ),
                create_choice(
                    name="heure",
                    value="h"
                  ),
                create_choice(
                    name="jour",
                    value="j"
                  ),
                create_choice(
                    name="mois",
                    value="mois"),
                ]),
                create_option(
                    name="raison",
                    description="Indiquer la raison du mute",
                    option_type=3,
                    required=False),
             ])
@has_permissions(manage_roles=True)
@bot_has_permissions(send_messages=True, read_messages=True, manage_roles=True)
async def tempmute(ctx, user: discord.User, duration: int, time: str, *, raison="Aucune raison fournie"):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    try:
        bot.warnings[ctx.guild.id][user.id][0] += 1
        bot.warnings[ctx.guild.id][user.id][1].append((ctx.author.id, 2,raison))
    except KeyError:
        bot.warnings[ctx.guild.id][user.id] = [1, [(ctx.author.id, 2,raison)]]

    async with aiofiles.open(f"{ctx.guild.id}/sanctions.txt", mode="a") as file:
        await file.write(f"{user.id} {ctx.author.id} 2 {raison}\n")
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    role_mute = await getRoleMute(ctx)
    author = ctx.author
    color = get_color(0xedda5f, 0xedab5f, 0xbb76f5)
    if "s" == time:
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} seconde(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed.set_thumbnail(url=user.avatar_url)
        embed_user = discord.Embed(title="Vous avez été mute temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=color)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de mute", value=f"{duration} seconde(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user.set_thumbnail(url=ctx.author.avatar_url)
        await user.add_roles(role_mute, reason=raison)
        await ctx.send(embed=discord.Embed(description=f"Vous avez mute temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await user.send(embed=embed_user)
        await asyncio.sleep(duration)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
        logging.info(f"{ctx.author} a mute temporairement {user} : {duration} {time}, raison : {raison}")
    elif "m" == time:
        duration_min = duration * 60
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} minute(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user = discord.Embed(title="Vous avez été mute temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=color)
        embed_user.set_thumbnail(url=ctx.author.avatar_url)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de mute", value=f"{duration} minute(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        await user.add_roles(role_mute, reason=raison)
        await ctx.send(embed=discord.Embed(description=f"Vous avez mute temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await user.send(embed=embed_user)
        await asyncio.sleep(duration_min)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
        logging.info(f"{ctx.author} a mute temporairement {user} : {duration} {time}, raison : {raison}")
    elif "h" == time:
        duration_heure = duration * 3600
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} heure(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user = discord.Embed(title="Vous avez été mute temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=color)
        embed_user.set_thumbnail(url=ctx.author.avatar_url)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de banissement", value=f"{duration} heure(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        await user.add_roles(role_mute, reason=raison)
        await ctx.send(embed=discord.Embed(description=f"Vous avez mute temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await user.send(embed=embed_user)
        await asyncio.sleep(duration_heure)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
        logging.info(f"{ctx.author} a mute temporairement {user} : {duration} {time}, raison : {raison}")
    elif "j" == time:
        duration_jour = duration * 86400
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} jour(s)", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user = discord.Embed(title="Vous avez été mute temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=color)
        embed_user.set_thumbnail(url=ctx.author.avatar_url)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de mute", value=f"{duration} jour(s)", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        await user.add_roles(role_mute, reason=raison)
        await ctx.send(embed=discord.Embed(description=f"Vous avez mute temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await user.send(embed=embed_user)
        await asyncio.sleep(duration_jour)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
        logging.info(f"{ctx.author} a mute temporairement {user} : {duration} {time}, raison : {raison}")
    elif "mois" == duration:
        duration_mois = duration * 86400 * 30
        embed = discord.Embed(title=f"{user.name} a été **mute temporairement** !",
                              description=f"Cet utilisateur n'a pas respecté les règles du serveur !", color=color)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Utilisateur mute", value=user.mention, inline=True)
        embed.add_field(name="Raison", value=raison, inline=True)
        embed.add_field(name="Durée", value=f"{duration} mois", inline=True)
        embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed_user = discord.Embed(title="Vous avez été mute temporairement !",
                                   description="Il semblerait que vous n'ayez pas respecté les règles du serveur. "
                                               "Si la raison de votre mute vous semble incorrecte, "
                                               "vous vous contacter le modérateur qui vous a mute.",
                                   color=color)
        embed_user.set_thumbnail(url=ctx.author.avatar_url)
        embed_user.add_field(name="Raison", value=raison, inline=True)
        embed_user.add_field(name="Temps de mute", value=f"{duration} mois", inline=True)
        embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
        embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
        await user.add_roles(role_mute, reason=raison)
        await ctx.send(embed=discord.Embed(description=f"Vous avez mute temporairement **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        await user.send(embed=embed_user)
        await asyncio.sleep(duration_mois)
        await user.remove_roles(role_mute, reason="Fin de la période de mute")
        logging.info(f"{ctx.author} a mute temporairement {user} : {duration} {time}, raison : {raison}")
    else:
        author = ctx.author
        embed = discord.Embed(title="Valeur de l'argument **[temps]** est inconnue",
                              description=f"{author.mention} L'argument [temps] doit être : **[s, m, j, mois]**",
                              color=0xf09400)
        embed.set_thumbnail(url=image_error)
        embed.add_field(name="s", value="seconde(s)", inline=True)
        embed.add_field(name="h", value="heure(s)", inline=True)
        embed.add_field(name="j", value="jour(s)", inline=True)
        embed.add_field(name="mois", value="mois", inline=True)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        await ctx.send(embed=embed, hidden=True)


@slash.slash(name="unmute", description="Ne plus rendre muet un membre", options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être unmute",
                    option_type=6,
                    required=True),
                create_option(
                    name="raison",
                    description="Indiquer la raison de l'unmute",
                    option_type=3,
                    required=False),
             ])
@has_permissions(manage_roles=True)
@bot_has_permissions(send_messages=True, read_messages=True, manage_roles=True)
async def unmute(ctx, user: discord.User, *, raison="Aucune raison fournie"):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    embed = discord.Embed(title=f"{user} été dé-mute !",
                              description="Il peut maintenant re-parler dans le chat !",
                              color=0x42f557)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Raison", value=raison, inline=True)
    embed.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    embed_user = discord.Embed(title="Vous avez été dé-mute !",
                               description="Vous pouvez maintenant re-parler dans le chat !",
                               color=0x42f557)
    embed_user.set_thumbnail(url=ctx.author.avatar_url)
    embed_user.add_field(name="Raison", value=raison, inline=True)
    embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    role_mute = await getRoleMute(ctx)
    if role_mute in user.roles:
        await user.remove_roles(role_mute, reason=raison)
        await user.send(embed=embed_user)
        await ctx.send(embed=discord.Embed(description=f"Vous avez dé-mute **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
        await channel_logs.send(embed=embed)
        logging.info(f"{ctx.author} a unmute {user}, raison : {raison}")
    else:
        await ctx.send(embed=discord.Embed(description=f":warning: **{user}** n'est pas mute :negative_squared_cross_mark:"
            , color=get_color(0xf54531, 0xf57231, 0xf53145)), hidden=True)
        logging.warning(f"{ctx.author} a utilisé la commande '/unmute {user}', ce membre n'est pas mute")
    


@slash.slash(name="report", description="Report un membre", permissions="",     options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être report",
                    option_type=6,
                    required=True),
                create_option(
                    name="raison",
                    description="Indiquer la raison du report",
                    option_type=3,
                    required=True),
                create_option(
                    name="preuve",
                    description="Indiquer une preuve",
                    option_type=3,
                    required=False),
             ])
async def report(ctx, user: discord.User, raison, *, preuve="Aucune preuve fournie"):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    color = get_color(0x34ebe5, 0x2f5da, 0x42f575)
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs = await bot.fetch_channel(data['channel_logs'])
    embed = discord.Embed(title=f"{ctx.author} a report {user}", color=color)
    embed.add_field(name="Raison", value=raison, inline=True)
    embed.add_field(name="Preuve", value=preuve, inline=True)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    if preuve != "Aucune preuve fournie":
        if preuve.endswith(".png") or preuve.endswith(".jpg") or preuve.endswith(".gif"):
            embed.set_thumbnail(url=preuve)
        else:
            pass
    else:
            pass
    await channel_logs.send(embed=embed)
    logging.info(f"{ctx.author} a report {user}, raison : {raison}, preuve : {preuve}")
    await ctx.send(embed=discord.Embed(description=f"Vous avez report **{user}** :white_check_mark:", color=0x34eb37), hidden=True)


@bot.event
async def on_guild_join(guild):
    bot.warnings[guild.id] = {}


@slash.slash(name="warn", description="Avertir un membre", options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être warn",
                    option_type=6,
                    required=True),
                create_option(
                    name="raison",
                    description="Entrez la raison du warn",
                    option_type=3,
                    required=True)
            ])
@has_permissions(manage_roles=True)
@bot_has_permissions(send_messages=True, read_messages=True)
async def warn(ctx, user: discord.User, raison):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    if await check_is_config(ctx.guild) is False:
        await ctx.send(embed=discord.Embed(title="Erreur", description=":warning: le bot n'est pas configuré, pour le configurer un administrateur doit exécuter la commande ``/config_server``", color=get_color(0xf54531, 0xf57231, 0xf53145)))
        logging.warning(f"{ctx.author} a utilisé une commande mais le bot n'est pas configuré")
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    channel_logs: discord.TextChannel = bot.get_channel(data['channel_logs'])
    color = get_color(0xedda5f, 0xedab5f, 0xbb76f5)
    try:
        bot.warnings[ctx.guild.id][user.id][0] += 1
        bot.warnings[ctx.guild.id][user.id][1].append((ctx.author.id, 1,raison))
    except KeyError:
        bot.warnings[ctx.guild.id][user.id] = [1, [(ctx.author.id, 1,raison)]]
    async with aiofiles.open(f"{ctx.guild.id}/sanctions.txt", mode="a") as file:
        await file.write(f"{user.id} {ctx.author.id} 1 {raison}\n")
    
    logging.info(f"{ctx.author} a warn {user}, raison : {raison}")
    await ctx.send(embed=discord.Embed(description=f"Vous avez warn **{user}** :white_check_mark:", color=0x34eb37), hidden=True)
    embed_user = discord.Embed(title="Vous avez été warn !", color=color)
    embed_user.set_thumbnail(url=ctx.author.avatar_url)
    embed_user.add_field(name="Raison", value=raison, inline=True)
    embed_user.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed_user.set_footer(text=f"Date • {datetime.datetime.now()}")
    await user.send(embed=embed_user)
    embed_logs = discord.Embed(title=f"{user} a été warn !", color=color)
    embed_logs.set_thumbnail(url=user.avatar_url)
    embed_logs.add_field(name="Raison", value=raison, inline=True)
    embed_logs.add_field(name="Modérateur", value=ctx.author.mention, inline=True)
    embed_logs.set_footer(text=f"Date • {datetime.datetime.now()}")
    await channel_logs.send(embed=embed_logs)


async def get_sanction_id(sanction_id):
    if sanction_id==1:
        return "warn"
    elif sanction_id==2:
        return "tempmute"
    elif sanction_id==3:
        return "kick"
    elif sanction_id==4:
        return "tempban"
    elif sanction_id==5:
        return "ban"


@slash.slash(name="sanctions", description="Permet d'obtenir la liste des sanctions d'un membre", options=[
                create_option(
                    name="user",
                    description="Entrez l'user qui doit être warn",
                    option_type=6,
                    required=True)
            ])
@has_permissions(manage_roles=True)
@bot_has_permissions(send_messages=True, read_messages=True)
async def sanctions(ctx, user: discord.User):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    color = get_color(0x5efffc, 0x5eff86, 0x7a75ff)
    guild: discord.Guild=ctx.guild
    embed_title = discord.Embed(title="Sanctions", description=f"Listes des sanctions de **{user}**", colour=color)
    try:
        try:
            await sanctions_files()
        except:
            pass
        i = 1
        embed_title.set_footer(text=user, icon_url=user.avatar_url)
        for author_id, sanction_id, raison in bot.warnings[ctx.guild.id][user.id][1]:
            color = get_color(0x5efffc, 0x5eff86, 0x7a75ff)
            sanction_name = await get_sanction_id(sanction_id)
            author = ctx.guild.get_member(author_id)
            embed=discord.Embed(title=f"{i}. {sanction_name}", description=":warning:", color=color)
            embed.add_field(name="Raison", value=raison)
            embed.add_field(name="Modérateur", value=author.mention)
            await ctx.send(embed=embed, hidden=True)
            i += 1
    except KeyError: # no warnings
        embed_title.add_field(name=":white_check_mark:", value="Ce membre n'a aucune sanction !")
        embed_title.set_footer(text=user, icon_url=user.avatar_url)
        await ctx.send(embed=embed_title, hidden=True)
    logging.info(f"{ctx.author} a utilisé la commande /sanctions {user}")

@slash.slash(name="user_info", description="Permet d'obtenir des informations à propos d'un membre sur le serveur")
@has_permissions(manage_roles=True)
async def user_info(ctx, user: discord.Member):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    embed=discord.Embed(title="User informations", description=f"**Informations** sur {user.mention}", color=get_color(0x42c5f5, 0xf54275, 0x5bfc58))
    embed.add_field(name="Pseudo complet", value=user, inline=True)
    embed.add_field(name="ID", value=user.id, inline=True)
    embed.add_field(name="Roles sur le serveur", value=len(user.roles) - 1, inline=False)
    embed.add_field(name="Role le plus haut", value=user.top_role, inline=False)
    if user.desktop_status is Status.online:
        status = ":green_circle: En ligne"
    elif user.desktop_status is Status.offline:
        status = ":black_circle: Hors ligne"
    elif user.desktop_status is Status.do_not_disturb:
        status = ":red_circle: Ne pas déranger"
    elif user.desktop_status is Status.idle:
        status = ":orange_circle: Inactif"
    embed.add_field(name="Statut", value=status)
    for booster in guild.premium_subscribers:
        if user is booster:
            embed.add_field(name="Serveur booster", value="Boost le serveur")
    embed.add_field(name="A rejoint le serveur le", value=user.joined_at)
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed, hidden=True)
    logging.info(f"{ctx.author} a utilisé la commande : /user_info {user}")


@slash.slash(name="server_info", description="Permet d'obtenir des informations sur le serveur")
@bot_has_permissions(send_messages=True, read_messages=True)
async def server_info(ctx: discord.ext.commands.context.Context):
    await ctx.defer(hidden=True)
    guild: discord.guild=ctx.guild
    if guild.description == None:
        guild_description="Aucune description"
    else:
        guild_description=guild.description
    embed=discord.Embed(title=f"Informations du serveur\n{guild.name}", description=guild_description, color=get_color(0xedda5f, 0xedab5f, 0xbb76f5))
    embed.add_field(name="Owner", value=guild.owner)
    embed.add_field(name="Serveur ID", value=guild.id)
    embed.add_field(name="Nombre de membres", value=guild.member_count, inline=True)
    embed.add_field(name="Nombre de salons", value=len(guild.channels), inline=True)
    embed.add_field(name="Nombre de salons vocaux", value=len(guild.voice_channels), inline=False)
    embed.add_field(name="Nombre de salons textuels", value=len(guild.text_channels), inline=True)
    embed.add_field(name="Création du serveur", value=guild.created_at, inline=False)
    embed.set_image(url=guild.icon_url)
    embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed, hidden=True)
    logging.info(f"{ctx.author} a utilisé la commande /server_info")


@slash.slash(name="config_server", description="Permet de configurer le bot pour le serveur discord")
@has_permissions(administrator=True)
@bot_has_permissions(manage_channels=True, send_messages=True, read_messages=True)
async def config_server(ctx):
    await ctx.defer(hidden=True)
    guild: discord.guild=ctx.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        guild.me: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel('configuration-serveur', overwrites=overwrites)
    config_channel = channel.id
    data= {'channel_config': config_channel}
    with open(f'guilds/{guild.id}/config.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)
    welcome_config: discord.Message = await channel.send(embed=discord.Embed(
        title="Configuration du bot", 
        description="Il y a t-il un channel de **bienvenue** ?", 
        color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e)), 
        components=[[
            Button(style=ButtonStyle.green, label="Oui", custom_id="yes_welcome_channel"), 
            Button(style=ButtonStyle.red, label="Non", custom_id="no_welcome_channel")
            ]])
    await ctx.send(embed=discord.Embed(title="Configuration du bot", 
                                        description="Un salon a été créé pour la configuration du bot", 
                                        color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e)), 
                                        components=[
                                    create_actionrow(
                                        create_button(style=ButtonStyle.URL, 
                                        url=f"https://discord.com/channels/{guild.id}/{channel.id}/{welcome_config.id}", 
                                        label="Lien vers le salon"))
                                    ])
    logging.info(f"{ctx.author} a commencé la configuration du bot")
    embed=discord.Embed(
                    title="Configuration du bot",
                    description=f"{ctx.author} a commencé la configuration du bot", 
                    color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e))
    logging.info(f"{ctx.author} a utilisé la commande /config_server {user}")
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    try:
        channel_logs: discord.TextChannel = await bot.fetch_channel(data['channel_logs'])
        await channel_logs.send(embed=embed)
    except:
        pass

@bot.event
async def on_button_click(interaction: Interaction):
    guild = interaction.guild
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    message_custom_id = interaction.custom_id 
    configserver_channel: TextChannel = await bot.fetch_channel(data['channel_config'])
    if message_custom_id== "yes_welcome_channel":
        await interaction.respond(embed=discord.Embed(
            title="Configuration du bot", 
            description="Entrez l'**id** du channel de bienvenue", 
                color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e)),
            components=[],
            type=7)
        async def get_channel_id(First_time=True):
            try:
                with open(f'guilds/{guild.id}/config.json') as infile:
                    data = json.load(infile)
                configserver_channel: TextChannel = await bot.fetch_channel(data['channel_config'])
                if First_time == False:
                    embed=discord.Embed(
                        title="Configuration du bot", 
                        description="Entrez l'**id** du channel de bienvenue", 
                            color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e),
                        components=[])
                    message_embed=await configserver_channel.send(embed=embed)
                message: discord.Message = await bot.wait_for("message", check=lambda m: m.author == interaction.author and m.channel == interaction.channel, timeout=30)
                
                channel = await bot.fetch_channel(message.content)
                data.update({'channel_welcome': channel.id})
                
                with open(f'guilds/{guild.id}/config.json', 'w') as outfile:
                    json.dump(data, outfile, indent=4)
                await message.delete()
                try:
                    await message_embed.delete()
                except:
                    pass
                await interaction.message.delete()
                await message.channel.send(embed=discord.Embed(
                title="Configuration du bot", 
                description="Il y a t-il un channel de **logs** ?", 
                    color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e)), 
                    components=[[
                Button(style=ButtonStyle.green, label="Oui", custom_id="yes_logs_channel"), 
                Button(style=ButtonStyle.red, label="Non", custom_id="no_logs_channel")
                ]],
                type=7)
                discord_invitation = await channel.create_invite(max_uses=0, max_age=0, reason="Configuration du bot")
                data.update({'invite_link': discord_invitation.url})
                with open(f'guilds/{guild.id}/config.json', 'w') as outfile:
                    json.dump(data, outfile, indent=4)
                return channel
            except asyncio.TimeoutError:
                await configserver_channel.send(embed=discord.Embed(title="Erreur", description=f"Vous n'avez pas repondu à la question", color=get_color(0xf54531, 0xf57231, 0xf53145)))
            except discord.errors.HTTPException:
                await configserver_channel.send(embed=discord.Embed(title="Erreur", description=f"Aucun channel ne correspond à l'id : **{message.content}**", color=get_color(0xf54531, 0xf57231, 0xf53145)))
                await get_channel_id(First_time=False)

        await get_channel_id(First_time=True)
        
    elif message_custom_id== "no_welcome_channel":
        guild: discord.Guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=True, send_messages=False),
    }
        channel: TextChannel = await guild.create_text_channel('bienvenue', overwrites=overwrites)
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        data.update({'channel_welcome': channel.id})
        
        with open(f'guilds/{guild.id}/config.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        message = await interaction.respond(embed=discord.Embed(
            title="Configuration du bot", 
            description="Channel **crée**, Il y a t-il un channel de **logs** ?", 
                color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e)), 
                components=[[
            Button(style=ButtonStyle.green, label="Oui", custom_id="yes_logs_channel"), 
            Button(style=ButtonStyle.red, label="Non", custom_id="no_logs_channel")
            ]],
            type=7)
        discord_invitation = await channel.create_invite(max_uses=0, max_age=0, reason="Configuration du bot")
        data.update({'invite_link': discord_invitation.url})
        with open(f'guilds/{guild.id}/config.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    elif message_custom_id == "yes_logs_channel":
        await interaction.message.delete()
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        configserver_channel: TextChannel = await bot.fetch_channel(data['channel_config'])
        
        async def get_channel_id(First_time: bool):
            message: discord.Message = await configserver_channel.send(embed=discord.Embed(
                title="Configuration du bot",
                description="Entrez l'**id** du channel de logs", 
                    color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e)),
                components=[],
                type=7)
            with open(f'guilds/{guild.id}/config.json') as infile:
                data = json.load(infile)
            try:
                if First_time == False:
                    embed=discord.Embed(
                        title="Configuration du bot", 
                        description="Entrez l'**id** du channel de logs", 
                            color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e),
                        components=[])
                    message_embed=await configserver_channel.send(embed=embed)
                message_user: discord.Message = await bot.wait_for("message", check=lambda m: m.author == interaction.author and m.channel == interaction.channel, timeout=30)
                channel_id = await bot.fetch_channel(message_user.content)
                data.update({'channel_logs': channel_id.id})
                with open(f'guilds/{guild.id}/config.json', 'w') as outfile:
                    json.dump(data, outfile, indent=4)
                    outfile.close()
                try:
                    await message_user.delete()
                except:
                    pass
                try:
                    await message_embed.delete()
                except:
                    pass
                try:
                    await message.delete()
                except:
                    pass
                embed=discord.Embed(
                    title="Configuration du bot", 
                    description="Terminée :white_check_mark:", 
                    color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e))
                embed.add_field(name="Channel de bienvenue", value=f"<#{data['channel_welcome']}>", inline=False)
                embed.add_field(name="Channel de logs", value=f"<#{data['channel_logs']}>", inline=False)
                embed.set_footer(text=f"Date • {datetime.datetime.now()}")
                await message.channel.send(embed=embed)
                return channel_id
            except asyncio.TimeoutError:
                await configserver_channel.send(embed=discord.Embed(title="Erreur", description=f"Vous n'avez pas repondu à la question", color=get_color(0xf54531, 0xf57231, 0xf53145)))
                await asyncio.sleep(10)
                await interaction.channel.delete()
            except discord.errors.HTTPException:
                await configserver_channel.send(embed=discord.Embed(title="Erreur", description=f"Aucun channel ne correspond à l'id : **{message.content}**", color=get_color(0xf54531, 0xf57231, 0xf53145)))
                await get_channel_id(First_time=False)
        await get_channel_id(First_time=True)
        await asyncio.sleep(10)
        try:
            await configserver_channel.delete()
        except discord.errors.NotFound:
            pass
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        embed=discord.Embed(title=f"{interaction.author} a terminé la configuration du bot", 
                    color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e))
        embed.add_field(name="Channel de bienvenue", value=f"<#{data['channel_welcome']}>", inline=False)
        embed.add_field(name="Channel de logs", value=f"<#{data['channel_logs']}>", inline=False)
        embed.add_field(name="Administateur", value=interaction.author.mention, inline=False)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed.set_thumbnail(url=interaction.author.avatar_url)
        channel_logs = await bot.fetch_channel(data['channel_logs'])
        await channel_logs.send(embed=embed)
        logging.info(f"{interaction.author} a terminé la configuration du bot")

    elif message_custom_id== "no_logs_channel":
        await interaction.message.delete()
        guild: discord.Guild = interaction.guild
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
        }
        channel = await guild.create_text_channel('logs', overwrites=overwrites)
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        data.update({'channel_logs': channel.id})
        with open(f'guilds/{guild.id}/config.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
        embed=discord.Embed(
                    title="Configuration du bot", 
                    description="Terminée :white_check_mark:", 
                    color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e))
        embed.add_field(name="Channel de bienvenue", value=f"<#{data['channel_welcome']}>", inline=False)
        embed.add_field(name="Channel de logs", value=f"<#{data['channel_logs']}>", inline=False)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        await interaction.respond(embed=embed)
        embed=discord.Embed(title=f"{interaction.author} a terminé la configuration du bot", color=get_color(0x3ef76f, 0xe8f73e, 0xf73e3e))
        embed.add_field(name="Channel de bienvenue", value=f"<#{data['channel_welcome']}>", inline=False)
        embed.add_field(name="Channel de logs", value=f"<#{data['channel_logs']}>", inline=False)
        embed.add_field(name="Administateur", value=interaction.author.mention, inline=False)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed.set_thumbnail(url=interaction.author.avatar_url)
        await channel.send(embed=embed)
        logging.info(f"{interaction.author} a terminé la configuration du bot")
        await asyncio.sleep(10)
        await interaction.channel.delete()

@slash.slash(name="help", description="Permet d'obtenir des renseignements à propos des commandes", options=[
                create_option(
                    name="command",
                    description="Renseignement à propos des commandes du bot",
                    option_type=3,
                    required=True,
                    choices=[
                 create_choice(
                    name="all commands",
                    value="all_commands"
                ),
                create_choice(
                    name="clear",
                    value="clear"
                  ),
                create_choice(
                    name="kick",
                    value="kick"
                  ),
                create_choice(
                    name="ban",
                    value="ban"
                  ),
                create_choice(
                    name="unban",
                    value="unban"
                  ),
                create_choice(
                    name="tempban",
                    value="tempban"
                  ),
                create_choice(
                    name="tempmute",
                    value="tempmute"
                  ),
                create_choice(
                    name="sanctions",
                    value="sanctions"
                ),
                create_choice(
                    name="unmute",
                    value="unmute"
                  ),
                create_choice(
                    name="report",
                    value="report"),
                create_choice(
                    name="ban_list",
                    value="ban_list"
                ),
                create_choice(
                    name="warn",
                    value="warn"
                ),
                create_choice(
                    name="server_info",
                    value="server_info"
                ),
                create_choice(
                    name="user_info",
                    value="user_info"
                ),
                create_choice(
                    name="config_server",
                    value="config_server"
                )
                ]),
             ])
@bot_has_permissions(send_messages=True, read_messages=True)
async def help(ctx, command):
    await ctx.defer(hidden=True)
    guild: discord.Guild=ctx.guild
    color = get_color(0xedda5f, 0xedab5f, 0xbb76f5)
    if command == "all_commands":
        author = ctx.author
        embed= discord.Embed(title="Liste de toutes les commandes les commandes",
        color=color)
        embed.add_field(name="``/clear``"
        , value="Cette commande permet d'effacer un certains nombre de message, pour plus de renseignement faites **/help clear**", inline=False)
        embed.add_field(name="``/kick``"
        , value="Cette commande permet d'expulser un membre du discord, pour plus de renseignement faites **/help kick**", inline=False)
        embed.add_field(name="``/ban``"
        , value="Cette commande permet de bannir un membre du discord, pour plus de renseignement faites **/help ban**", inline=False)
        embed.add_field(name="``/unban``"
        , value="Cette commande permet de dé-bannir un membre du discord, pour plus de renseignement faites **/help unban**", inline=False)
        embed.add_field(name="``/tempban``"
        , value="Cette commande permet de bannir temporairement un membre du discord, pour plus de renseignement faites **/help tempban**", inline=False)
        embed.add_field(name="``/tempmute``"
        , value="Cette commande permet de mute temporairement un membre du discord, pour plus de renseignement faites **/help tempmute**", inline=False)
        embed.add_field(name="``/unmute``"
        , value="Cette commande permet dé-mute un membre du discord, pour plus de renseignement faites **/help unmute**", inline=False)
        embed.add_field(name="``/report``"
        , value="Cette commande permet de report un membre du discord pour plus de renseignement faites **/help report**", inline=False)
        embed.add_field(name="``/ban_list``"
        , value="Cette commande permet d'obtenir la listes des membres bannis du discord, pour plus de renseignement faites **/help ban_list**", inline=False)
        embed.add_field(name="``/sanctions``"
        , value="Cette commande permet d'obtenir la listes des sanctions d'un membre du discord, pour plus de renseignement faites **/help sanctions**", inline=False)
        embed.add_field(name="``/warn``"
        , value="Cette commande permet d'avertir un membre du discord, pour plus de renseignement faites **/help ban_list**", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        embed.add_field(name="``/server_info``"
        , value="Cette commande permet d'obtenir des informations sur le serveur, pour plus de renseignement faites **/help server_info **", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        embed.add_field(name="``/config_server``"
        , value="Cette commande permet de configurer le bot pour le discord, pour plus de renseignement faites **/help config_server**", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        embed.add_field(name="``/user_info``"
        , value="Cette commande permet d'obtenir des informations d'un membre sur le serveur, pour plus de renseignement faites **/help user_info**", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "clear":
        author = ctx.author
        embed= discord.Embed(title="Commande clear", description="***/clear***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet d'effacer un certains nombre de message", inline=False)
        embed.add_field(name="Utilisation", value="``/clear [nombre de message]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "kick":
        author = ctx.author
        embed= discord.Embed(title="Commande kick", description="***/kick***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet d'expulser un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/kick [membre] [*raison]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "ban":
        author = ctx.author
        embed= discord.Embed(title="Commande ban", description="***/ban***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet de bannir un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/ban [membre] [*raison]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "unban":
        author = ctx.author
        embed= discord.Embed(title="Commande unban", description="***/unban***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet de dé-bannir un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/unban [membre] [*raison]`` :warning: l'option **membre** doit être rempli sous cette forme ***user#1234***", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "tempban":
        author = ctx.author
        embed= discord.Embed(title="Commande tempban", description="***/tempban***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet de bannir temporairement un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/tempban [membre] [durée : nombre] [temps : seconde / minute / heure / jour / mois] [*raison]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "tempmute":
        author = ctx.author
        embed= discord.Embed(title="Commande tempmute", description="***/tempmute***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet de mute temporairement un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/tempmute [membre] [durée : nombre] [temps : seconde / minute / heure / jour / mois] [*raison]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "unmute":
        author = ctx.author
        embed= discord.Embed(title="Commande tempban", description="***/tempmute***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet dé-mute un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/unmute [membre] [*raison]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "report":
        author = ctx.author
        embed= discord.Embed(title="Commande report", description="***/report***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet de report un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/report [membre] [raison] [*preuve: :warning: url vers une image :warning:]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "ban_list":
        author = ctx.author
        embed= discord.Embed(title="Commande ban_list", description="***/ban_list***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet d'obtenir la liste des membres bannis du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/ban_list``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)      
    elif command == "sanctions":
        author = ctx.author
        embed= discord.Embed(title="Commande sanctions", description="***/sanctions***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet d'obtenir la liste des sanctions d'un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/sanctions [membre]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "warn":
        author = ctx.author
        embed= discord.Embed(title="Commande warn", description="***/warn***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande d'avertir un membre du discord", inline=False)
        embed.add_field(name="Utilisation", value="``/warn [membre] [raison]``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "server_info":
        author = ctx.author
        embed= discord.Embed(title="Commande serveur information", description="***/server_info***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet d'obtenir des informations sur le serveur", inline=False)
        embed.add_field(name="Utilisation", value="``/server_info``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "user_info":
        author = ctx.author
        embed= discord.Embed(title="Commande user information", description="***/user_info***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet d'obtenir des informations à propos d'un membre du serveur", inline=False)
        embed.add_field(name="Utilisation", value="``/user_info``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    elif command == "config_server":
        author = ctx.author
        embed= discord.Embed(title="Commande configuration", description="***/config_server***",
        color=color)
        embed.add_field(name="A quoi sert cette commande ?", value="Cette commande permet de configurer le bot pour le serveur", inline=False)
        embed.add_field(name="Utilisation", value="``/config_server``", inline=False)
        embed.set_footer(text=author, icon_url=author.avatar_url)
        await ctx.send(embed=embed, hidden=True)
    
    logging.info(f"{ctx.author} a utilisé la commande /help {command}")


# BOT EVENT FOR LOGS
@bot.event
@bot_has_permissions(send_messages=True, read_messages=True)
async def on_message_delete(message: discord.Message):
    if message.author != bot.user:
        guild: discord.Guild=message.guild
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        try:
            channel_logs: discord.TextChannel = bot.get_channel(data['channel_logs'])
        except KeyError:
            pass
        embed=discord.Embed(
            title="Message supprimé",
            description=message.content,
            color=get_color(0xedda5f, 0xedab5f, 0xbb76f5)
        )
        embed.add_field(name="Auteur du message", value=message.author)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed.set_thumbnail(url=message.author.avatar_url)
        try:
            await channel_logs.send(embed=embed)
        except UnboundLocalError:
            pass
        logging.info(f"{message.author} a supprimé le message {message.id}, contenue : '{message.content}'")


# BOT EVENT FOR LOGS
@bot.event
@bot_has_permissions(send_messages=True, read_messages=True)
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author != bot.user:
        guild: discord.Guild=before.guild
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        try:
            channel_logs: discord.TextChannel = bot.get_channel(data['channel_logs'])
        except KeyError:
            pass
        embed=discord.Embed(
            title="Message edité",
            description=after.content,
            color=get_color(0xedda5f, 0xedab5f, 0xbb76f5)
        )
        embed.add_field(name="Auteur du message", value=before.author)
        embed.add_field(name="Ancien message", value=before.content)
        embed.set_footer(text=f"Date • {datetime.datetime.now()}")
        embed.set_thumbnail(url=after.author.avatar_url)
        try:
            await channel_logs.send(embed=embed)
        except UnboundLocalError:
            pass
        logging.info(f"{before.author} a edité le message {before.id}, avant : '{before.content}', après : '{after.content}'")


# BOT EVENT FOR LOGS
@bot.event
@bot_has_permissions(send_messages=True, read_messages=True)
async def on_guild_channel_create(channel):
    guild: discord.Guild=channel.guild
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    try:
        channel_logs: discord.TextChannel = bot.get_channel(data['channel_logs'])
    except KeyError:
        pass
    embed=discord.Embed(
        title="Un channel a été créé",
        color=get_color(0xedda5f, 0xedab5f, 0xbb76f5)
    )
    embed.add_field(name="Nom du channel", value=channel)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    try:
        await channel_logs.send(embed=embed)
    except UnboundLocalError:
        pass
    logging.info(f"Le salon '{channel}' a été créé")


# BOT EVENT FOR LOGS
@bot.event
@bot_has_permissions(send_messages=True, read_messages=True)
async def on_guild_channel_delete(channel):
    guild: discord.Guild=channel.guild
    with open(f'guilds/{guild.id}/config.json') as infile:
        data = json.load(infile)
    try:
        channel_logs: discord.TextChannel = bot.get_channel(data['channel_logs'])
    except KeyError:
        pass
    embed=discord.Embed(
        title="Un channel a été supprimé",
        color=get_color(0xedda5f, 0xedab5f, 0xbb76f5)
    )
    embed.add_field(name="Nom du channel", value=channel)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    try:
        await channel_logs.send(embed=embed)
    except UnboundLocalError:
        pass
    logging.info(f"Le salon '{channel}' a été supprimé")


# BOT EVENT FOR LOGS
@bot.event
@bot_has_permissions(send_messages=True, read_messages=True)
async def on_user_update(before: discord.User, after: discord.User):
    for guild in before.mutual_guilds:
        guild: discord.Guild=guild
        print(guild)
        with open(f'guilds/{guild.id}/config.json') as infile:
            data = json.load(infile)
        try:
            channel_logs: discord.TextChannel = bot.get_channel(data['channel_logs'])
        except:
            pass
    embed=discord.Embed(
        title=f"{before} a changé son profil",
        color=get_color(0xedda5f, 0xedab5f, 0xbb76f5)
    )
    embed.set_thumbnail(url=after.avatar_url)
    embed.set_footer(text=f"Date • {datetime.datetime.now()}")
    try:
        await channel_logs.send(embed=embed)
    except UnboundLocalError:
        pass
    except:
        pass
    logging.info(f"Le salon '{channel}' a été supprimé")


@bot.event
@bot_has_permissions(send_messages=True, read_messages=True)
async def on_message(message):
    if message.author == bot.user:
        return

    phrase = message.content.split(" ")

    hey_list = ['Bonjour', 'bonjour', 'Bonsoir', 'bonsoir', 'Salut', 'salut',
     'Hey', 'hey', 'Hello', 'hello', 'Coucou', 'coucou']
    hey_respond_list = ['Bonjour', 'Bonsoir', 'Salut', 'Heyyy', 'Hello', 'Coucou']
    if phrase[0] in hey_list:
        try:
            user = phrase[1]
            if user.startswith("<@!"):
                pass
            else:
                await message.reply(random.choice(hey_respond_list), delete_after=5)
        except IndexError:
            await message.reply(random.choice(hey_respond_list), delete_after=5)

    await bot.process_commands(message)


'''@bot.event
async def on_error(event, *args, **kwargs):
    exc_type, value, traceback = exc_info()
    if exc_type is discord.errors.Forbidden:
        logging.warning(f"{event}, discord.errors.Forbidden")
    elif exc_type is ValueError:
        logging.warning(f"{event}, ValueError")
    elif exc_type is KeyError:
        pass
    elif exc_type is discord.errors.NotFound:
        pass
    elif exc_type is json.decoder.JSONDecodeError:
        data= {}
        with open(f'guilds/{guild.id}/config.json', 'w') as outfile:
            json.dump(data, outfile, indent=4)
    else:
        print(f"""
        exc_type: {exc_type}\n
        value: {value}\n
        traceback.tb_frame: {traceback.tb_frame}\n
        args: {args}\n
        """
        )
        logging.warning(f"{event}, {exc_type}")'''


@bot.event
async def on_slash_command_error(ctx, error: discord.errors):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title="Erreur", description="Un argument requis n'a pas  été spécifié", color=get_color(0xf54531, 0xf57231, 0xf53145)), hidden=True)
        logging.warning(f"{ctx.author} a obtenu une erreur : {error}")
    elif isinstance(error, discord.errors.HTTPException):
        pass
    elif isinstance(error, MissingPermissions):
        embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145))
        embed.add_field(name="Permissions requises", value=f"**{error.missing_perms[0]}**")
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu une erreur : {error}")
    elif isinstance(error, commands.BotMissingPermissions):
        embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145))
        embed.add_field(name="Permission(s) requise(s)", value=f"**{error.missing_perms[0]}**")
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu l'erreur : {error}")
    elif isinstance(error, commands.errors.CommandInvokeError):
        pass
    elif isinstance(error, commands.errors.UserNotFound):
        embed=discord.Embed(title="Erreur", description="L'user spécifié est introuvable", color=get_color(0xf54531, 0xf57231, 0xf53145))
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu l'erreur : {error}")
    elif isinstance(error, commands.errors.NoPrivateMessage):
        embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145))
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu l'erreur : {error}")
    else:
        logging.warning(f"{ctx.author} a obtenu une erreur : {error}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145)), hidden=True)
        logging.warning(f"{ctx.author} a obtenu une erreur : {error}")
    elif isinstance(error, discord.errors.HTTPException):
        pass
    elif isinstance(error, MissingPermissions):
        embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145))
        embed.add_field(name="Permissions requises", value=f"**{error.missing_perms[0]}**")
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu une erreur : {error}")
    elif isinstance(error, commands.BotMissingPermissions):
        embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145))
        embed.add_field(name="Permission(s) requise(s)", value=f"**{error.missing_perms[0]}**")
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu l'erreur : {error}")
    elif isinstance(error, commands.errors.CommandInvokeError):
        pass
    elif isinstance(error, commands.errors.UserNotFound):
        embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145))
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu l'erreur : {error}")
    elif isinstance(error, errors.PrivilegedIntentsRequired):
        embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145))
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu l'erreur : {error}")
    else:
        embed=discord.Embed(title="Erreur", description=error, color=get_color(0xf54531, 0xf57231, 0xf53145))
        await ctx.send(embed=embed, hidden=True)
        logging.warning(f"{ctx.author} a obtenu l'erreur : {error}")


try:
    bot.run(os.getenv("TOKEN"))
except discord.errors.PrivilegedIntentsRequired:
    print(f'{Fore.RED}You need to enable "presence intents" and "server member intent" in developper portal : https://discord.com/developers/applications/{Fore.RESET}')
    logging.warning("Les parametres intents ne sont pas activés")
except AttributeError:
    print(f"{Fore.RED}Vous n'avez pas encore setup le bot, executez 'setup.py'{Fore.RESET}")
    logging.warning("Le token n'existe pas")
except discord.errors.LoginFailure:
    print(f"{Fore.RED}Le token entré n'est pas un token de bot valide{Fore.RESET}")
    logging.warning("Le token entré n'est pas un token de bot valide")
