from scrapdata.scrapdata import *
import time

while True:
    wheather = Scrap(['San Sebastian, ES'])
    print(wheather.get_wheather_data())
    # air pollution
    # google trends
    # twitter trends
    #
    time.sleep(60*60)