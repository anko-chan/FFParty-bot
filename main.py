import discord
import configparser
import random

import os
import errno
import logging

client = discord.Client()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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

    #todo
    #guildを取得したい

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
                    await message.channel.send("> " + str(dicepref[0]) + "D" + str(dicepref[1]) + " \n> =" + "".join(results))

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
    #PT番号
    PTnum = 0
    #PT情報保存用リスト
    #[messageid, authorid, title, desc, ]
    PTinfo = [[0] * 4] * int(config['Settings']['maxparty'])


    if message.content.startswith("!PT") or message.content.startswith("!pt"):

        # PT募集チャンネル未設定or設定チャンネル上の場合
        if (int(config['Settings']['PTfindchannel']) == 0) or (message.channel.id == int(config['Settings']['PTfindchannel'])):
            #await message.channel.send("LookingForPT")

            #todo 同時募集PT数制限

            PTnum += 1
            PTdesc = message.content.split(" ")

            #出力
            PTfindmsg = await message.channel.send(message.author.mention + "がPT募集中!\n> **__" + str(PTdesc[1]) + "__**\n > " + str(PTdesc[2]))
            # @author がPT募集中!
            # <b><u>Title</b></u>
            # desc~~~

            #Messageidを取得。保存。emoji付け
            PTfindmsg_id = PTfindmsg.id
            PTfindmsg_guild = PTfindmsg.guild


            #各種emoji
            pld_em = discord.utils.get(PTfindmsg.guild.emojis, name='PLD')
            war_em = discord.utils.get(PTfindmsg.guild.emojis, name='WAR')
            drk_em = discord.utils.get(PTfindmsg.guild.emojis, name='DRK')
            gnb_em = discord.utils.get(PTfindmsg.guild.emojis, name='GNB')

            drg_em = discord.utils.get(PTfindmsg.guild.emojis, name='DRG')
            mnk_em = discord.utils.get(PTfindmsg.guild.emojis, name='MNK')
            nin_em = discord.utils.get(PTfindmsg.guild.emojis, name='NIN')
            sam_em = discord.utils.get(PTfindmsg.guild.emojis, name='SAM')

            brd_em = discord.utils.get(PTfindmsg.guild.emojis, name='BRD')
            mch_em = discord.utils.get(PTfindmsg.guild.emojis, name='MCH')
            dnc_em = discord.utils.get(PTfindmsg.guild.emojis, name='DNC')

            smn_em = discord.utils.get(PTfindmsg.guild.emojis, name='SMN')
            blm_em = discord.utils.get(PTfindmsg.guild.emojis, name='BLM')
            rdm_em = discord.utils.get(PTfindmsg.guild.emojis, name='RDM')

            whm_em = discord.utils.get(PTfindmsg.guild.emojis, name='WHM')
            sch_em = discord.utils.get(PTfindmsg.guild.emojis, name='SCH')
            ast_em = discord.utils.get(PTfindmsg.guild.emojis, name='AST')

            async for message in PTfindmsg.channel.history(limit=10):
                if message.id == PTfindmsg_id:
                    await message.add_reaction(pld_em)
                    await message.add_reaction(war_em)
                    await message.add_reaction(drk_em)
                    await message.add_reaction(gnb_em)

                    await message.add_reaction(drg_em)
                    await message.add_reaction(mnk_em)
                    await message.add_reaction(nin_em)
                    await message.add_reaction(sam_em)

                    await message.add_reaction(brd_em)
                    await message.add_reaction(mch_em)
                    await message.add_reaction(dnc_em)

                    await message.add_reaction(smn_em)
                    await message.add_reaction(blm_em)
                    await message.add_reaction(rdm_em)

                    await message.add_reaction(whm_em)
                    await message.add_reaction(sch_em)
                    await message.add_reaction(ast_em)
            #emojiを付けたユーザーを保存、リアクション削除、かぶり検知
            #揃ったらメンションでｼｬｷｰﾝ

        # 設定されたPT募集チャンネルに送信
        else:
            await message.channel.send("PT募集用チャンネルを使ってください")

    #Partyfinder, emoji付け

    #emoji 検索
    #job_emoji = discord.utils.get(guild.emojis, name='BLM')
    #if job_emoji:
    #    await message.add_reaction(job_emoji)

client.run(str(config['bot']['BotToken']))
