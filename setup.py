import os

os.system('pip3 install -r requirements.txt')
os.system('clear')

from pyfade import *

setup = """
███████╗███████╗████████╗██╗   ██╗██████╗ 
██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗
███████╗█████╗     ██║   ██║   ██║██████╔╝
╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝ 
███████║███████╗   ██║   ╚██████╔╝██║     
╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝     
                                          
"""

print(Fade.Vertical(Colors.green_to_blue, setup))

try:
    config = open("token", "x")
except FileExistsError:
    os.remove("token")
    config = open("token", "a")

token = input("Entrez le token du bot : ")
config.write(f"TOKEN = {token}\n")

os.system('clear')
setup_finish = """
███████╗███████╗████████╗██╗   ██╗██████╗     ███████╗██╗███╗   ██╗██╗███████╗██╗  ██╗
██╔════╝██╔════╝╚══██╔══╝██║   ██║██╔══██╗    ██╔════╝██║████╗  ██║██║██╔════╝██║  ██║
███████╗█████╗     ██║   ██║   ██║██████╔╝    █████╗  ██║██╔██╗ ██║██║███████╗███████║
╚════██║██╔══╝     ██║   ██║   ██║██╔═══╝     ██╔══╝  ██║██║╚██╗██║██║╚════██║██╔══██║
███████║███████╗   ██║   ╚██████╔╝██║         ██║     ██║██║ ╚████║██║███████║██║  ██║
╚══════╝╚══════╝   ╚═╝    ╚═════╝ ╚═╝         ╚═╝     ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝
"""

print(Fade.Vertical(Colors.red_to_blue, setup_finish))

input("Appuyez sur ENTER pour quitter le setup ")