import os

try:
    config = open("config", "x")
except FileExistsError:
    os.remove("config")
    config = open("config", "a")

token = input("Entrez le token du bot : ")
config.write(f"TOKEN = {token}\n")

channel_logs = input("Entrez l'id du channel logs : ")
config.write(f"channel_logs = {channel_logs}\n")

channel_welcome = input("Entrez l'id du channel de bienvenue : ")
config.write(f"channel_welcome = {channel_welcome}\n")

invite_link = input("Entrez un lien d'invitation ATTENTION veillez bien à ce que l'invation n'expire jamais : ")
config.write(f"invite_link = {invite_link}\n")