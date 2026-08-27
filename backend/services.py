from typing import List, Optional
from .schemas import Product
from .database import get_all_products

class ProductService:
    @staticmethod
    def filter_and_sort_products(
        categories: Optional[str] = None,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_star: Optional[int] = None,
        sort_by: Optional[str] = None
    ) -> List[Product]:
        """
        Combinatorial Intersect Filtering Array Logic.
        Extracted to a service layer for clean architecture.
        """
        cat_list = categories.split(",") if categories else []
        filtered_data = []
        
        # 1. Fetch the master product item inventory array from the DB
        inventory = get_all_products()
        
        # 2. Comprehensive search loop over the array
        for item in inventory:
            # Category Filter
            if cat_list and item["category"] not in cat_list:
                continue
                
            # Price Filter
            if min_price is not None and item["price"] < min_price:
                continue
            if max_price is not None and item["price"] > max_price:
                continue
                
            # Star Rating Filter
            if min_star is not None and item["rating"] < min_star:
                continue
                
            # If all criteria met, map to Pydantic model for validation
            filtered_data.append(Product(**item))
            
        # The Vibe Check: Sort By Logic
        if sort_by == "price_asc":
            filtered_data.sort(key=lambda x: x.price)
        elif sort_by == "price_desc":
            filtered_data.sort(key=lambda x: x.price, reverse=True)
        elif sort_by == "rating_desc":
            filtered_data.sort(key=lambda x: x.rating, reverse=True)
            
        # Graceful Null Handling: if no filters applied, returns the full set.
        return filtered_data
