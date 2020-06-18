# FF14Party-bot
Discord用FF14もパーティー募集ごっこをするbot
現在1bot1サーバー用


#通常コマンド
!PT "募集タイトル" "募集文"
で8人PTを募集可能。間は半角スペースのみ

!PT4 "募集タイトル" "募集文"
で4人PTを募集。

#管理者機能
settings.iniにDiscordのSetting＞Appearance＞Advanced＞Developer Modeをオンにして、サーバー上のメンバーリストから自分を右クリック、Copy IDで得られるIDを入力すると一部コマンドが使えるようになります。

!PTcheck
現在アクティブな募集とそれの参加者をリスト出力。

!shutdown
botをシャットダウン

# todo
募集分にかぶり禁止とpt人数記載
強制出発コマンド
募集削除コマンド
!help
これ
ちゃんとreactionを消す処理
await create_custom_emoji(*, name, image, roles=None, reason=None)
