from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import List, Optional
import json
import os
import logging

# Relative imports from our new architecture
from .schemas import Product
from .services import ProductService

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="VibeStore API", version="1.0.0")

# Setup paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")



# Mount static files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def read_root():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/api/products", response_model=List[Product])
def get_products(
    categories: Optional[str] = Query(None, description="Comma separated categories"),
    min_price: Optional[float] = Query(None, description="Minimum price"),
    max_price: Optional[float] = Query(None, description="Maximum price"),
    min_star: Optional[int] = Query(None, description="Minimum star rating (1-5)"),
    sort_by: Optional[str] = Query(None, description="Sort criteria")
):
    """
    API Router: Responsible ONLY for receiving requests and returning responses.
    Business logic is delegated to the ProductService.
    """
    logger.info(f"Incoming filter request: categories={categories}, min_price={min_price}, max_price={max_price}, min_star={min_star}, sort_by={sort_by}")
    
    return ProductService.filter_and_sort_products(
        categories=categories,
        min_price=min_price,
        max_price=max_price,
        min_star=min_star,
        sort_by=sort_by
    )
