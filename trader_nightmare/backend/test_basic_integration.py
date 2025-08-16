"""
Basic integration tests for the Enhanced Trading System
"""

import unittest
import asyncio
import time
from unittest.mock import Mock, patch
from datetime import datetime
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from enhanced_trading_system import (
    EnhancedTradingSystem, EnhancedScoutModule, RealTimeExecutorModule, 
    MockDataProvider, TokenData, TradeSignal
)

class TestBasicIntegration(unittest.TestCase):
    """Basic integration tests for the trading system"""
    
    def setUp(self):
        """Set up test environment"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Create mock data providers
        self.providers = [
            MockDataProvider("Provider1"),
            MockDataProvider("Provider2")
        ]
        
        # Initialize components
        self.scout = EnhancedScoutModule(self.providers)
        self.executor = RealTimeExecutorModule(self.providers)
        self.trading_system = EnhancedTradingSystem()
        
        # Test tokens
        self.test_tokens = [
            "0x1234567890123456789012345678901234567890",
            "0x2345678901234567890123456789012345678901"
        ]
    
    def tearDown(self):
        """Clean up test environment"""
        self.loop.close()
    
    def async_test(self, coro):
        """Helper method to run async tests"""
        return self.loop.run_until_complete(coro)
    
    def test_data_provider_connection(self):
        """Test data provider connection and disconnection"""
        async def run_test():
            provider = self.providers[0]
            
            # Initially disconnected
            self.assertFalse(provider.is_connected)
            
            # Connect
            result = await provider.connect()
            self.assertTrue(result)
            self.assertTrue(provider.is_connected)
            
            # Disconnect
            await provider.disconnect()
            self.assertFalse(provider.is_connected)
        
        self.async_test(run_test())
    
    def test_token_data_retrieval(self):
        """Test token data retrieval from providers"""
        async def run_test():
            provider = self.providers[0]
            await provider.connect()
            
            token_address = self.test_tokens[0]
            token_data = await provider.get_token_data(token_address)
            
            self.assertIsInstance(token_data, TokenData)
            self.assertEqual(token_data.address, token_address)
            self.assertGreater(token_data.price_usd, 0)
            self.assertGreater(token_data.volume_24h, 0)
            
            await provider.disconnect()
        
        self.async_test(run_test())
    
    def test_scout_module_assessment(self):
        """Test scout module token assessment"""
        async def run_test():
            # Connect providers
            for provider in self.providers:
                await provider.connect()
            
            token_address = self.test_tokens[0]
            
            # Get comprehensive assessment
            score, token_data, trade_signal = await self.scout.assess_token_comprehensive(token_address)
            
            # Verify results
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)
            
            self.assertIsInstance(token_data, TokenData)
            self.assertEqual(token_data.address, token_address)
            
            self.assertIsInstance(trade_signal, TradeSignal)
            self.assertEqual(trade_signal.token_address, token_address)
            self.assertIn(trade_signal.signal_type, ["BUY", "SELL", "HOLD"])
            
            # Disconnect providers
            for provider in self.providers:
                await provider.disconnect()
        
        self.async_test(run_test())
    
    def test_viability_score_calculation(self):
        """Test ML viability score calculation"""
        async def run_test():
            # Connect providers
            await self.providers[0].connect()
            
            token_address = self.test_tokens[0]
            token_data = await self.providers[0].get_token_data(token_address)
            
            # Calculate viability score
            score = self.scout.calculate_ml_viability_score(token_data)
            
            self.assertIsInstance(score, float)
            self.assertGreaterEqual(score, 0)
            self.assertLessEqual(score, 100)
            
            await self.providers[0].disconnect()
        
        self.async_test(run_test())
    
    def test_data_aggregation(self):
        """Test data aggregation from multiple providers"""
        async def run_test():
            # Connect all providers
            for provider in self.providers:
                await provider.connect()
            
            token_address = self.test_tokens[0]
            
            # Get aggregated data
            aggregated_data = await self.scout.get_aggregated_token_data(token_address)
            
            self.assertIsInstance(aggregated_data, TokenData)
            self.assertEqual(aggregated_data.address, token_address)
            self.assertGreater(aggregated_data.price_usd, 0)
            
            # Disconnect providers
            for provider in self.providers:
                await provider.disconnect()
        
        self.async_test(run_test())
    
    def test_caching_mechanism(self):
        """Test token data caching"""
        async def run_test():
            # Connect providers
            await self.providers[0].connect()
            
            token_address = self.test_tokens[0]
            
            # First call - should fetch from provider
            start_time = time.time()
            data1 = await self.scout.get_aggregated_token_data(token_address)
            first_call_time = time.time() - start_time
            
            # Second call - should use cache (should be faster)
            start_time = time.time()
            data2 = await self.scout.get_aggregated_token_data(token_address)
            second_call_time = time.time() - start_time
            
            # Verify data consistency
            self.assertIsNotNone(data1)
            self.assertIsNotNone(data2)
            self.assertEqual(data1.address, data2.address)
            
            # Second call should be faster (cached)
            self.assertLess(second_call_time, first_call_time)
            
            await self.providers[0].disconnect()
        
        self.async_test(run_test())
    
    def test_executor_module_basic(self):
        """Test basic executor module functionality"""
        # Test initialization
        self.assertIsNotNone(self.executor)
        
        # Test that executor has required methods
        self.assertTrue(hasattr(self.executor, 'start'))
        self.assertTrue(hasattr(self.executor, 'stop'))
    
    def test_trading_system_initialization(self):
        """Test trading system initialization"""
        self.assertIsNotNone(self.trading_system)
        
        # Test that system has required methods
        self.assertTrue(hasattr(self.trading_system, 'start'))
        self.assertTrue(hasattr(self.trading_system, 'stop'))
    
    def test_signal_generation_logic(self):
        """Test trade signal generation logic"""
        # Create test token data with high viability characteristics
        high_viability_token = TokenData(
            address="0x1234567890123456789012345678901234567890",
            symbol="HIGH",
            name="High Viability Token",
            price_usd=1.0,
            volume_24h=2000000,  # High volume
            liquidity=8000000,   # High liquidity
            market_cap=50000000, # Good market cap
            holder_count=20000,  # Many holders
            price_change_24h=8.0, # Positive price change
            volatility=0.2,      # Low volatility
            timestamp=datetime.now()
        )
        
        # Calculate score
        high_score = self.scout.calculate_ml_viability_score(high_viability_token)
        
        # Generate signal
        high_signal = self.scout._generate_trade_signal(high_viability_token, high_score)
        
        # High viability should generate BUY or HOLD signal
        self.assertIn(high_signal.signal_type, ["BUY", "HOLD"])
        self.assertGreater(high_signal.confidence, 0.0)
        self.assertLessEqual(high_signal.confidence, 1.0)
        
        # Create test token data with low viability characteristics
        low_viability_token = TokenData(
            address="0x9876543210987654321098765432109876543210",
            symbol="LOW",
            name="Low Viability Token",
            price_usd=0.1,
            volume_24h=50000,    # Low volume
            liquidity=100000,    # Low liquidity
            market_cap=500000,   # Small market cap
            holder_count=500,    # Few holders
            price_change_24h=-18.0, # Negative price change
            volatility=0.8,      # High volatility
            timestamp=datetime.now()
        )
        
        # Calculate score
        low_score = self.scout.calculate_ml_viability_score(low_viability_token)
        
        # Generate signal
        low_signal = self.scout._generate_trade_signal(low_viability_token, low_score)
        
        # Low viability should generate SELL or HOLD signal
        self.assertIn(low_signal.signal_type, ["SELL", "HOLD"])
        
        # High viability should have higher score than low viability
        self.assertGreater(high_score, low_score)
    
    def test_error_handling(self):
        """Test basic error handling"""
        async def run_test():
            # Test with disconnected provider
            token_address = self.test_tokens[0]
            
            # Should handle gracefully when provider is disconnected
            data = await self.providers[0].get_token_data(token_address)
            self.assertIsNone(data)
            
            # Should handle gracefully when no providers are connected
            aggregated_data = await self.scout.get_aggregated_token_data(token_address)
            self.assertIsNone(aggregated_data)
        
        self.async_test(run_test())
    
    def test_multiple_token_assessment(self):
        """Test assessment of multiple tokens"""
        async def run_test():
            # Connect providers
            for provider in self.providers:
                await provider.connect()
            
            results = []
            
            # Assess multiple tokens
            for token_address in self.test_tokens:
                score, token_data, signal = await self.scout.assess_token_comprehensive(token_address)
                results.append((score, token_data, signal))
            
            # Verify all assessments completed
            self.assertEqual(len(results), len(self.test_tokens))
            
            for score, token_data, signal in results:
                self.assertIsInstance(score, float)
                self.assertIsInstance(token_data, TokenData)
                self.assertIsInstance(signal, TradeSignal)
            
            # Disconnect providers
            for provider in self.providers:
                await provider.disconnect()
        
        self.async_test(run_test())

class TestPerformanceBasics(unittest.TestCase):
    """Basic performance tests"""
    
    def setUp(self):
        """Set up test environment"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.providers = [MockDataProvider("TestProvider")]
        self.scout = EnhancedScoutModule(self.providers)
    
    def tearDown(self):
        """Clean up test environment"""
        self.loop.close()
    
    def async_test(self, coro):
        """Helper method to run async tests"""
        return self.loop.run_until_complete(coro)
    
    def test_assessment_performance(self):
        """Test assessment performance"""
        async def run_test():
            await self.providers[0].connect()
            
            token_address = "0x1234567890123456789012345678901234567890"
            
            # Measure assessment time
            start_time = time.time()
            score, token_data, signal = await self.scout.assess_token_comprehensive(token_address)
            assessment_time = time.time() - start_time
            
            # Assessment should complete within reasonable time (< 1 second)
            self.assertLess(assessment_time, 1.0)
            
            # Results should be valid
            self.assertIsNotNone(score)
            self.assertIsNotNone(token_data)
            self.assertIsNotNone(signal)
            
            await self.providers[0].disconnect()
        
        self.async_test(run_test())
    
    def test_concurrent_assessments(self):
        """Test concurrent token assessments"""
        async def run_test():
            await self.providers[0].connect()
            
            tokens = [
                "0x1234567890123456789012345678901234567890",
                "0x2345678901234567890123456789012345678901",
                "0x3456789012345678901234567890123456789012"
            ]
            
            # Run concurrent assessments
            start_time = time.time()
            tasks = [self.scout.assess_token_comprehensive(token) for token in tokens]
            results = await asyncio.gather(*tasks)
            total_time = time.time() - start_time
            
            # All assessments should complete
            self.assertEqual(len(results), len(tokens))
            
            # Concurrent execution should be faster than sequential
            # (This is a basic check - in real scenarios, the difference would be more significant)
            self.assertLess(total_time, len(tokens) * 1.0)  # Less than 1 second per token
            
            await self.providers[0].disconnect()
        
        self.async_test(run_test())

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestBasicIntegration))
    test_suite.addTest(unittest.makeSuite(TestPerformanceBasics))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Basic Integration Tests Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    if result.testsRun > 0:
        success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100)
        print(f"Success rate: {success_rate:.1f}%")
    print(f"{'='*60}")
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)

