#! /usr/bin/env python3
#
# test for automatic varibright->monobright conversion of messages
# try changing varibright to True for smooth brightness transition
#

import asyncio
import monome


class MonobrightGrid(monome.Grid):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.varibright = False


class MonobrightApp(monome.GridApp):
    def __init__(self):
        grid = MonobrightGrid()
        super().__init__(grid)

    async def light(self, x, y):
        for i in range(16):
            self.grid.led_level_set(x, y, i)
            await asyncio.sleep(0.1)

    def on_grid_key(self, x, y, s):
        if s == 1:
            asyncio.ensure_future(self.light(x, y))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    monobright_app = MonobrightApp()

    def serialosc_device_added(id, type, port):
        print('connecting to {} ({})'.format(id, type))
        asyncio.ensure_future(monobright_app.grid.connect('127.0.0.1', port))

    serialosc = monome.SerialOsc()
    serialosc.device_added_event.add_handler(serialosc_device_added)

    loop.run_until_complete(serialosc.connect())

    loop.run_forever()
