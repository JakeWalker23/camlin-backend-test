from fastapi.testclient import TestClient
from fastapi import HTTPException
from unittest.mock import AsyncMock, patch
from src.services.auth_service import verify_jwt
from src.controllers.wallet_controller import read_wallet
from main import app

client = TestClient(app)

class TestWalletController:
    async def mock_jwt(self):
        return {"sub": "test-user-id"}

    def fake_verify_jwt_fail(self):
        raise HTTPException(status_code=401, detail="Invalid token")

    async def mock_wallet(self):
        return {'holdings': {'PLN': 0.0}, 'pln_holdings': {'PLN': 0.0}, 'total_pln': 0.0}
    
    async def mock_add_currency_to_wallet(self, currency, amount):
        return None

    async def mock_add_currency_fail(self, currency, amount):
        raise ValueError("Invalid currency")

    def setup_method(self):
        app.dependency_overrides = {}

    def teardown_method(self):
        app.dependency_overrides = {}

    def test_read_wallet_returns_HTTP_200_response(self):
        app.dependency_overrides[verify_jwt] = self.mock_jwt
        app.dependency_overrides[read_wallet] = self.mock_wallet

        response = client.get("/wallet")

        assert response.status_code == 200
        assert response.json() == {'holdings': {'PLN': 0.0}, 'pln_holdings': {'PLN': 0.0}, 'total_pln': 0.0}

    def test_read_wallet_returns_HTTP_401_response_when_unauthorised(self):
        app.dependency_overrides[verify_jwt] = self.fake_verify_jwt_fail

        response = client.get("/wallet")

        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid token"}
    

    @patch("src.controllers.wallet_controller.wallet_service.add_currency_to_wallet", new_callable=AsyncMock)
    def test_add_to_wallet_success(self, mock_add):
        mock_add.return_value = None
        app.dependency_overrides[verify_jwt] = self.mock_jwt

        response = client.post("/wallet/add/USD/10.5")

        assert response.status_code == 200
        assert response.json() == {"message": "Added 10.5 USD to wallet"}
        mock_add.assert_awaited_once_with("USD", 10.5)

    @patch("src.controllers.wallet_controller.wallet_service.add_currency_to_wallet", new_callable=AsyncMock)
    def test_add_to_wallet_validation_error(self, mock_add_currency_fail):
        mock_add_currency_fail.side_effect = ValueError("Invalid currency")
        app.dependency_overrides[verify_jwt] = self.mock_jwt

        response = client.post("/wallet/add/INVALID/10.5")

        assert response.status_code == 400
        assert "Invalid currency" in response.json()["detail"]
        mock_add_currency_fail.assert_not_awaited()
    
    @patch("src.controllers.wallet_controller.wallet_service.subtract_currency_from_wallet", new_callable=AsyncMock)
    def test_subtract_from_wallet_success(self, mock_subtract):
        mock_subtract.return_value = None
        app.dependency_overrides[verify_jwt] = self.mock_jwt

        response = client.post("/wallet/sub/USD/10.5")

        assert response.status_code == 200
        assert response.json() == {"message": "Subtracted 10.5 USD from wallet."}
        mock_subtract.assert_awaited_once_with("USD", 10.5)

    @patch("src.controllers.wallet_controller.wallet_service.subtract_currency_from_wallet", new_callable=AsyncMock)
    def test_subtract_from_wallet_validation_error(self, mock_subtract_fail):
        mock_subtract_fail.side_effect = ValueError("Invalid currency")
        app.dependency_overrides[verify_jwt] = self.mock_jwt

        response = client.post("/wallet/sub/INVALID/10.5")

        assert response.status_code == 400
        assert "Invalid currency" in response.json()["detail"]
        mock_subtract_fail.assert_not_awaited()

    @patch("src.controllers.wallet_controller.wallet_service.remove_currency_from_wallet", new_callable=AsyncMock)
    @patch("src.controllers.wallet_controller.currency_validator.validate_currency_code")
    def test_delete_currency_success(self, mock_validate_currency, mock_remove_currency):
        mock_validate_currency.return_value = "USD"
        mock_remove_currency.return_value = None
        app.dependency_overrides[verify_jwt] = self.mock_jwt

        response = client.delete("/wallet/USD")

        assert response.status_code == 200
        assert response.json() == {"message": "USD removed from wallet."}
        mock_validate_currency.assert_called_once_with("USD")
        mock_remove_currency.assert_awaited_once_with("USD")

    @patch("src.controllers.wallet_controller.currency_validator.validate_currency_code")
    def test_delete_currency_invalid_currency(self, mock_validate_currency):
        mock_validate_currency.side_effect = ValueError("Invalid currency code")
        app.dependency_overrides[verify_jwt] = self.mock_jwt

        response = client.delete("/wallet/INVALID")

        assert response.status_code == 400
        assert response.json() == {"detail": "Invalid currency code"}
        mock_validate_currency.assert_called_once_with("INVALID")