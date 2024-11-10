from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import json
import subprocess
import time
import os
import traceback  # Ensure traceback is imported for detailed error logging

ingfodacasrol = ["Green Beans","Condensed Cream of Mushroom Soup", "Fried Onions"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can specify specific origins if needed
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods like GET, POST, etc.
    allow_headers=["*"],  # Allows all headers
)

#lass ItemRequest():
@app.post("/run-scraper")
async def run_scraper(request: Request):
    data = await request.json()
    item_name = data.get("itemName", "")

    try:
        # Get the absolute path to the 'scraper' directory
        scraper_path = os.path.join(os.getcwd(), 'amazonscraper', 'amazonscraper')  # Adjust if necessary
        
        # Scrapy spider name (replace with your spider name)
        spider_name = 'peter'  # Example spider name
        output_file_path = os.path.join(scraper_path, 'output.json')
        # Run Scrapy command using subprocess
        result = subprocess.run(
            ['scrapy', 'crawl', spider_name, '-O', 'output.json'],
            cwd=scraper_path,  # Change the working directory to the scraper folder
            capture_output=True, text=True
        )
        
        print(f"Scrapy result: {result.stdout}")
        print(f"Scrapy error (if any): {result.stderr}")
        if result.returncode == 0:
            while not os.path.exists(output_file_path):
                print("Waiting for output.json to be created...")
                time.sleep(1)
            # Read the output.json file to get scraped data
            with open(output_file_path, 'r') as file:
                output_data = json.load(file)
            filtered_items = []
            for item in output_data:
                name = item.get('name','')
                price = item.get('price','')  # Assuming the price exists in the item

                if isinstance(price, str) and price.startswith('$'):
                    price = float(price[1:])  # Convert to float
                
                for keyword in ingfodacasrol:
                    if keyword.lower() in name.lower():  # Check case-insensitive
                        filtered_items.append({'name': name, 'price': price})  # Append a dictionary with name and price
                        print(filtered_items)


            return JSONResponse(content={'filtered_items': filtered_items})
        else:
            return JSONResponse(content={'status': 'error', 'output': result.stderr}, status_code=500)
    except Exception as e:
        return JSONResponse(content={'status': 'error', 'message': str(e)}, status_code=505)