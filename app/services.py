from typing import List, Optional, Dict
from fastapi import HTTPException
from .models import Product, ProductDetails, ProductId, ProductType

products: Dict[int, Product] = {}
next_id = 1

async def get_all_products_service(type: Optional[ProductType] = None) -> List[Product]:
    """
    Retrieve all products from the in-memory store, optionally filtered by type.
    
    Args:
        type (Optional[ProductType]): The type of the products to filter by, if provided.

    Returns:
        List[Product]: A list of products, possibly filtered by the specified type.
    """
    return [product for product in products.values() if type is None or product.type == type]

async def create_product_service(product_details: ProductDetails) -> ProductId:
    """
    Create a new product in the in-memory store.

    Args:
        product_details (ProductDetails): The details of the product to create, 
                                          including name, type, and inventory count.

    Returns:
        ProductId: The ID of the newly created product.
    """
    global next_id
    product = Product(id=next_id, **product_details.dict())
    products[next_id] = product
    next_id += 1
    return ProductId(id=product.id)

async def get_product_by_id_service(product_id: int) -> Product:
    """
    Retrieve a single product by its ID from the in-memory store.

    Args:
        product_id (int): The ID of the product to retrieve.

    Returns:
        Product: The product matching the given ID.

    Raises:
        HTTPException: 404 error if no product is found with the given ID.
    """
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

async def update_product_service(product_id: int, product_details: ProductDetails) -> Product:
    """
    Update an existing product in the in-memory store.

    Args:
        product_id (int): The ID of the product to update.
        product_details (ProductDetails): The new details of the product to be updated.

    Returns:
        Product: The updated product.

    Raises:
        HTTPException: 404 error if no product is found with the given ID.
    """
    product = products.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.update_details(product_details)
    return product

async def delete_product_service(product_id: int):
    """
    Delete a product from the in-memory store by its ID.

    Args:
        product_id (int): The ID of the product to delete.

    Raises:
        HTTPException: 404 error if no product is found with the given ID.
    """
    if product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")
    del products[product_id]
