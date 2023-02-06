from pyrogram import *
from pyrogram.types import *
import redis
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
MONGO = "mongodb+srv://devcoder:aaee1122@cluster0.m4rtiot.mongodb.net/?retryWrites=true&w=majority"

mongo = MongoClient(MONGO)

botdb = mongo.Bots
usersdb = mongo.Users
groupsdb = mongo.Groups
sudodb = mongo.Sudos

api_id = 12643300
api_hash = "73c1a336adc28a59661ff7761ff02672"
token = "6061404312:AAFrjP-Bk3NqhA3AETToX0PUoE_H3nXwyEM"
bot_id = token.split(":")[0]
owner = int(5550346979)
owner_username = "BodaDev"

app = Client("kvy",api_id=api_id,api_hash=api_hash,bot_token=token)

#==================================================#

Start_txt = "hello how are you ?!"
Start_mark = InlineKeyboardMarkup([[
InlineKeyboardButton("Dev",url=f"https://t.me/{owner_username}"),
InlineKeyboardButton("ch ",url=f"https://t.me/{f'{bot_id}_force_channel'}")
]])

#==================================================#

async def is_user(user_id:int) -> bool:
	user = await usersdb.find_one({"user":user_id})
	if not user:
		return False
	return True
	
async def is_group(chat_id:int) -> bool:
	group = groupsdb.find_one({"group":chat_id})
	if not group:
		return False
	return True

async def is_sudo(sudo_id:int) -> bool:
	sudo = await sudodb.find_one({"sudo":sudo_id})
	if not sudo:
		return False
	return True

#==================================================#

async def add_user(user_id:int):
	is_aded = await is_user(user_id=user_id)
	if is_aded:
		return
	await usersdb.insert_one({"user":user_id})
	
async def add_group(chat_id:int):
	is_aded = await is_group(chat_id=chat_id)
	if is_aded:
		return
	await groupsdb.insert_one({"chat":chat_id})

async def add_sudo(sudo_id:int):
	is_aded = await is_sudo(sudo_id=sudo_id)
	if is_aded:
		return
	await sudodb.insert_one({"sudo":sudo_id})

async def rem_sudo(sudo_id:int):
	is_aded = await is_sudo(sudo_id=sudo_id)
	if not is_aded:
		return
	await sudodb.remove_one({"sudo":sudo_id})
	
#==================================================#

async def get_users() -> list:
	users =[] 
	async for user in usersdb.find_one({"user":{"$gt":0}}):
		users.append(user)
	return users

async def get_groups() -> list:
	groups =[]
	async for group in groupsdb.find_one({"chat":{"$gt":0}}):
		groups.append(group)
	return groups

#==================================================#

r = redis.from_url("redis://default:hzETAuS6vkUy7LZwgcB84G44jDMwgDik@redis-13813.c289.us-west-1-2.ec2.cloud.redislabs.com:13813")
	
r.set(f"{bot_id}_owner",owner)

async def check(id):
	if await is_sudo(sudo_id=id):
		return True
	if id == int(r.get(f"{bot_id}_owner")):
		return True
	else:
		return False

async def chk_sub(c:Client,m:Message):
	if not r.get(f"{bot_id}_enable_force_sub"):
		return
	else:
		if not r.get(f"{bot_id}_force_channel"):
			return
		else:
			channel = r.get(f"{bot_id}_force_channel").decode('utf-8')
			text =f"**You must join @{channel} to user the bot √**"
			try:
				get = await c.get_chat_member(chat_id=channel,user_id=m.from_user.id)
				if get.status in [enums.ChatMemberStatus.BANNED,enums.ChatMemberStatus.LEFT]:
					return await m.reply(text=text,quote=True,disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ch",url=f"https://t.me/{channel}")]]))
				return await m.reply(text=Start_txt,quote=True,disable_web_page_preview=True,reply_markup=Start_mark)
			except:
				return await m.reply(text=text,quote=True,disable_web_page_preview=True,reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ch",url=f"https://t.me/{channel}")]]))
			return await m.reply(text=Start_txt,quote=True,disable_web_page_preview=True,reply_markup=Start_mark)
		#return await m.reply(text=Start_txt,quote=True,disable_web_page_preview=True,reply_markup=Start_mark)
		
#==================================================#

@app.on_message(filters.command("start")&filters.private)
async def st(c:Client,m:Message):
	
	user = m.from_user.id
	
	if not await check(id=user):
		return await chk_sub(c,m)
	if not await is_user(user_id=user):
		text = f"**New user in your bot !**\n\nuser-id : `{user}` √\nuser link : {m.from_user.mention} √"
		mark = InlineKeyboardMarkup([[InlineKeyboardButton(f"{m.from_user.first_name}",user_id=int(user))]])
		
		await app.send_message(owner,text=text,reply_markup=mark)
		await m.reply(text=Start_txt,quote=True,disable_web_page_preview=True,reply_markup=Start_mark)
		return
	return await m.reply(text=Start_txt,quote=True,disable_web_page_preview=True,reply_markup=Start_mark)
	
if __name__ == "__main__":
	app.run()
