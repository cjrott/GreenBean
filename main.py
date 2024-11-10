from fastapi import FastAPI
from fastapi.responses import JSONResponse
import subprocess
import os
import traceback  # Ensure traceback is imported for detailed error logging

app = FastAPI()
class ItemRequest(BaseModle):
    item: str
@app.post("/run-scraper")
async def run_scraper(request:ItemRequest):
    item_name = request.item
    try:
        # Get the absolute path to the 'scraper' directory
        scraper_path = os.path.join(os.getcwd(), 'amazonscraper', 'amazonscraper')  # Adjust if necessary
        
        # Scrapy spider name (replace with your spider name)
        spider_name = 'peter'  # Example spider name
        
        # Run Scrapy command using subprocess
        result = subprocess.run(
            ['scrapy', 'crawl', spider_name, '-O', 'output.json'],
            cwd=scraper_path,  # Change the working directory to the scraper folder
            capture_output=True, text=True
        )
        
        print(f"Scrapy result: {result.stdout}")  # Log output of the subprocess
        
        # Return the output from Scrapy
        if result.returncode == 0:
            return JSONResponse(content={'status': 'success', 'output': result.stdout})
        else:
            return JSONResponse(content={'status': 'error', 'output': result.stderr}, status_code=500)
    
    except Exception as e:
        error_message = f"Error: {str(e)}\n{traceback.format_exc()}"
        print(error_message)  # Log the error message and traceback
        return JSONResponse(content={'status': 'error', 'message': error_message}, status_code=500)
