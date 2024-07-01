from pydantic import BaseModel, StrictInt, validator, StrictFloat, Field
from typing import Optional
from enum import Enum


class ProductType(str, Enum):
    """
    Enumeration for Product Type with restricted values.

    Attributes:
        BOOK: Represents a book product.
        FOOD: Represents a food product.
        GADGET: Represents a gadget product.
        OTHER: Represents any other type of product.
    """
    BOOK = "book"
    FOOD = "food"
    GADGET = "gadget"
    OTHER = "other"

class ProductDetails(BaseModel):
    """
    Base model for product details, capturing common properties shared by products.

    Attributes:
        name (str): The name of the product.
        type (ProductType): The type of the product, restricted to the ProductType enum.
        inventory (StrictInt): The quantity of the product in stock, must be an integer.
        cost Optional(StrictFloat): The cost of the product in USD, must be an float. Default is 0.00 and value >= 0.00 and value <= 999.99

    The inventory field is validated to ensure it is an integer between 1 and 9999, inclusive.
    """
    name: str
    type: ProductType
    inventory: StrictInt  # Ensure only integers are accepted
    cost: Optional[StrictFloat] = Field(default=0.00, le=999.99, ge=0.00)

    @validator('inventory')
    def check_inventory(cls, v):
        """
        Validate that the inventory is an integer within the specified range.

        Args:
            v (int): The inventory value to validate.

        Returns:
            int: The validated inventory value.

        Raises:
            ValueError: If the inventory is not an integer or not within the required range.
        """
        if not isinstance(v, int) or isinstance(v, bool):
            raise ValueError('Inventory must be an integer')
        if v < 1 or v > 9999:
            raise ValueError('Value should be greater than 1 and less than 9999')
        return v
    
    @validator('cost', pre=True, always=True)
    def check_cost(cls, v):
        """
        Validate that the cost is an float within the specified range.

        Args:
            v (float): The cost value to validate.

        Returns:
            float: The validated inventory value.

        Raises:
            ValueError: If the inventory is None.
        """      
        if v is None:
            raise ValueError('Cost must not be null')
        return v

class Product(ProductDetails):
    """
    Product model extending ProductDetails with a unique identifier.

    Attributes:
        id (int): The unique identifier for the product.
    """
    id: int
    
    def update_details(self, new_details: ProductDetails):
        """
        Updates the product details with new information.

        Args:
            new_details (ProductDetails): An object containing the new details for the product.
        """
        for field, value in new_details.dict(exclude_unset=True).items():
            setattr(self, field, value)

class ProductId(BaseModel):
    """
    Model for representing a product's ID.

    Attributes:
        id (int): The unique identifier of the product.
    """
    id: int
