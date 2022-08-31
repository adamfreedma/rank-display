import rocket_league
import valorant
import clash_of_clans
import time
from PIL import Image
from divoom_controller import DivoomController
from PIL import Image, ImageDraw, ImageFont
from threading import Thread

def main():

    PIXOO_ADDRESS = '11:75:58:ae:8e:cc'

    pixoo = DivoomController(PIXOO_ADDRESS)


    COC_PLAYER_TAG = "#90CVPR2RP"
    EPIC_ID = "d6065524054c447780dc90335ec85bbd"
    VALORANT_NAME = "freedaddy#Daddy"
    # all periods are in seconds
    RL_UPDATE_PERIOD = 6 * 60 * 60
    COC_UPDATE_PERIOD = 60
    VALORANT_UPDATE_PERIOD = 5

    curr_time = time.time()
    last_rl_update = curr_time
    last_coc_update = 0
    last_valorant_update = 0

    valorant_rank = ""
    rl_rank = ""
    coc_heroes_progress = 0

    coc_player = clash_of_clans.CocPlayer(COC_PLAYER_TAG)
    valorant_player = valorant.ValorantPlayer(*VALORANT_NAME.split("#"))

    th = Thread(target=pixoo.run)
    th.start()

    while True:

        curr_time = time.time()

        if (curr_time - last_rl_update) > RL_UPDATE_PERIOD:
            rl_rank = rocket_league.get_rank(EPIC_ID)
        
        # if (curr_time - last_coc_update) > COC_UPDATE_PERIOD:
        #     coc_player.update_player_data()
        #     coc_heroes_progress = coc_player.heroes_progress()

        if (curr_time - last_valorant_update) > VALORANT_UPDATE_PERIOD:
            new_game, valorant_kda = valorant_player.get_kda()
            valorant_rank = valorant_player.get_rank()
            
        if new_game:
            img = Image.open('background.png')
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype(r'arial.ttf', 11)
            draw.text((0, 0), str(valorant_kda), fill=(int(100 / valorant_kda), int(100 *  valorant_kda), 0), font=font)
            img.save("kda.png")
            pixoo.cycle_set("kda", "kda.png")

        # print("valorant:", valorant_rank)
        # print("rocket_league:", rl_rank)
        # print("coc:", coc_heroes_progress)
        
        if(valorant_rank):
            filename = valorant_rank.lower().replace(' ', '')
            print("drawing", valorant_rank)
            pixoo.cycle_set("valorant", "rank-images\\" + filename + ".png")
        
        if new_game:
            pixoo.push("kda.png", 20)

        time.sleep(5)

if __name__ == "__main__":
    main()
