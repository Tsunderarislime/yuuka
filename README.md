# yuuka
Discord bot which should automatically detect scam messages, delete said messages, then ban the offending account.

Use chat commands `y^<command>` to configure the bot. Chat commands require the 'manage server' permission to be used.

### Commands
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
