import discord
import configparser
import random

import os
import errno
import logging


#logger-------------------------------------------
client = discord.Client()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
#--------------------------------------------------

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


#PT情報保存用リスト
#PTinfo = [messageid, author, title, desc, is4ppl, allowdupe] * maxparty
PTinfo = [[0] * 6] * int(config['Settings']['maxparty'])
PTmember = [[0] * 8] * int(config['Settings']['maxparty'])
PTrole = [[0] * 3] * int(config['Settings']['maxparty'])
#______________________________________

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    print(client.user)

    #todo
    #guildを取得したい
    #client.guildsでリスト取得可能


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

    """emojiをconfigparserに入れたいと思ったけどコメントが消えてしまうので断念
    #emoji init---------------------------------------------------------------
    if message.content.startswith('!init'):
        if message.author.id == int(boss):
            pld_em = discord.utils.get(message.guild.emojis, name='PLD')
            war_em = discord.utils.get(message.guild.emojis, name='WAR')
            drk_em = discord.utils.get(message.guild.emojis, name='DRK')
            gnb_em = discord.utils.get(message.guild.emojis, name='GNB')
            config["Emojis"] = {"Pld": pld_em,
                                "War": war_em,
                                "Drk": drk_em,
                                "Gnb": gnb_em}

            with open("settings.ini", "w") as configfile:
                config.write(configfile)
            print("initiated!")
        else:
            await message.channel.send('ask boss for init')
            return
    """

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

    if message.content.startswith("!PT") or message.content.startswith("!pt"):

        #PT登録内容チェック----------------------------------------------------------
        if message.content.startswith('!PTcheck'):
            if message.author.id == int(boss):
                for i in range(len(PTinfo)):
                    await message.channel.send(str(PTinfo[i]) + "\n"
                                                + str(PTmember[i][0]) + ", "
                                                + str(PTmember[i][1]) + ", "
                                                + str(PTmember[i][2]) + ", "
                                                + str(PTmember[i][3]) + ", "
                                                + str(PTmember[i][4]) + ", "
                                                + str(PTmember[i][5]) + ", "
                                                + str(PTmember[i][6]) + ", "
                                                + str(PTmember[i][7]))
                return

            else:
                await message.channel.send("Who's there?")
                return
        #--------------------------------------------------------------------------

        # PT募集チャンネル未設定or設定チャンネル上の場合
        if (int(config['Settings']['PTfindchannel']) == 0) or (message.channel.id == int(config['Settings']['PTfindchannel'])):

            #すでに募集を立てていたらor空き募集があればreturn
            for i in range(len(PTinfo)):
                if message.author == PTinfo[i][1]:
                    return
            if PTinfo[PTnum][0] != 0:
                warn = await message.channel.send(message.author.mention + " 募集件数上限により、今は新しく募集はできません。")
                await warn.delete(delay=3)
                return

            PTdesc = message.content.split(" ")
            PTfind_txt = message.author.mention + "がPT募集中!\n> **__" + str(PTdesc[1]) + "__**\n > " + str(PTdesc[2])

            #PTinfo = [messageid, author, title, desc, is4ppl, allowdupe] * maxparty
            if "4" in PTdesc[0]:
                PTinfo[PTnum] = [0, message.author, PTdesc[1], PTdesc[2], True, False]
                PTfind_txt += "\nLight Party"
            else:
                PTinfo[PTnum] = [0, message.author, PTdesc[1], PTdesc[2], False, False]
                PTfind_txt += "\nFull Party"

            #かぶり禁止
            if ("k" or "K") in PTdesc[0]:
                PTinfo[PTnum][5] = True
                PTfind_txt += "：被りナシ"

            #募集分を組み立て、出力
            PTfindmsg = await message.channel.send(PTfind_txt)
            # @author がPT募集中!
            # <b><u>Title</b></u>
            # desc~~~

            #Messageidを取得。保存。PTmemberとPTrole初期化
            PTfindmsg_id = PTfindmsg.id
            PTfindmsg_guild = PTfindmsg.guild

            PTinfo[PTnum][0] = PTfindmsg_id
            PTmember[PTnum] = [0] * 8
            PTrole[PTnum] = [0] * 3

            print("PTnum:" + str(PTnum) + " msgid:" + str(PTfindmsg_id) + " Author:" + str(PTfindmsg.author) + " Title:" + str(PTdesc[1]) + " desc:" + str(PTdesc[2]))
            print(PTinfo)



            PTnum += 1
            if PTnum == int(config['Settings']['maxparty']):
                PTnum = 0

            #各種emoji
            jobemotelist = getjobemotes(message)
            print(jobemotelist)


            async for message in PTfindmsg.channel.history(limit=10):
                if message.id == PTfindmsg_id:
                    for job in jobemotelist:
                        await message.add_reaction(job)


        # 設定されたPT募集チャンネルに送信
        else:
            await message.channel.send("PT募集用チャンネルを使ってください")




@client.event
async def on_reaction_add(reaction, user):
    #botのreaction付け感知
    if user == client.user:
        #print("no")
        return

    #どうでもいいリアクションが追加されたときに消す
    if reaction.count == 1:
        await reaction.remove(user)
        return

    #ロールリアクションが追加されたとき
    if reaction.count > 1 and reaction.me == True:
        #PTinfo内のメッセージ判別

        inv_msg = reaction.message
        reaction_emj = reaction.emoji

        for i in range(int(config['Settings']['maxparty'])):
            #print(str(i) + "：" + str(inv_msg.id) + "：" + str(PTinfo[i][0]))
            if inv_msg.id == PTinfo[i][0]:

                """
                #reactionした人がすでにPTにいる場合
                if user in PTmember[i]:
                    warn = await inv_msg.channel.send(user.mention + "そのPTには参加済みだよ！")
                    await reaction.remove(user)
                    await warn.delete(delay=10)
                    return
                """

                jobemotelist = getjobemotes(inv_msg)

                #タンク数管理
                if (reaction_emj == jobemotelist[0]
                    or reaction_emj == jobemotelist[1]
                    or reaction_emj == jobemotelist[2]
                    or reaction_emj == jobemotelist[3]):

                    PTrole[i][0] += 1

                elif (reaction_emj == jobemotelist[4]
                    or reaction_emj == jobemotelist[5]
                    or reaction_emj == jobemotelist[6]
                    or reaction_emj == jobemotelist[7]
                    or reaction_emj == jobemotelist[8]
                    or reaction_emj == jobemotelist[9]
                    or reaction_emj == jobemotelist[10]
                    or reaction_emj == jobemotelist[11]
                    or reaction_emj == jobemotelist[12]
                    or reaction_emj == jobemotelist[13]):

                    PTrole[i][1] += 1

                elif (reaction_emj == jobemotelist[14]
                    or reaction_emj == jobemotelist[15]
                    or reaction_emj == jobemotelist[16]):

                    PTrole[i][2] += 1

                print("tankcount=" + str(PTrole[i][0]) +
                      "\ndpscount=" + str(PTrole[i][1]) +
                      "\nhealercount=" + str(PTrole[i][2]))



                #タンクが規定数以上参加していた場合残りのタンクを削除
                if (PTinfo[i][4] == True and PTrole[i][0] > 0) or PTrole[i][0] > 1:
                        for rc in inv_msg.reactions:
                            if (str(rc) == str(jobemotelist[0])
                                or str(rc) == str(jobemotelist[1])
                                or str(rc) == str(jobemotelist[2])
                                or str(rc) == str(jobemotelist[3])):
                                await rc.clear()

                        #reactionを消せてなくてオーバーしてしまったときはreacction調整だけして処理を中断
                        if (PTinfo[i][4] == True and PTrole[i][0] > 1) or PTrole[i][0] > 2:
                            await reaction.clear()
                            PTrole[i][0] -= 1
                            return

                #dpsが規定数参加していたらemote削除
                #全部ひとまとめだと消しきれないことがあったので分散させてみる
                #だめでした
                if (PTinfo[i][4] == True and PTrole[i][1] > 1) or PTrole[i][1] > 3:
                    for rc in inv_msg.reactions:
                        if (str(rc) == str(jobemotelist[4])
                            or str(rc) == str(jobemotelist[6])
                            or str(rc) == str(jobemotelist[8])
                            or str(rc) == str(jobemotelist[10])
                            or str(rc) == str(jobemotelist[12])
                            or str(rc) == str(jobemotelist[5])
                            or str(rc) == str(jobemotelist[7])
                            or str(rc) == str(jobemotelist[9])
                            or str(rc) == str(jobemotelist[11])
                            or str(rc) == str(jobemotelist[13])):
                            await rc.clear()

                    if (PTinfo[i][4] == True and PTrole[i][1] > 2) or PTrole[i][1] > 4:
                        await reaction.clear()
                        PTrole[i][1] -= 1
                        return

                #ヒーラーが規定数以上参加していた場合削除
                if (PTinfo[i][4] == True and PTrole[i][2] > 0) or PTrole[i][2] > 1:
                    for rc in inv_msg.reactions:
                        if (str(rc) == str(jobemotelist[14])
                            or str(rc) == str(jobemotelist[15])
                            or str(rc) == str(jobemotelist[16])):
                            await rc.clear()

                    if (PTinfo[i][4] == True and PTrole[i][2] > 1) or PTrole[i][2] > 2:
                        await reaction.clear()
                        PTrole[i][2] -= 1
                        return

                print("emote added, tank, dps, and healer adjusted")

                #かぶり禁止の場合押されたemoteを削除
                if PTinfo[i][5] == True:
                    await reaction.clear()

                #reactionした人のidをPTmemberに追加
                PTmember[i][PTrole[i][0] + PTrole[i][1] + PTrole[i][2] - 1] = user
                print("user stored to party list")

                #8人揃った処理
                if PTrole[i][0] + PTrole[i][1] + PTrole[i][2] > 7:
                    await inv_msg.channel.send("Full Party! \n" +
                                                        "**__" + str(PTinfo[i][2]) + "__**\n" +
                                                        PTmember[i][0].mention + " " +
                                                        PTmember[i][1].mention + " " +
                                                        PTmember[i][2].mention + " " +
                                                        PTmember[i][3].mention + " " +
                                                        PTmember[i][4].mention + " " +
                                                        PTmember[i][5].mention + " " +
                                                        PTmember[i][6].mention + " " +
                                                        user.mention)

                    #募集メッセージ削除、PTinfoをクリア
                    PTinfo[i] = [0] * 6
                    await inv_msg.delete(delay=3)

                elif PTinfo[i][4] == True and PTrole[i][0] + PTrole[i][1] + PTrole[i][2] > 3:
                    await inv_msg.channel.send("Light Party! \n" +
                                                        "**__" + str(PTinfo[i][2]) + "__**\n" +
                                                        PTmember[i][0].mention + " " +
                                                        PTmember[i][1].mention + " " +
                                                        PTmember[i][2].mention + " " +
                                                        user.mention)

                    PTinfo[i] = [0] * 6
                    await inv_msg.delete(delay=3)


#msgを渡して、鯖からエモートを取得しリスト化
def getjobemotes(msg):
    pld_em = discord.utils.get(msg.guild.emojis, name='PLD')
    war_em = discord.utils.get(msg.guild.emojis, name='WAR')
    drk_em = discord.utils.get(msg.guild.emojis, name='DRK')
    gnb_em = discord.utils.get(msg.guild.emojis, name='GNB')

    drg_em = discord.utils.get(msg.guild.emojis, name='DRG')
    mnk_em = discord.utils.get(msg.guild.emojis, name='MNK')
    nin_em = discord.utils.get(msg.guild.emojis, name='NIN')
    sam_em = discord.utils.get(msg.guild.emojis, name='SAM')

    brd_em = discord.utils.get(msg.guild.emojis, name='BRD')
    mch_em = discord.utils.get(msg.guild.emojis, name='MCH')
    dnc_em = discord.utils.get(msg.guild.emojis, name='DNC')

    smn_em = discord.utils.get(msg.guild.emojis, name='SMN')
    blm_em = discord.utils.get(msg.guild.emojis, name='BLM')
    rdm_em = discord.utils.get(msg.guild.emojis, name='RDM')

    whm_em = discord.utils.get(msg.guild.emojis, name='WHM')
    sch_em = discord.utils.get(msg.guild.emojis, name='SCH')
    ast_em = discord.utils.get(msg.guild.emojis, name='AST')


    return [pld_em, war_em, drk_em, gnb_em,
            drg_em, mnk_em, nin_em, sam_em,
            brd_em, mch_em, dnc_em,
            smn_em, blm_em, rdm_em,
            whm_em, sch_em, ast_em]



client.run(str(config['bot']['BotToken']))
