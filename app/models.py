from pydantic import BaseModel, StrictInt, validator
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

    The inventory field is validated to ensure it is an integer between 1 and 9999, inclusive.
    """
    name: str
    type: ProductType
    inventory: StrictInt  # Ensure only integers are accepted

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
