import rocket_league
import valorant
import clash_of_clans
import time
from PIL import Image
from divoom_controller import DivoomController
from PIL import Image, ImageDraw, ImageFont
from threading import Thread
import draw

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
        
        if (curr_time - last_coc_update) > COC_UPDATE_PERIOD:
            coc_player.update_player_data()
            coc_heroes_progress = coc_player.heroes_progress()

        if (curr_time - last_valorant_update) > VALORANT_UPDATE_PERIOD:
            valorant_player.update_match_stats()

            valorant_win = valorant_player.get_win()

            valorant_kda = valorant_player.get_kda()
            valorant_rank = valorant_player.get_rank()
            


        if valorant_kda:
            color = (int(100 / valorant_kda), int(100 *  valorant_kda), 0)
        else:
            color = (255, 0, 0)
        draw.draw_text(valorant_kda, color, "kda.png")
        pixoo.cycle_set("kda", "kda.png")

        if coc_heroes_progress:
            draw.draw_text(coc_heroes_progress, (255, 255, 255), "heroes.png", background_path="crown.png", starting_pos=(0, 5))
            pixoo.cycle_set("coc", "heroes.png")
        
        if valorant_rank:
            filename = valorant_rank.lower().replace(' ', '')
            pixoo.cycle_set("valorant", "rank-images\\" + filename + ".png")
        
        if valorant_player.new_game:
            if valorant_win:
                pixoo.push("win_screen.gif", 20)

        time.sleep(5)

if __name__ == "__main__":
    main()
