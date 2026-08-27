from backend.services import ProductService

# Mock data for testing
mock_inventory = [
    {"id": 1, "name": "Test A", "category": "Electronics", "price": 100, "rating": 5, "image": ""},
    {"id": 2, "name": "Test B", "category": "Apparel", "price": 50, "rating": 3, "image": ""},
    {"id": 3, "name": "Test C", "category": "Electronics", "price": 200, "rating": 4, "image": ""},
]

def test_no_filters_returns_all():
    result = ProductService.filter_and_sort_products(mock_inventory)
    assert len(result) == 3

def test_category_filter():
    result = ProductService.filter_and_sort_products(mock_inventory, categories="Electronics")
    assert len(result) == 2
    assert all(p.category == "Electronics" for p in result)

def test_price_filter():
    result = ProductService.filter_and_sort_products(mock_inventory, min_price=60, max_price=150)
    assert len(result) == 1
    assert result[0].name == "Test A"

def test_star_rating_filter():
    result = ProductService.filter_and_sort_products(mock_inventory, min_star=4)
    assert len(result) == 2
    assert all(p.rating >= 4 for p in result)

def test_sort_by_price_asc():
    result = ProductService.filter_and_sort_products(mock_inventory, sort_by="price_asc")
    assert result[0].price == 50
    assert result[-1].price == 200

def test_combinatorial_intersect():
    # Should find Electronics, >50 price, >= 4 stars
    result = ProductService.filter_and_sort_products(
        mock_inventory, 
        categories="Electronics", 
        min_price=150, 
        min_star=4
    )
    assert len(result) == 1
    assert result[0].name == "Test C"
