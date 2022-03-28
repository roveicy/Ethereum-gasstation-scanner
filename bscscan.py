import asyncio
from datetime import datetime
import pymongo
from pyppeteer import launch
from os.path import exists
from time import sleep

class bscscan:
    def get_db_mongo(c):
        # CONNECT:
        client = pymongo.MongoClient("mongodb://%s:%s@%s:27017/" % ("root", "password", "localhost"))
        db = client.iot
        mycol = db["bscscan"]

        # INSERT DOCUMENT:    
        mydict = { "date_time": c[6], "standardgas": c[0], "fastgas": c[1], "rapidgas": c[2], "pendingcount": c[3], "avgtxnsperblock": c[4], "avgnetworkutilization": c[5] }
        mycol.insert_one(mydict)

        # CLEAN DOCUMENTS:
        # print("cleaning")
        # mycol.delete_many({})

        # PRINT DOCUMENTS:
        # cursor = mycol.find({})
        # for document in cursor:
        #       print(document)

        return db

    async def csv_insert(column):
        if not exists("bscscan.csv"):
            with open('bscscan.csv','a+') as fd:
                fd.writelines("date_time,standardgas,fastgas,rapidgas,pendingcount,avgtxnsperblock,avgnetworkutilization\n")
        else:
            with open('bscscan.csv','a') as fd:
                fd.writelines("{},{},{},{},{},{},{}\n".format(column[6], column[0], column[1], column[2], column[3], column[4], column[5]))

    async def scrap(page):
        # SCRAPE WEBSITE:
        columns = []
        try:
            column_1 = await page.waitForSelector("#standardgas")
            columns.append(await page.evaluate('(element) => element.textContent', column_1))
            column_2 = await page.waitForSelector("#fastgas")
            columns.append(await page.evaluate('(element) => element.textContent', column_2))
            column_3 = await page.waitForSelector("#rapidgas")
            columns.append(await page.evaluate('(element) => element.textContent', column_3))
            column_4 = await page.waitForSelector("#pendingcount > b")
            columns.append(await page.evaluate('(element) => element.textContent', column_4)) 
            column_5 = await page.waitForSelector("#avgtxnsperblock > b")
            columns.append(await page.evaluate('(element) => element.textContent', column_5))    
            column_6 = await page.waitForSelector("#avgnetworkutilization > b")
            columns.append(await page.evaluate('(element) => element.textContent', column_6))    
            now = datetime.now()    
            columns.append(now.strftime("%Y-%m-%d %H:%M:%S"))   
            print("Bscscan:", columns)
            await bscscan.csv_insert(columns) 
            bscscan.get_db_mongo(columns)
        except:
            pass

    async def main():
        # MAIN LOOP:
        url = "https://bscscan.com/gastracker"
        browser = await launch(headless = True, defaultViewport = None, args=["--start-maximized", '--disable-blink-features=AutomationControlled'])
        page = await browser.newPage()
        print("Scrapping bscscan...")
        await page.goto(url)
        await bscscan.scrap(page)
        await browser.close()

    # asyncio.get_event_loop().run_until_complete(main())