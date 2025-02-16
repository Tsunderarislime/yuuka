# yuuka
![Yuuka icon](https://i.imgur.com/NFxbJOU.png)

Discord bot which should automatically detect scam messages, delete said messages, then ban the offending account. This is more or less just a proof of concept for an automated moderation tool as a Discord bot. A few servers I frequent have noticed a rise in scam advertisements, which often involve giving away a "free" MacBook or PlayStation.

I noticed that these messages and the users that send them tend to follow a pattern. I initially tried using regular expressions to filter, but found that even the smallest changes to the message would get around the filter. These bots often include similar terms, but may mix up the structure of how the scams are advertised.  So I made Yuuka to test if these scams could be detected with a simple algorithm to automatically delete the messages and ban the users. 

# !!! IMPORTANT UPDATE, PLEASE READ !!!
A **complete implementation of Yuuka** has been developed as a cog for the [Red Discord Bot](https://github.com/Cog-Creators/Red-DiscordBot). This cog has been given the name "Gatekeep" and is part of the [lui-cogs](https://github.com/SFUAnime/lui-cogs-v3) repository. SFU Anime's fork of the Red Discord Bot, [Ren](https://github.com/SFUAnime/Ren), has utilized my cog to great success.

![Scam message gets gatekept](https://i.imgur.com/kbGFCz4.png)
<sub>Perish, MacBook scammer!</sub>

Anyways, if you want to use Yuuka (Gatekeep), you should host an instance of the Red Discord Bot and install lui-cogs on it.
<br><br><br>
<hr>
<hr>
<hr>
<br>

## Usage, for those who still want to use this instead of using Red

### Commands
Use chat commands `y^<command>` to configure the bot. Chat commands require the 'manage server' permission to be used.

- **help**: Lists all of the commands
- **github**: Links to this repository
- **initialize**: Generates a database for the server that this command was used in. This needs to be done before the filter can operate
- **filter**: Important command that allows for configuration of the filter. Using this command without any arguments provides a list of sub-commands and how to use them.

### How it Works
The way this bot works is you add words and give them 'weights'. If a message contains a lot of these weighted words, it will accumulate a high score. If this score exceeds a threshold (configurable), then that message is marked as spam and the account that sent the message will be banned.

There is a kind of 'trust' system that exists to prevent all messages from all users from being scored. **Upon initialization, every account which has been on the server for over 3 weeks is automatically entered into a database which marks their user IDs as 'trusted'. For accounts that are not in this database, all they have to do is send one message which does not exceed the threshold.**

This is subject to change, maybe it's too forgiving, maybe it's too strict, it really comes down to the effectiveness of the filter and the word weights.

### How to Run
1. `echo bot-token >> token.txt` (this file should be in root directory with `bot.py`)
2. `pip install -r requirements.txt`
3. `python bot.py`
