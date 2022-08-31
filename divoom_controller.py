from time import sleep
from divoom import Pixoo
from queue import Queue
import time


class DivoomController:

    DEFAULT_DURATION = 5

    def __init__(self, mac_address) -> None:
        
        self.pixoo = Pixoo(mac_address)
        self.pixoo.connect()
        # (path, duration)
        self.picture_queue = Queue()
        
        self.cycle = []
        self.cycle_queue = {}
        self.cycle_index = 0


    def push(self, path, duration=DEFAULT_DURATION):

        self.picture_queue.put((path, duration))


    def cycle_set(self, frame_name, frame_path, frame_duration=DEFAULT_DURATION):

        if frame_name not in self.cycle:
            self.cycle.append(frame_name)

        self.cycle_queue[frame_name] = (frame_path, frame_duration)

    def run(self):

        while True:

            if not self.picture_queue.empty():
                path, duration = self.picture_queue.get()

                self.pixoo.draw_pic(path)
                print(duration)
                time.sleep(duration)

            elif len(self.cycle) > 0:
                path, duration = self.cycle_queue[self.cycle[self.cycle_index % len(self.cycle)]]
                self.pixoo.draw_pic(path)
                self.cycle_index += 1

                time.sleep(duration)

            else:

                time.sleep(5)