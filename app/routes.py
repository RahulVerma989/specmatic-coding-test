from fastapi import APIRouter, HTTPException
from typing import List, Optional
from .models import Product, ProductDetails, ProductId, ProductType
from .services import (
    get_all_products_service,
    create_product_service,
    get_product_by_id_service,
    update_product_service,
    delete_product_service,
)

router = APIRouter()

@router.get("/products", response_model=List[Product], tags=["Products"])
async def get_products(type: Optional[ProductType] = None):
    """
    Retrieve a list of products, optionally filtered by product type.

    Args:
        type (Optional[ProductType]): The type of products to filter by. If not specified,
                                      all products are returned.

    Returns:
        List[Product]: A list of products that match the given type or all products if no type is specified.
    """
    return await get_all_products_service(type)

@router.post("/products", response_model=ProductId, status_code=201, tags=["Products"])
async def create_product(product_details: ProductDetails):
    """
    Create a new product and add it to the store.

    Args:
        product_details (ProductDetails): The details of the product to create.

    Returns:
        ProductId: The ID of the newly created product.
    """
    return await create_product_service(product_details)

@router.get("/products/{product_id}", response_model=Product, tags=["Products"])
async def get_product_by_id(product_id: int):
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): The unique identifier of the product to retrieve.

    Returns:
        Product: The requested product if found.

    Raises:
        HTTPException: 404 error if no product is found with the given ID.
    """
    return await get_product_by_id_service(product_id)

@router.put("/products/{product_id}", response_model=Product, tags=["Admin"])
async def update_product(product_id: int, product_details: ProductDetails):
    """
    Update an existing product with new details.

    Args:
        product_id (int): The unique identifier of the product to update.
        product_details (ProductDetails): The new details for the product.

    Returns:
        Product: The updated product.

    Raises:
        HTTPException: 404 error if no product is found with the given ID.
    """
    return await update_product_service(product_id, product_details)

@router.delete("/products/{product_id}", status_code=204, tags=["Admin"])
async def delete_product(product_id: int):
    """
    Delete a product from the store by its ID.

    Args:
        product_id (int): The unique identifier of the product to delete.

    Raises:
        HTTPException: 404 error if no product is found with the given ID.
    """
    await delete_product_service(product_id)
