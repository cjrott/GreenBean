from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import subprocess
import time
import os
import traceback  

ingfodacasrol = ["Green Beans","Condensed Cream of Mushroom Soup", "Fried Onions"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)


@app.post("/run-scraper")
async def run_scraper(request: Request):
    data = await request.json()
    item_name = data.get("itemName", "")

    try:
        scraper_path = os.path.join(os.getcwd(), 'amazonscraper', 'amazonscraper')  
        spider_name = 'peter'  
        output_file_path = os.path.join(scraper_path, 'output.json')
        result = subprocess.run(
            ['scrapy', 'crawl', spider_name, '-O', 'output.json'],
            cwd=scraper_path,  
            capture_output=True, text=True
        )
        
        print(f"Scrapy result: {result.stdout}")
        print(f"Scrapy error (if any): {result.stderr}")
        if result.returncode == 0:
            while not os.path.exists(output_file_path):
                print("Waiting for output.json to be created...")
                time.sleep(1)
            with open(output_file_path, 'r') as file:
                output_data = json.load(file)
            filtered_items = []
            beenitem = {"name": "", "price": float('inf')}  
            mushitem = {"name": "", "price": float('inf')}
            lastone = {"name": "", "price": float('inf')}
            for item in output_data:
                name = item.get('name','')
                price = item.get('price','')  

                if isinstance(price, str) and price.startswith('$'):
                    try:
                        price = float(price[1:])  
                    except ValueError:
                        continue  

                    for keyword in ingfodacasrol:
                        if keyword.lower() in name.lower():  
                            if keyword.lower() == ingfodacasrol[0].lower():  # Green Beans
                                if price < beenitem["price"] or beenitem["price"] == float('inf'):
                                    #filtered_items.append({'name': name, 'price': price})
                                    beenitem["name"] = name 
                                    beenitem["price"] = price
                                    
                            elif keyword.lower() == ingfodacasrol[1].lower():  
                                 if price < mushitem["price"]or mushitem["price"] == float('inf'):
                                    #filtered_items.append({'name': name, 'price': price})
                                    mushitem["name"] = name 
                                    mushitem["price"] = price
                            elif keyword.lower() == ingfodacasrol[2].lower():  # Fried Onions
                                if price < lastone["price"]or lastone["price"] == float('inf'):
                                    #filtered_items.append({'name': name, 'price': price})
                                    lastone["name"] = name 
                                    lastone["price"] = price
            p = beenitem["price"] + mushitem["price"] + lastone["price"]                    
            filtered_items.append({'name': beenitem["name"], 'price': beenitem["price"]}) 
            filtered_items.append({'name': mushitem["name"], 'price': mushitem["price"]})
            filtered_items.append({'name': lastone["name"], 'price': lastone["price"]})
            filtered_items.append({'name': "Total", 'price': p})
            print(filtered_items)


            return JSONResponse(content={'filtered_items': filtered_items})
        else:
            return JSONResponse(content={'status': 'error', 'output': result.stderr}, status_code=500)
    except Exception as e:
        return JSONResponse(content={'status': 'error', 'message': str(e)}, status_code=505)



