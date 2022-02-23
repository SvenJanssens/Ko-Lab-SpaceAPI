# Ko-Lab-SpaceAPI

This is the Git repository for the Ko-Lab-SpaceAPI Discord bot hosted at https://replit.com/@SvenJanssens/Ko-Lab-SpaceAPI.

Most of the files on GitHub are generated by Replit.

The main files for consideration are the following:
* [main.py](/main.py) - Contains the actual logic of the bot. It checks the content of the SpaceAPI JSON located at https://vloer.ko-lab.space/spaceapi.json (configured in [config.toml](/config.toml)) and based on the content of the state/open field the bot will:
  * post status update messages in a specified channel (configured in an environment variable BOT_CHANNEL);
  * update its status to "Watching an open space" or "Watching a closed space" (enabled/disabled by using the statuses/change_status boolean in [config.toml](/config.toml));
  * reply with the current status after a user enters ?space-open in a text channel to which the bot has access.
* [keep_alive.py](/keep_alive.py) - Contains a basic Flask web server, this is used because hosted bots will get shut down after an hour on Replit. This is avoided by using this web server and polling it from a service like https://www.uptimerobot.com/
* [config.toml](/config.toml) - Configuration file currently having settings for:
  * The URL which will return the SpaceAPI JSON
  * The messages used by the bot to reply to ?space-open
  * The statuses used by the bot to set its own status
