def main():
    print('''
        *******************************************************************************
                |                   |                  |                     |
        _________|________________.=""_;=.______________|_____________________|_______
        |                   |  ,-"_,=""     `"=.|                  |
        |___________________|__"=._o`"-._        `"=.______________|___________________
                |                `"=._o`"=._      _`"=._                     |
        _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
        |                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
        |___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
                |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
        _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
        |                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
        |___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
        ____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
        /______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
        ____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
        /______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
        ____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
        /______/______/______/______/______/______/______/______/______/______/______/_
        *******************************************************************************
        ''')

    print("Welcome to Treasure Island.\nYour mission is to find treasure.")
    
    #1st screen
    print("You start at a crossroad. Which way do you want to go? Type \"left\" or \"right\"")
    user_input = 0
    while user_input == 0:
        user_input = (input()).lower()
        if  user_input not in ["right","left"]:
            print("You typed the wrong instruction. Try again.\nType \"left\" or \"right\"")
            user_input=0
    
    #1st death
    if user_input == "right":
        print('''
                            _.--....
                 _....---;:'::' ^__/
               .' `'`___....---=-'`
              /::' (`
              \\'   `:.
               `\::.  ';-"":::-._  \{\}
            _.--'`\:' .'`-.`'`.' `{I}
         .-' `' .;;`\::.   '. _: {-I}`\\
       .'  .:.  `:: _):::  _;' `{=I}.:|
      /.  ::::`":::` ':'.-'`':. {_I}::/
      |:. ':'  :::::  .':'`:. `'|':|:'
       \:   .:. ''\' .:| .:, _:./':.|
        '--.:::...---'\:'.:`':`':./
                       '-::..:::-'
                       ''')
        print("You just found a poisonous snake. Unfortunately you reacted too late and it bit you. Without any antidote, you died. Game over")
        
    # 2nd Screen
    if user_input == "left":
        print('''
                                  _
                      .=========.%88,
                     /_,-.___.-._\88%
                   o8| [_]/o\[_] |7'
               i=I8%@|____|_|____|I=I=I=i
              |/,*`*,*`**'/ \      ,-'`.\|
             |/          /...\   (__.-._)\|
             ||||||||||||TTTTT|||||||||||||hjw
             """"""""""""HHHHH"""""""""""""
             ''')
        print("You arrived at a small cottage. You can choose to \"enter\" or \"continue\" on your path.")
        
        user_input = 0
        while user_input == 0:
            user_input = (input()).lower()
            if  user_input not in ["enter","continue"]:
                print("You typed the wrong instruction. Try again.\nType \"enter\" or \"continue\"")
                user_input=0
            
            #2nd death    
            if user_input == "enter":
                print('''
                _..--.._       _..--.      _..--..
                ,'      ,'`.   ,','.--.\   ,' \   `.`.
                /  /    /  /|  : : /  _ \:  |\  \    \ \\
            /  :    :  /`.  | |:| ,'' _``. \\
            | ,;,   .  `:\ _:   | `,/_\.   :`/;'  ,   .:\ )
            `'/'   _ \   \:\(  _|__`>_/`' /(:/   /     .\` 
            /:  .'  ,`.._|_\\'  ( _=`;._//_|_..'`      \\
            :: /   '|    (__=`, :`||| `,.__)     \      :
            | \           \`.\\__\;|| //`|/       :     |
            |  `.._____.-,`'| \\___||// /`-._           |
            :         | : ,<''_\\,.|//_`>.  :`._       ;:
            \         ; ; )`-..______..-'(  :\  `-.__.' /
            ;        / /|:                : | `.._____.':
            :      _.' / ||                | |   `.       :
            :  _.-'   /  ::                ; :     `-.____;
            \;     ,'   ( \              /  )\          /
            ,'    ,'____,' ,`-,.______..-') (__\        _`.
            (___..'>_>____`.`.'._)_\_>._)-' ,'___`._________)
                    
                    ''')
                print("You found a group of witches inside. They immediatly cursed you and turned you into a pig.\nMay this be a lesson not to wander into someone else's home. Game Over")
            
            #3rd Screen
            if user_input == "continue":
                print('''
            mm###########mmm
            m####################m
        m#####`"#m m###"""'######m
        ######*"  "   "   "mm#######
    m####"  ,             m"#######m
    m#### m*" ,'  ;     ,   "########m
    ####### m*   m  |#m  ;  m ########
    |######### mm#  |####  #m##########|
    ###########|  |######m############
    "##########|  |##################"
    "#########  |## /##############"
        ########|  # |/ m###########
        "#######      ###########"
            """"""       """""""""
            ''')
                print("You arrived at a beach. You can choose to \"dig\" here or to \"swim\" to a neighbouring island.")
                user_input = 0
                while user_input == 0:
                    user_input = (input()).lower()
                    if  user_input not in ["dig","swim"]:
                        print("You typed the wrong instruction. Try again.\nType \"dig\" or \"swim\"")
                        user_input=0
                    
                    #3rd death
                    if user_input == "swim":
                        print('''
                                        ,-
                                    ,'::|
                                    /::::|
                                    ,'::::o\                                      _..
                ____........-------,..::?88b                                  ,-' /
        _.--"""". . . .      .   .  .  .  ""`-._                           ,-' .;'
        <. - :::::o......  ...   . . .. . .  .  .""--._                  ,-'. .;'
        `-._  ` `":`:`:`::||||:::::::::::::::::.:. .  ""--._ ,'|     ,-'.  .;'
            """_=--       //'doo.. ````:`:`::::::::::.:.:.:. .`-`._-'.   .;'
                ""--.__     P(       \               ` ``:`:``:::: .   .;'
                        "\""--.:-.     `.                             .:/
                        \. /    `-._   `.""-----.,-..::(--"".\""`.  `:\\
                        `P         `-._ \          `-:\          `. `:\\
                                        ""            "            `-._)
                                        ''')
                        print("There are sharks in the water!!! You tried to rush back, but you are helpless against a shark's speed. Game Over")
                    
                    
                    #Final Screen
                    if user_input == "dig":
                        print('''
                              
                                    _.--.
                                _.-'_:-'||
                            _.-'_.-::::'||
                    _.-:'_.-::::::'  ||
                    .'`-.-:::::::'     ||
                    /.'`;|:::::::'      ||_
                ||   ||::::::'     _.;._'-._
                ||   ||:::::'  _.-!oo @.!-._'-.
                \\'.  ||:::::.-!()oo @!()@.-'_.|
                    '.'-;|:.-'.&$@.& ()$%-'o.'\\U||
                    `>'-.!@%()@'@_%-'_.-o _.|'||
                    ||-._'-.@.-'_.-' _.-o  |'||
                    ||=[ '-._.-\\U/.-'    o |'||
                    || '-.]=|| |'|      o  |'||
                    ||      || |'|        _| ';
                    ||      || |'|    _.-'_.-'
                    |'-._   || |'|_.-'_.-'
                        '-._'-.|| |' `_.-'
                            '-.||_/.-'
''')
                        print("Congratulations, you found the treasure!")
if __name__ == "__main__":
    main()