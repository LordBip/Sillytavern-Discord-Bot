Lucrative method to run a discord bot using the sillytavern platform. While I am certain alternative methods may be easier to implement I figure this would be a simple bootlegged solution for those fixated on achieving this. It uses a webdriver (selenium in this case) to navigate to your sillytavern instance and interact with the page. I dont see too much in the way of expansion for this project as its essentially automating page usage with the webdriver handling everything.

To operate you need to have the following:

  Python (Version used = 3.10.14) *I don't think your version would affect this much*
  I can't remember exactly what packages I installed as I used the same enviorment for another project :). Definitly Selenium and Discord.py (Would reccomend conda enviorment if your familiar) 
    1. pip install selenium
    2. pip install discord.py

  Webdriver
  I used Edge (https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver?form=MA13LH), I can not remember the exact version so I included the driver files in the repository. Just make 
  to change your file path to it accordingly on line 11
  
  Sillytavern 
    1. Sillytavern character created: In the code you will need to edit Line 25 with the name of this character for it to be selected properly 
    2. A generation API:  I used koboldcpp and ran locally using my own GPU howver you can use any of the supported API's.
    3. Personas (optional): Line 123 - 140 of the code have the webdriver type "/persona PERSONANAME" before each message. If your operating a bot for a small user group it may be   
       beneficial to create a persona in sillytavern for each user as the bot will be able to attach a name to the user as well as persona descriptions can include info on each user for the bot to        reference. You will need to apply the correct User Id to each persona in the code. Line 138 - 140 contains the exception if a user is not found. I madea a persona for a unknown speaker     
       however I think the code would still work fine without a "Unknown speaker" persona made. 

  Discord Bot
    1. You need to create a discord bot (https://discord.com/developers/docs/quick-start/getting-started)
    2. Bot needs to added to your discord server and ensure it has the permission to read, and send messages. Additionally it will need to have proper channel permissions.

Notes:

Code is designed to only have the bot interact with messages recieved in a specified channel. You can set the channel id to one you create for the bot, or you can remove the channel id checks (not overall reccommended) to have the bot react with all messages.

Code does not handle a user sending back to back messages well, it can lead to a response being skipped, or other "bugs". Best practice is to wait for a response before sending another message.

The first time you regenerate a response, Sillytavern prompts the user to confirm. You will need to check the box "dont ask again" when this happens. Once you have done this once, you will no longer need to repeat this step untill you restart the bot.

As of 7/9/24 I can confirm the code works however updates to Sillytavern Ui can make this obsolete or better solutions may become obtainable.
  