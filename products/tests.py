from unittest.mock import MagicMock

import pytest

from buying.models import CartItemEntity
from products.models import ProductEntity, BrowsingHistory, PurchaseHistory


@pytest.fixture
def mock_redis(mocker):
    return mocker.patch('products.managers.redis.Redis')


@pytest.fixture
def mock_database(mocker):
    # Mocking the ProductEntity and related models
    mock_product_entity = MagicMock(spec=ProductEntity)
    mock_product_entity.id = 1
    mock_product_entity.name = "Product 1"
    mock_product_entity.category = "Category 1"

    mock_product_entity_2 = MagicMock(spec=ProductEntity)
    mock_product_entity_2.id = 2
    mock_product_entity_2.name = "Product 2"
    mock_product_entity_2.category = "Category 2"

    mock_browsing_history = MagicMock(spec=BrowsingHistory)
    mock_browsing_history.user.id = 1
    mock_browsing_history.product_id = 1

    mock_purchase_history = MagicMock(spec=PurchaseHistory)
    mock_purchase_history.user.id = 1
    mock_purchase_history.product_id = 1

    mock_cart_item = MagicMock(spec=CartItemEntity)
    mock_cart_item.cart.user.id = 1
    mock_cart_item.product_id = 2

    mocker.patch('products.models.ProductEntity.objects.all', return_value=[mock_product_entity, mock_product_entity_2])
    mocker.patch('products.models.BrowsingHistory.objects.filter', return_value=[mock_browsing_history])
    mocker.patch('products.models.PurchaseHistory.objects.filter', return_value=[mock_purchase_history])
    mocker.patch('products.models.CartItemEntity.objects.filter', return_value=[mock_cart_item])

    return {
        'mock_product_entity': mock_product_entity,
        'mock_product_entity_2': mock_product_entity_2,
        'mock_browsing_history': mock_browsing_history,
        'mock_purchase_history': mock_purchase_history,
        'mock_cart_item': mock_cart_item,
    }
