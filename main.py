import discord
import os
import requests
import json
import toml
from replit import db
from keep_alive import keep_alive
from discord.ext import tasks

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # an attribute we can access from our task
        # self.counter = 0

        # start the task to run in the background
        self.my_background_task.start()


    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


    async def on_message(self, message):
      if message.author == client.user:
        return

      msg = message.content

      if msg.startswith('?space-open'):
        await handle_open_state(message.channel, True, client)
  

    @tasks.loop(seconds=60) # task runs every 60 seconds
    async def my_background_task(self):
        channel = self.get_channel(os.environ['BOT_CHANNEL'])
        await handle_open_state(channel, False, None)


    @my_background_task.before_loop
    async def before_my_task(self):
        await self.wait_until_ready() # wait until the bot logs in
        await handle_open_state(None, True, self)



async def handle_open_state(channel, always_send, client):
  open_state = get_open_state()
  already_sent = False

  if open_state == "OPEN":
    state_message = space_open_message
    status_message = space_open_status
  else:
    state_message = space_closed_message
    status_message = space_closed_status

  if check_open_state_changed(open_state):
    update_open_state(open_state)

    if channel:
      await channel.send(state_message)
    
    if client and change_status:
      await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_message))
      
    already_sent = True

  if always_send and already_sent == False:
    if channel:
      await channel.send(state_message)

    if client:
      if change_status:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status_message))
      else:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=""))

def update_open_state(open_state):
  db["open_state"] = open_state


def get_open_state():
  response = requests.get(spaceapi_url)
  json_data = json.loads(response.text)  

  if (json_data["state"]["open"]):
    open_state = "OPEN"
  else:
    open_state = "CLOSED"

  return(open_state)


def check_open_state_changed(open_state):
  if "open_state" in db.keys():
    if db["open_state"] == open_state:
      changed = False
    else:
      changed = True
  else:
    changed = True

  return(changed)


config = toml.load("config.toml")
print(config)

spaceapi_url = config["settings"]["spaceapi_url"]
space_open_message = config["messages"]["space_open"]
space_closed_message = config["messages"]["space_closed"]
space_open_status = config["statuses"]["space_open"]
space_closed_status = config["statuses"]["space_closed"]
change_status = config["statuses"]["change_status"]

client = MyClient()

keep_alive()
client.run(os.environ['TOKEN'])