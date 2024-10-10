import sys
import asyncio

from src.core import Fintopio
from src.deeplchain import log, mrh, _clear as ve, _banner as ge

if __name__ == "__main__":
    ve(), ge()
    try:
        fintopio = Fintopio()
        asyncio.run(fintopio.main())
    except KeyboardInterrupt as e:
        log(mrh + f"Stopping due to keyboard interrupt.")
        sys.exit()