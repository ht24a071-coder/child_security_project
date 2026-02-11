# スペシャルイベント：不審者遭遇時の対処フローを学ぶ（いかのおすし）
# イベント登録は def_mapdat.rpy の event_pools で管理

label special_e_encounter_flow:
    show stranger with dissolve
    stranger "ちょっとちょっと、{rb}君{/rb}{rt}きみ{/rt}～"
    stranger "ちょっとこっちに{rb}来{/rb}{rt}き{/rt}てくれない？"

    menu:
        "はい、{rb}何{/rb}{rt}なん{/rt}ですか？（{rb}近{/rb}{rt}ちか{/rt}づく）":
            stranger "（にやり）いい{rb}子{/rb}{rt}こ{/rt}だね…"
            
            "{i}{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}に{rb}近{/rb}{rt}ちか{/rt}づくのは{rb}危{/rb}{rt}あぶ{/rt}ないよ！{/i}"
            "{i}「いかのおすし」を{rb}思{/rb}{rt}おも{/rt}い{rb}出{/rb}{rt}だ{/rt}そう！{/i}"
            "{i}・いか（{rb}行{/rb}{rt}い{/rt}かない）{/i}"
            "{i}・の（{rb}乗{/rb}{rt}の{/rt}らない）{/i}"
            "{i}・お（{rb}大声{/rb}{rt}おおごえ{/rt}を{rb}出{/rb}{rt}だ{/rt}す）{/i}"
            "{i}・す（すぐ{rb}逃{/rb}{rt}に{/rt}げる）{/i}"
            "{i}・し（{rb}知{/rb}{rt}し{/rt}らせる）{/i}"

        "（{rb}無視{/rb}{rt}むし{/rt}して{rb}歩{/rb}{rt}ある{/rt}き{rb}続{/rb}{rt}つづ{/rt}ける）":
            $ update_score(15)
            stranger "あら、{rb}行{/rb}{rt}い{/rt}っちゃうの…"
            hide stranger with dissolve
            "{i}よくできました！{rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}には{rb}近{/rb}{rt}ちか{/rt}づかないのが{rb}正解{/rb}{rt}せいかい{/rt}です。{/i}"
            "{i}{rb}声{/rb}{rt}こえ{/rt}をかけられても{rb}無視{/rb}{rt}むし{/rt}して、{rb}安全{/rb}{rt}あんぜん{/rt}な{rb}場所{/rb}{rt}ばしょ{/rt}に{rb}行{/rb}{rt}い{/rt}きましょう。{/i}"
            return

        "（{rb}大{/rb}{rt}おお{/rt}きな{rb}声{/rb}{rt}こえ{/rt}で）{rb}助{/rb}{rt}たす{/rt}けてー！":
            $ update_score(20)
            stranger "うわっ…！（{rb}逃{/rb}{rt}に{/rt}げていく）"
            hide stranger with dissolve
            "{i}いい{rb}判断{/rb}{rt}はんだん{/rt}だね！{/i}"
            "{i}{rb}怖{/rb}{rt}こわ{/rt}いと{rb}思{/rb}{rt}おも{/rt}ったら{rb}大{/rb}{rt}おお{/rt}きな{rb}声{/rb}{rt}こえ{/rt}を{rb}出{/rb}{rt}だ{/rt}して、{rb}周{/rb}{rt}まわ{/rt}りの{rb}人{/rb}{rt}ひと{/rt}に{rb}助{/rb}{rt}たす{/rt}けを{rb}求{/rb}{rt}もと{/rt}めよう！{/i}"
            "{i}{rb}近{/rb}{rt}ちか{/rt}くのお{rb}店{/rb}{rt}みせ{/rt}や「こども110{rb}番{/rb}{rt}ばん{/rt}の{rb}家{/rb}{rt}いえ{/rt}」に{rb}逃{/rb}{rt}に{/rt}げ{rb}込{/rb}{rt}こ{/rt}むのも{rb}大事{/rb}{rt}だいじ{/rt}だよ。{/i}"
            return

    hide stranger with dissolve
    
    "{i}{rb}次{/rb}{rt}つぎ{/rt}からは「いかのおすし」を{rb}思{/rb}{rt}おも{/rt}い{rb}出{/rb}{rt}だ{/rt}してね！{/i}"
    "{i}・いか（{rb}行{/rb}{rt}い{/rt}かない）- {rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}についていかない{/i}"
    "{i}・の（{rb}乗{/rb}{rt}の{/rt}らない）- {rb}知{/rb}{rt}し{/rt}らない{rb}人{/rb}{rt}ひと{/rt}の{rb}車{/rb}{rt}くるま{/rt}に{rb}乗{/rb}{rt}の{/rt}らない{/i}"
    "{i}・お（{rb}大声{/rb}{rt}おおごえ{/rt}を{rb}出{/rb}{rt}だ{/rt}す）- 「{rb}助{/rb}{rt}たす{/rt}けて！」と{rb}大{/rb}{rt}おお{/rt}きな{rb}声{/rb}{rt}こえ{/rt}を{rb}出{/rb}{rt}だ{/rt}す{/i}"
    "{i}・す（すぐ{rb}逃{/rb}{rt}に{/rt}げる）- {rb}安全{/rb}{rt}あんぜん{/rt}な{rb}場所{/rb}{rt}ばしょ{/rt}にすぐ{rb}逃{/rb}{rt}に{/rt}げる{/i}"
    "{i}・し（{rb}知{/rb}{rt}し{/rt}らせる）- {rb}大人{/rb}{rt}おとな{/rt}に{rb}知{/rb}{rt}し{/rt}らせる{/i}"

    return
