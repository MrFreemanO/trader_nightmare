"""
Unit tests for the Enhanced Scout Module
"""

import unittest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.utils.error_handling import CircuitBreaker, handle_api_errors
from enhanced_trading_system import EnhancedScoutModule, TokenData, TradeSignal, MockDataProvider

class TestMockDataProvider(unittest.TestCase):
    """Test cases for MockDataProvider"""
    
    def setUp(self):
        self.provider = MockDataProvider("TestProvider")
    
    def test_initial_state(self):
        """Test initial provider state"""
        self.assertFalse(self.provider.is_connected)
        self.assertIsNone(self.provider.last_update)
        self.assertEqual(self.provider.name, "TestProvider")
    
    async def test_connect(self):
        """Test provider connection"""
        result = await self.provider.connect()
        self.assertTrue(result)
        self.assertTrue(self.provider.is_connected)
        self.assertIsNotNone(self.provider.last_update)
    
    async def test_disconnect(self):
        """Test provider disconnection"""
        await self.provider.connect()
        await self.provider.disconnect()
        self.assertFalse(self.provider.is_connected)
    
    async def test_get_token_data(self):
        """Test token data retrieval"""
        await self.provider.connect()
        token_address = "0x1234567890123456789012345678901234567890"
        
        data = await self.provider.get_token_data(token_address)
        
        self.assertIsInstance(data, TokenData)
        self.assertEqual(data.address, token_address)
        self.assertGreater(data.price_usd, 0)
        self.assertGreater(data.volume_24h, 0)
        self.assertGreater(data.liquidity, 0)
    
    async def test_get_token_data_disconnected(self):
        """Test token data retrieval when disconnected"""
        token_address = "0x1234567890123456789012345678901234567890"
        data = await self.provider.get_token_data(token_address)
        self.assertIsNone(data)
    
    async def test_get_real_time_price(self):
        """Test real-time price retrieval"""
        await self.provider.connect()
        token_address = "0x1234567890123456789012345678901234567890"
        
        price = await self.provider.get_real_time_price(token_address)
        
        self.assertIsInstance(price, float)
        self.assertGreater(price, 0)

class TestEnhancedScoutModule(unittest.TestCase):
    """Test cases for EnhancedScoutModule"""
    
    def setUp(self):
        self.providers = [
            MockDataProvider("Provider1"),
            MockDataProvider("Provider2"),
            MockDataProvider("Provider3")
        ]
        self.scout = EnhancedScoutModule(self.providers)
    
    async def test_ml_viability_score_calculation(self):
        """Test ML viability score calculation"""
        token_data = TokenData(
            address="0x1234567890123456789012345678901234567890",
            symbol="TEST",
            name="Test Token",
            price_usd=1.0,
            volume_24h=1000000,
            liquidity=5000000,
            market_cap=10000000,
            holder_count=10000,
            price_change_24h=5.0,
            volatility=0.3,
            timestamp=datetime.now()
        )
        
        score = self.scout.calculate_ml_viability_score(token_data)
        
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
    
    async def test_ml_viability_score_edge_cases(self):
        """Test ML viability score with edge case values"""
        # Test with very low values
        low_token_data = TokenData(
            address="0x1234567890123456789012345678901234567890",
            symbol="LOW",
            name="Low Token",
            price_usd=0.001,
            volume_24h=1000,
            liquidity=10000,
            market_cap=50000,
            holder_count=100,
            price_change_24h=-15.0,
            volatility=0.9,
            timestamp=datetime.now()
        )
        
        low_score = self.scout.calculate_ml_viability_score(low_token_data)
        
        # Test with very high values
        high_token_data = TokenData(
            address="0x1234567890123456789012345678901234567890",
            symbol="HIGH",
            name="High Token",
            price_usd=1000.0,
            volume_24h=50000000,
            liquidity=100000000,
            market_cap=1000000000,
            holder_count=100000,
            price_change_24h=15.0,
            volatility=0.1,
            timestamp=datetime.now()
        )
        
        high_score = self.scout.calculate_ml_viability_score(high_token_data)
        
        self.assertGreater(high_score, low_score)
        self.assertGreaterEqual(low_score, 0)
        self.assertLessEqual(high_score, 100)
    
    async def test_get_aggregated_token_data(self):
        """Test token data aggregation from multiple providers"""
        # Connect all providers
        for provider in self.providers:
            await provider.connect()
        
        token_address = "0x1234567890123456789012345678901234567890"
        
        aggregated_data = await self.scout.get_aggregated_token_data(token_address)
        
        self.assertIsInstance(aggregated_data, TokenData)
        self.assertEqual(aggregated_data.address, token_address)
        self.assertGreater(aggregated_data.price_usd, 0)
    
    async def test_get_aggregated_token_data_no_providers(self):
        """Test token data aggregation with no connected providers"""
        token_address = "0x1234567890123456789012345678901234567890"
        
        aggregated_data = await self.scout.get_aggregated_token_data(token_address)
        
        self.assertIsNone(aggregated_data)
    
    async def test_caching_mechanism(self):
        """Test token data caching"""
        # Connect providers
        for provider in self.providers:
            await provider.connect()
        
        token_address = "0x1234567890123456789012345678901234567890"
        
        # First call - should fetch from providers
        data1 = await self.scout.get_aggregated_token_data(token_address)
        
        # Second call - should use cache
        data2 = await self.scout.get_aggregated_token_data(token_address)
        
        self.assertIsNotNone(data1)
        self.assertIsNotNone(data2)
        self.assertEqual(data1.address, data2.address)
        
        # Check cache was used
        cache_key = f"token_{token_address}"
        self.assertIn(cache_key, self.scout.token_cache)
    
    async def test_assess_token_comprehensive(self):
        """Test comprehensive token assessment"""
        # Connect providers
        for provider in self.providers:
            await provider.connect()
        
        token_address = "0x1234567890123456789012345678901234567890"
        
        score, token_data, trade_signal = await self.scout.assess_token_comprehensive(token_address)
        
        self.assertIsInstance(score, float)
        self.assertIsInstance(token_data, TokenData)
        self.assertIsInstance(trade_signal, TradeSignal)
        
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        self.assertEqual(token_data.address, token_address)
        self.assertEqual(trade_signal.token_address, token_address)
    
    async def test_trade_signal_generation(self):
        """Test trade signal generation logic"""
        # High viability token
        high_viability_token = TokenData(
            address="0x1234567890123456789012345678901234567890",
            symbol="HIGH",
            name="High Token",
            price_usd=1.0,
            volume_24h=2000000,
            liquidity=8000000,
            market_cap=50000000,
            holder_count=20000,
            price_change_24h=8.0,
            volatility=0.2,
            timestamp=datetime.now()
        )
        
        high_score = self.scout.calculate_ml_viability_score(high_viability_token)
        high_signal = self.scout._generate_trade_signal(high_viability_token, high_score)
        
        # Low viability token
        low_viability_token = TokenData(
            address="0x9876543210987654321098765432109876543210",
            symbol="LOW",
            name="Low Token",
            price_usd=0.1,
            volume_24h=50000,
            liquidity=100000,
            market_cap=500000,
            holder_count=500,
            price_change_24h=-18.0,
            volatility=0.8,
            timestamp=datetime.now()
        )
        
        low_score = self.scout.calculate_ml_viability_score(low_viability_token)
        low_signal = self.scout._generate_trade_signal(low_viability_token, low_score)
        
        # Verify signal types make sense
        if high_score >= 70:
            self.assertIn(high_signal.signal_type, ["BUY", "HOLD"])
        
        if low_score < 40:
            self.assertIn(low_signal.signal_type, ["SELL", "HOLD"])
        
        # Verify confidence levels
        self.assertGreaterEqual(high_signal.confidence, 0.0)
        self.assertLessEqual(high_signal.confidence, 1.0)
        self.assertGreaterEqual(low_signal.confidence, 0.0)
        self.assertLessEqual(low_signal.confidence, 1.0)

class TestCircuitBreaker(unittest.TestCase):
    """Test cases for Circuit Breaker functionality"""
    
    def setUp(self):
        self.circuit_breaker = CircuitBreaker(failure_threshold=3, timeout=1, name="test")
    
    def test_initial_state(self):
        """Test initial circuit breaker state"""
        from src.utils.error_handling import CircuitState
        self.assertEqual(self.circuit_breaker.state, CircuitState.CLOSED)
        self.assertEqual(self.circuit_breaker.failure_count, 0)
    
    def test_successful_calls(self):
        """Test successful function calls"""
        def successful_function():
            return "success"
        
        result = self.circuit_breaker.call(successful_function)
        self.assertEqual(result, "success")
        self.assertEqual(self.circuit_breaker.failure_count, 0)
    
    def test_circuit_opening(self):
        """Test circuit breaker opening after failures"""
        from src.utils.error_handling import CircuitState
        
        def failing_function():
            raise Exception("Test failure")
        
        # Cause failures to open circuit
        for i in range(3):
            with self.assertRaises(Exception):
                self.circuit_breaker.call(failing_function)
        
        self.assertEqual(self.circuit_breaker.state, CircuitState.OPEN)
    
    def test_circuit_half_open_transition(self):
        """Test circuit breaker half-open transition"""
        import time
        from src.utils.error_handling import CircuitState, CircuitBreakerOpenError
        
        def failing_function():
            raise Exception("Test failure")
        
        def successful_function():
            return "success"
        
        # Open the circuit
        for i in range(3):
            with self.assertRaises(Exception):
                self.circuit_breaker.call(failing_function)
        
        # Should be open
        self.assertEqual(self.circuit_breaker.state, CircuitState.OPEN)
        
        # Should raise CircuitBreakerOpenError
        with self.assertRaises(CircuitBreakerOpenError):
            self.circuit_breaker.call(successful_function)
        
        # Wait for timeout
        time.sleep(1.1)
        
        # Should transition to half-open and allow call
        result = self.circuit_breaker.call(successful_function)
        self.assertEqual(result, "success")

class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling decorators"""
    
    def test_handle_api_errors_success(self):
        """Test handle_api_errors decorator with successful function"""
        @handle_api_errors
        def successful_function():
            return {"data": "test"}
        
        result = successful_function()
        self.assertTrue(result["success"])
        self.assertEqual(result["data"]["data"], "test")
    
    def test_handle_api_errors_connection_error(self):
        """Test handle_api_errors decorator with connection error"""
        @handle_api_errors
        def failing_function():
            raise ConnectionError("Connection failed")
        
        result = failing_function()
        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "connection")
        self.assertTrue(result["retry"])
    
    def test_handle_api_errors_timeout_error(self):
        """Test handle_api_errors decorator with timeout error"""
        @handle_api_errors
        def failing_function():
            raise TimeoutError("Request timeout")
        
        result = failing_function()
        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "timeout")
        self.assertTrue(result["retry"])
    
    def test_handle_api_errors_value_error(self):
        """Test handle_api_errors decorator with validation error"""
        @handle_api_errors
        def failing_function():
            raise ValueError("Invalid data")
        
        result = failing_function()
        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "validation")
        self.assertFalse(result["retry"])

# Async test runner
class AsyncTestCase(unittest.TestCase):
    """Base class for async test cases"""
    
    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
    
    def tearDown(self):
        self.loop.close()
    
    def async_test(self, coro):
        """Helper method to run async tests"""
        return self.loop.run_until_complete(coro)

class TestAsyncScoutModule(AsyncTestCase):
    """Async test cases for Scout Module"""
    
    def setUp(self):
        super().setUp()
        self.providers = [MockDataProvider("TestProvider")]
        self.scout = EnhancedScoutModule(self.providers)
    
    def test_async_token_assessment(self):
        """Test async token assessment"""
        async def run_test():
            await self.providers[0].connect()
            token_address = "0x1234567890123456789012345678901234567890"
            
            score, token_data, trade_signal = await self.scout.assess_token_comprehensive(token_address)
            
            self.assertIsInstance(score, float)
            self.assertIsInstance(token_data, TokenData)
            self.assertIsInstance(trade_signal, TradeSignal)
        
        self.async_test(run_test())
    
    def test_async_data_aggregation(self):
        """Test async data aggregation"""
        async def run_test():
            await self.providers[0].connect()
            token_address = "0x1234567890123456789012345678901234567890"
            
            data = await self.scout.get_aggregated_token_data(token_address)
            
            self.assertIsInstance(data, TokenData)
            self.assertEqual(data.address, token_address)
        
        self.async_test(run_test())

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestMockDataProvider))
    test_suite.addTest(unittest.makeSuite(TestEnhancedScoutModule))
    test_suite.addTest(unittest.makeSuite(TestCircuitBreaker))
    test_suite.addTest(unittest.makeSuite(TestErrorHandling))
    test_suite.addTest(unittest.makeSuite(TestAsyncScoutModule))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)

