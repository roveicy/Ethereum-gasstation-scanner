import asyncio
from time import sleep
from polygonscan import polygonscan
from ftmscan import ftmscan
from snowtrace import snowtrace
from bscscan import bscscan

async def main():
    while 1:
        try:
            await polygonscan.main()
            await ftmscan.main()
            await snowtrace.main()
            await bscscan.main()
        except TimeoutError:
            pass
        sleep(30)

asyncio.get_event_loop().run_until_complete(main())