import os
from time import sleep

from detection import *

MAX_RETRIES = 5


class Bot:

    def __init__(self, client, **kwargs):
        self.client = client
        self.should_post_expos = True
        self.refill_energy = False
        self.sell_gear = False
        self.stop_at = 0  # Timestamp
        os.makedirs("error_screenshots", exist_ok=True)

    def error_screenshot(self):
        screenshot = self.client.capture_screen(asarray_output=False)
        screenshot.show()

    def open_menu(self, max_retries=5):
        print("Opening battle menu...")
        retries = 0

        while retries < max_retries:
            screenshot = self.client.capture_screen()

            show_menu = locate_image(screenshot, "show_menu.png", 0.9)
            menu_expos = locate_image(screenshot, "menu_expos.png", 0.9)

            if menu_expos:
                # If we can see the expos menu, we can assume the battle menu is open
                return True

            elif show_menu:
                self.client.click(show_menu)
                sleep(1)

            else:
                retries += 1
                self.client.click((480, 270))
                sleep(1)

        raise Exception("Failed to open battle menu")

    def wait_for_battle_end(self):
        print("Waiting for battle to end...")
        bg_battle_end = None
        while not bg_battle_end:
            screenshot = self.client.capture_screen()
            bg_battle_end = locate_image(screenshot, "bg_battle_end.png", 0.9)
            if bg_battle_end:
                break
            else:
                sleep(3)

    def results_handler(self, max_retries=MAX_RETRIES):
        print("Restarting battle...")
        retries = 0

        while retries < max_retries:
            screenshot = self.client.capture_screen()

            stop_bg_battle = locate_image(screenshot, "stop_bg_battle.png", 0.8)
            cancel = locate_image(screenshot, "cancel.png", 0.9)
            expo_confirm = locate_image(screenshot, "expo_confirm.png", 0.9)
            confirm = locate_image(screenshot, "confirm.png", 0.8)
            try_again = locate_image(screenshot, "try_again.png", 0.8)
            select_team = locate_image(screenshot, "select_team.png", 0.8)

            if select_team:
                self.client.click(select_team)
                sleep(1)
                return True

            elif try_again:
                self.client.click(try_again)
                sleep(1)

            elif expo_confirm:
                self.client.click(expo_confirm)
                sleep(1)

            elif cancel:
                # Cancel friend popups
                self.client.click(cancel)
                sleep(1)

            elif confirm:
                self.client.click(confirm)
                sleep(1)

            elif stop_bg_battle:
                self.client.click(stop_bg_battle)
                sleep(1)

            else:
                retries += 1
                self.client.click((480, 270))
                sleep(3)

        raise Exception("Failed to restart battle")

    def refill_energy_handler(self, max_retries=MAX_RETRIES):
        print("Refilling energy...")
        retries = 0

        while retries < max_retries:
            screenshot = self.client.capture_screen()

            buy_energy = locate_image(screenshot, "buy_energy.png", 0.9)
            buy = locate_image(screenshot, "buy.png", 0.8)

            if buy_energy:
                self.client.click(buy_energy)
                sleep(1)

            elif buy:
                self.client.click(buy)
                sleep(1)

            else:
                retries += 1
                sleep(3)

        raise Exception("Failed to refill energy")

    def start_battle_handler(self, max_retries=MAX_RETRIES):
        # Handle popups when clicking start (e.g., "buy energy", "out of inventory", etc.)
        print("Attempting to start battle...")
        retries = 0

        while retries < max_retries:
            screenshot = self.client.capture_screen()
            buy = locate_image(screenshot, "buy.png", 0.9)
            start = locate_image(screenshot, "start.png", 0.8)
            start_bg_battle = locate_image(screenshot, "start_bg_battle.png", 0.8)

            if start_bg_battle:
                # Battle has started
                return True

            if buy:
                self.client.click(buy)
                sleep(1)

            elif start:
                self.client.click(start)
                sleep(1)

            else:
                retries += 1
                sleep(3)

        raise Exception("Failed to start battle")

    def return_to_lobby(self, max_retries=MAX_RETRIES):
        print("Returning to lobby...")
        retries = 0

        while retries < max_retries:
            screenshot = self.client.capture_screen()

            start_bg_battle = locate_image(screenshot, "start_bg_battle.png", 0.8)
            bg_battle_confirm = locate_image(screenshot, "bg_battle_confirm.png", 0.9)
            show_menu = locate_image(screenshot, "show_menu.png", 0.8)

            if show_menu:
                # If we can see the menu, we can assume we're in the lobby
                return True

            if bg_battle_confirm:
                self.client.click(bg_battle_confirm)
                sleep(1)

            elif start_bg_battle:
                self.client.click(start_bg_battle)
                sleep(1)

            else:
                retries += 1
                sleep(3)

        raise Exception("Failed to return to lobby")

    def post_expos(self, max_retries=MAX_RETRIES):
        print("Posting expos...")
        retries = 0

        while retries < max_retries:
            screenshot = self.client.capture_screen()

            menu_expos = locate_image(screenshot, "menu_expos.png", 0.8)
            to_expos = locate_image(screenshot, "to_expos.png", 0.8)
            show_expos = locate_image(screenshot, "show_expos.png", 0.8)
            embark_expos = locate_image(screenshot, "embark_expos.png", 0.8)

            if embark_expos:
                self.client.click(embark_expos)
                sleep(1)
                return True

            elif show_expos:
                self.client.click(show_expos)
                sleep(1)

            elif to_expos:
                self.client.click(to_expos)
                sleep(1)

            elif menu_expos:
                self.client.click(menu_expos)
                sleep(1)

            else:
                retries += 1
                sleep(3)

        raise Exception("Failed to post expos")

    def run(self):
        try:
            while True:
                self.wait_for_battle_end()
                self.results_handler()
                self.start_battle_handler()
                self.return_to_lobby()
                if self.should_post_expos:
                    self.open_menu()
                    self.post_expos()
                self.open_menu()
        except Exception as e:
            self.error_screenshot()
            print(f"Stopped: {e}")
