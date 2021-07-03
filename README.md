# Smogy BOT

Smogy BOT is a **usefull** moderation bot totally made in **python** with the module ``discord_py`` and ``discord_slash``.

## **Normal member commands list**

\
This is all the commands that you can execute only with the permission to write in a channel. If a command is preceded by a " * " it means that the argument is optional.

### **Help**

This command allows you to obtain more information about an order.

- `/help {command}`

### **Report**

This command allows you to report a member who has not respected the rules of the server.

- `/report {member} {reason} {*proof}`

## **Moderator commands list**

### **Clear**

This command allows you to delete a certain number of messages.

- `/clear {amount}`

### **Tempmute**

This command allows you to temporarily mute a member of the discord.

- `/tempmute {member} {amount: int} {time: (s - m - h - j - mois)} {*reason}`

### **Unmute**

This command allows you to unmutes a member of the discord.

- `/unmute {member} {*reason}`

### **Kick**

This command allows you to kick a member of the discord.

- `/kick {member} {*reason}`

### **Ban**

This command allows you to ban a member of the discord.

- `/ban {member} {*reason}`

### **Unban**

This command allows to un-ban a member of the discord.

- `/unban {member} {*reason}`

⚠️ The option {member} should be like this : **name#1234**
