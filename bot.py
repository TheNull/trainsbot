# Invite bot for Gay Trains
import discord
import asyncio
import datetime
import bot_info

trainsbot = discord.Client()

@trainsbot.event
async def on_ready():
	print("Ready to go!")
	print(trainsbot.user.name)
	print(trainsbot.user.id)
	reqperms = discord.Permissions()
	reqperms.administrator = True
	url = discord.utils.oauth_url(trainsbot.user.id, permissions=reqperms) 
	print(url)
	print("Beginning execution...")

@trainsbot.event
async def on_message(message):
	try:
		firehose = discord.utils.find(lambda m: m.name == "firehose", message.server.channels)
	except:
		await trainsbot.send_message(message.channel, "Something went wrong")
	if message.channel.name != "firehose":
		unfdmsg = "{0.channel} **|** {0.author.display_name}: {0.content}" 
		await trainsbot.send_message(firehose, unfdmsg.format(message))
	if message.content.startswith("!invite"):
		try:
			fmt2 = "landing-{0.author.id}" 
			everyone_perms = discord.PermissionOverwrite(read_messages=False)
			mine_perms = discord.PermissionOverwrite(read_messages=True)
			mine = discord.ChannelPermissions(target=message.server.me, overwrite=mine_perms)
			everyone = discord.ChannelPermissions(target=message.server.default_role, overwrite=everyone_perms)
			newchan = await trainsbot.create_channel(message.server,fmt2.format(message),everyone,mine)
			invite = await trainsbot.create_invite(destination= newchan, max_uses = 1)
			await trainsbot.send_message(message.channel, "Your invite is awaiting approval, thank you.")
			adminchannel = discord.utils.find(lambda m: m.name == "admins", message.server.channels)
			fmt = "User {0.author} has requested an invite. Invite code: {1.code}"
			await trainsbot.send_message(adminchannel, fmt.format(message,invite))
		except Exception as e: print(e)
@trainsbot.event
async def on_message_delete(message):
	firehose = discord.utils.find(lambda m: m.name == "firehose", message.server.channels)
	unfdmsg = "{0.channel} **|** **{0.author.display_name}** deleted their message: {0.content}"
	await trainsbot.send_message(firehose, unfdmsg.format(message))
trainsbot.run(client_key)		
