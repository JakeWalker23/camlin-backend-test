import pytest
from unittest.mock import patch, AsyncMock
from src.services.wallet_service import WalletService
from src.models.wallet import Wallet

@pytest.mark.asyncio
class TestWalletService:
    @patch("src.services.wallet_service.fetch_all_currencies")
    @patch("src.services.wallet_service.fetch_exchange_rates", new_callable=AsyncMock)
    async def test_get_wallet(self, mock_fetch_exchange_rates, mock_fetch_all_currencies):
        mock_fetch_all_currencies.return_value = {"USD": 10.0, "PLN": 20.0}
        mock_fetch_exchange_rates.return_value = {"USD": 4.0, "PLN": 1.0}

        wallet_service = WalletService()
        wallet = await wallet_service.get_wallet()

        assert wallet.holdings == {"USD": 10.0, "PLN": 20.0}
        assert wallet.pln_holdings == {"USD": 40.0, "PLN": 20.0}
        assert wallet.total_pln == 60.0
        assert isinstance(wallet, Wallet)

    @patch("src.services.wallet_service.add_currency_amount")
    async def test_add_currency_success(self, mock_add_currency_amount):
        mock_add_currency_amount.return_value = None
        
        service = WalletService()
        await service.add_currency_to_wallet("USD", 10.5)

        mock_add_currency_amount.assert_called_once_with("USD", 10.5)

    @patch("src.services.wallet_service.add_currency_amount")
    async def test_add_currency_raises_value_error(self, mock_add_currency_amount):
        mock_add_currency_amount.side_effect = ValueError("Cannot add negative amount")
        
        service = WalletService()

        with pytest.raises(ValueError, match="Cannot add negative amount"):
            await service.add_currency_to_wallet("USD", -5.0)
    
    @patch("src.services.wallet_service.subtract_currency_from_wallet")
    async def test_remove_currency_success(self, mock_remove_currency):
        mock_remove_currency.return_value = None
        
        service = WalletService()
        await service.subtract_currency_from_wallet("USD")

        mock_remove_currency.assert_called_once_with("USD")

    @patch("src.services.wallet_service.subtract_currency_from_wallet")
    async def test_remove_currency_raises_value_error(self, mock_remove_currency):
        mock_remove_currency.side_effect = ValueError("Currency not found")
        
        service = WalletService()

        with pytest.raises(ValueError, match="Currency not found"):
            await service.subtract_currency_from_wallet("USD")
    
    @patch("src.services.wallet_service.remove_currency")
    async def test_remove_currency_success(self, mock_remove_currency):
        mock_remove_currency.return_value = None
        
        wallet_service = WalletService()
        await wallet_service.remove_currency_from_wallet("USD")
        
        mock_remove_currency.assert_called_once_with("USD")

    @patch("src.services.wallet_service.remove_currency")
    async def test_remove_currency_raises_value_error(self, mock_remove_currency):
        mock_remove_currency.side_effect = ValueError("Currency not found")
        
        wallet_service = WalletService()
        
        with pytest.raises(ValueError, match="Currency not found"):
            await wallet_service.remove_currency_from_wallet("INVALID")