import discord
import configparser
import random

import os
import errno

client = discord.Client()

#____________________________________
#config読み込み
#____________________________________
config = configparser.ConfigParser()
config_ini_path = 'settings.ini'
#configファイルがない場合のエラー
if not os.path.exists(config_ini_path):
    raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), config_ini_path)

config.read(config_ini_path, encoding='utf-8')

#権限設定取得
boss = config['Admin']['AdminID']

#______________________________________

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    #shutdown command for Admin-----------------------------------------------
    if message.content.startswith('!shutdown'):
        if message.author.id == int(boss):
            await message.channel.send("Shutting down.")
            await client.close()
        else:
            await message.channel.send("Who's there?")
            return

    if message.content.startswith('!hello'):
        await message.channel.send('Hello!')


    #diceroll------------------------------------------------------------
    if message.content.startswith('!roll'):
        dices = message.content.split(" ")
        print("roll command in")

        if len(dices) == 2:
            # D前後をsplit
            dicepref = dices[1].split("D")

            # Dの前後が数字か確認
            if dicepref[0].isdigit() and dicepref[1].isdigit():

                #100D100制限
                if (int(dicepref[0]) > 100) or (int(dicepref[1]) > 100):
                    await message.channel.send("100D100が最大値です")

                else:
                    rolls = 0
                    results = [0]

                    #roll, 数記憶
                    for i in range(int(dicepref[0]) - 1):
                        rolls = random.randint(1, int(dicepref[1]))
                        results[0] += rolls
                        results.append(str(rolls) + "+")
                        print(str(rolls) + "+",end="")

                    rolls = random.randint(1, int(dicepref[1]))
                    results[0] += rolls
                    results.append(str(rolls) + "= **" + str(results[0]) + "**")
                    print(str(rolls) + "= " + str(results[0]))

                    #ひとまとめにして出力
                    #for i in range(1, dicepref[0] + 1):
                    #    rollline = str(rollline + results[i])
                    del results[0]
                    await message.channel.send("> " + str(dicepref[0]) + "D" + str(dicepref[1]) + " =\n> " + "".join(results))

            #!roll後にスペースが入っている
            elif len(dices[1]) < 3:
                await message.channel.send("> D6 = **" + str(random.randint(1, 6)) + "**")

            #Dの前後が数字ではない場合
            else:
                await message.channel.send("「!roll」でD6一つ、「!roll xDy」でDyをx個ロール")
        elif len(dices) == 1:
            print(random.randint(1, 6))
            await message.channel.send("> D6 = **" + str(random.randint(1, 6)) + "**")
        else:
            await message.channel.send("「!roll」でD6一つ、「!roll xDy」でDyをx個ロール")

    #todo FF14マクロ変換
    if message.content.startswith('!henkan'):
        line = message.content.split(" ")
        await message.channel.send(line)

    #Partyfinder-------------------------------------------------------------
    if message.content.startswith("!PT") or message.content.startswith("!pt"):

        # PT募集チャンネル未設定or設定チャンネル上の場合
        if (int(config['Settings']['PTfindchannel']) == 0) or (message.channel.id == int(config['Settings']['PTfindchannel'])):

            await message.channel.send("LookingForPT")

        # 設定されたPT募集チャンネルに送信
        else:
            await message.channel.send("PT募集用チャンネルを使ってください")

client.run(str(config['bot']['BotToken']))
