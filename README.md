[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
![GitHub repo size](https://img.shields.io/github/repo-size/feytus/neptunbot?style=for-the-badge&logo=appveyor)
___
[![Invite - me](https://img.shields.io/badge/Invite-me-2295c7?style=for-the-badge&logo=discord&logoColor=white)](discord.com/oauth2/authorize?client_id=811977160067776522&permissions=-214438817&scope=applications.commands%20bot)
[![Docs](https://img.shields.io/website?down_color=lightgrey&down_message=offline&style=for-the-badge&up_color=green&up_message=documentation&url=https%3A%2F%2Ffeytus.github.io%2F%23neptun)](https://feytus.github.io/#neptun)
<br>

# Neptun BOT Documentation

Neptun BOT is a **usefull** moderation bot totally made in **python** with the module ``discord_py`` and ``discord_slash``.

## **If you want to host the bot by yourself follow the steps :**

1. Installation

```
git clone https://github.com/feytus/NeptunBOT.git
```

2. Setup

To setup the bot you need to execute ``setup.py`` file and enter the token of your bot.

3. Configuration

A server administrator will have to execute the command [/config_server](https://github.com/feytus/NeptunBOT#server-config) on the **discord**.

## **Normal member commands list**

This is all the commands that you can execute only with the permission to write in a channel. If a command is preceded by a " * " it means that the argument is optional.

### **Help**

This command allows you to obtain more information about an order.

- `/help {command}`

### **Report**

This command allows you to report a member who has not respected the rules of the server.

- `/report {member} {reason} {*proof}`

### **Server info**

This command allows you to get information about the discord.

- `/serverinfo`

## **Moderator commands list**

### **Clear**

This command allows you to delete a certain number of messages.

- `/clear {*amount}`

### **Tempmute**

This command allows you to temporarily mute a member of the discord.

- `/tempmute {member} {amount: int} {time: (s / m / h / j / mois)} {*reason}`

### **Unmute**

This command allows you to unmutes a member of the discord.

- `/unmute {member} {*reason}`

### **Kick**

This command allows you to kick a member of the discord.

- `/kick {member} {*reason}`

### **Tempban**

This command allows you to temporarily ban a member of the discord.

- `/tempban {member} {amount: int} {time: (s / m / h / j / mois)} {*reason}`

### **Ban**

This command allows you to ban a member of the discord.

- `/ban {member} {*reason}`

### **Unban**

This command allows to un-ban a member of the discord.

- `/unban {member} {*reason}`

⚠️ The option **{member}** should be like this : *name#1234*

### **Banlist**

This command allows you to get the list of members banned from the discord.

- `/banlist`

### **Warn**

This command allows you to warn a member of the discord.

- `/warn {member} {reason}`

### **Sanctions**

This command allows you to see all the sanctions of a discord member.

- `/sanctions {member}`

### **Server config**

This command allows you to configure the bot for the discord server.

- `/server_config`

### **Server information**

This command allows you to get information about the server.

- `/server_info`

### **User information**

This command allows you to get information about za member of the server.

- `/user_info {member}`

## **Other things**

The bot also send a message on member join the discord.

![Image of welcome_message_embed](https://i.imgur.com/GlyVXYZ.png)

All bot actions are logged in a file and in a channel exemple :

![Image of welcome_message_embed](https://i.imgur.com/isEzFh3.png)
