import discord
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import asyncio

# Replace with the path to your WebDriver
driver_path = (r'C:\Users\')

# Create a new instance of the web driver
driver = webdriver.Edge()

# Go to the local hosted page
driver.get("http://127.0.0.1:8000")

# Wait for the page to load completely
time.sleep(3)  # You can use WebDriverWait for a more robust solution

Charbar = driver.find_element(By.ID, "rightNavDrawerIcon")
Charbar.click()
time.sleep(2)
Charpane = driver.find_element(By.XPATH, '//*[@title="[Character] CEO Joe"]')
Charpane.click()
time.sleep(2)
Charbar = driver.find_element(By.ID, "rightNavDrawerIcon")
Charbar.click()
time.sleep(2)

# Initialize Discord bot with command prefix
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

async def send_prompt_to_ST(user_message):
    textarea = driver.find_element(By.ID, "send_textarea")
    textarea.clear()
    textarea.send_keys(Speaker)
    
    # Find the send button and click it
    send_button = driver.find_element(By.ID, "send_but")
    send_button.click()

    textarea = driver.find_element(By.ID, "send_textarea")
    textarea.clear()
    textarea.send_keys(user_message)
    
    # Find the send button and click it
    send_button = driver.find_element(By.ID, "send_but")
    send_button.click()

    # Poll for the response from the SillyTavern interface (raise timeout for handling longer response)
    timeout = 60
    elapsed_time = 0
    polling_interval = 3
    
    while elapsed_time < timeout:
        await asyncio.sleep(polling_interval)
        elapsed_time += polling_interval

        try:
            # Retrieve the last message's div
            last_message_div = driver.find_element(By.XPATH, "//*[@class='mes last_mes']")
            
            # Check if the last message is from "CEO Joe"
            if last_message_div.get_attribute('ch_name') == "CEO Joe":
                # Retrieve the response text
                response_area = last_message_div.find_element(By.XPATH, ".//*[@class='mes_block']/*[@class='mes_text']")
                response = response_area.get_attribute('innerText')
                return response
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return "No response received from CEO Joe within the timeout period."

#FUNCTION FOR RESPONSE REGENERATION (will need to confirm manually the first time in the web interface as the hotkeys trigger a confirmation window)
async def regenerate_response():
    ActionChains(driver).key_down(Keys.LEFT_CONTROL).key_down(Keys.ENTER).key_up(Keys.LEFT_CONTROL).key_up(Keys.ENTER).perform()
    # Poll for the response from the SillyTavern interface
    timeout = 60
    elapsed_time = 0
    polling_interval = 3
    
    while elapsed_time < timeout:
        await asyncio.sleep(polling_interval)
        elapsed_time += polling_interval

        try:
            # Retrieve the last message's div
            last_message_div = driver.find_element(By.XPATH, "//*[@class='mes last_mes']")
            
            # Check if the last message is from "CEO Joe"
            if last_message_div.get_attribute('ch_name') == "CEO Joe":
                # Retrieve the response text
                aresponse_area = last_message_div.find_element(By.XPATH, ".//*[@class='mes_block']/*[@class='mes_text']")
                aresponse = aresponse_area.get_attribute('innerText')
                return aresponse
        except Exception as e:
            print(f"Error: {e}")
            continue
    
    return "No response received from CEO Joe within the timeout period."

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    ceojoe_channel = bot.get_channel("YOUR CHANNEL ID")
    if ceojoe_channel:
        await ceojoe_channel.send("online")

@bot.event
async def on_message(message):
    global Speaker
    global Lastbotmsg
    if message.author == bot.user:
        Lastbotmsg = message.content
        return

#Use discord user id to have silly tavern swap to corresponding persona ensure persona name matches
    if message.channel.id == "YOUR CHANNEL ID":
        Contacts = {
            142362674401900000: "/persona Dan",
            139851631750000000: "/persona Danny",
            446104480990000000: "/persona Daniel",
            139879372360000000: "/persona Dwain",
            175045276900000000: "/persona Draven",
            140218139500000000: "/persona Dunder"
        }

        Persona = message.author.id
        print(Persona)
        if Persona in Contacts:
            Speaker = Contacts[Persona]
            print(Speaker)
        else:
            #need to create a persona for a unknown person if a identified person is not messaging.
            Speaker = "/persona Unknown Person"
        
        response = await send_prompt_to_ST(message.content)
        
        if response:
            response_message = await message.channel.send(response)
            await response_message.add_reaction('🔄')

#Regenerate a response by reacting to the reaction the bot sends with every message
@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
        
    if payload.emoji.name == '🔄' and payload.channel_id == "YOUR CHANNEL ID":
        channel = bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        if message.author.id == bot.user.id:
            await message.delete()
            aresponse = await regenerate_response()
            if aresponse:
                aresponse_message = await message.channel.send(aresponse)
                await aresponse_message.add_reaction('🔄')

bot.run('YOUR BOT TOKEN ID')
