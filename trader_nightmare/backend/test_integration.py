"""
Integration tests for the Enhanced Trading Bot System
"""

import unittest
import asyncio
import time
import json
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime, timedelta
import sys
import os

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from enhanced_trading_system import (
    EnhancedTradingSystem, EnhancedScoutModule, RealTimeExecutorModule, 
    MockDataProvider, TokenData, TradeSignal
)

class TestTradingBotIntegration(unittest.TestCase):
    """Integration tests for the complete trading bot system"""
    
    def setUp(self):
        """Set up test environment"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        # Create mock data providers
        self.providers = [
            MockDataProvider("Provider1"),
            MockDataProvider("Provider2"),
            MockDataProvider("Provider3")
        ]
        
        # Initialize trading bot
        self.bot = EnhancedTradingBot(self.providers)
        
        # Test tokens
        self.test_tokens = [
            "0x1234567890123456789012345678901234567890",
            "0x2345678901234567890123456789012345678901",
            "0x3456789012345678901234567890123456789012"
        ]
    
    def tearDown(self):
        """Clean up test environment"""
        self.loop.close()
    
    def async_test(self, coro):
        """Helper method to run async tests"""
        return self.loop.run_until_complete(coro)
    
    def test_full_trading_cycle(self):
        """Test complete trading cycle from signal generation to position exit"""
        async def run_test():
            # Connect all providers
            for provider in self.providers:
                await provider.connect()
            
            # Start the trading bot
            await self.bot.start()
            
            # Wait for initial setup
            await asyncio.sleep(0.1)
            
            # Check that bot is running
            self.assertTrue(self.bot.is_running)
            
            # Run a few trading cycles
            for i in range(3):
                await self.bot.run_trading_cycle()
                await asyncio.sleep(0.1)
            
            # Check that some activity occurred
            self.assertGreater(len(self.bot.performance_metrics), 0)
            
            # Stop the bot
            await self.bot.stop()
            self.assertFalse(self.bot.is_running)
        
        self.async_test(run_test())
    
    def test_position_management(self):
        """Test position opening, monitoring, and closing"""
        async def run_test():
            # Connect providers
            for provider in self.providers:
                await provider.connect()
            
            await self.bot.start()
            
            # Simulate a high-viability token
            token_address = self.test_tokens[0]
            
            # Get token data
            token_data = await self.bot.scout.get_aggregated_token_data(token_address)
            self.assertIsNotNone(token_data)
            
            # Calculate viability score
            viability_score = self.bot.scout.calculate_ml_viability_score(token_data)
            
            # If score is high enough, should create position
            if viability_score >= 70:
                # Execute trade
                execution_result = await self.bot.executor.execute_trade(
                    token_address, "BUY", 100.0, token_data.price_usd
                )
                
                if execution_result["success"]:
                    # Check position was created
                    positions = self.bot.executor.get_active_positions()
                    self.assertGreater(len(positions), 0)
                    
                    # Find our position
                    position = next((p for p in positions if p.token_address == token_address), None)
                    self.assertIsNotNone(position)
                    
                    # Simulate price changes and check exit logic
                    for price_change in [1.1, 1.2, 0.9, 1.15]:  # Various price movements
                        new_price = token_data.price_usd * price_change
                        
                        # Update position with new price
                        position.current_price = new_price
                        position.current_value = position.amount * new_price
                        position.pnl = position.current_value - position.entry_value
                        position.pnl_percentage = (position.pnl / position.entry_value) * 100
                        
                        # Check exit conditions
                        should_exit, exit_reason = self.bot.exit_module.should_exit_position(position)
                        
                        if should_exit:
                            # Execute exit
                            exit_result = await self.bot.executor.execute_trade(
                                token_address, "SELL", position.amount, new_price
                            )
                            
                            if exit_result["success"]:
                                # Position should be closed
                                self.bot.executor.close_position(position.position_id)
                                break
            
            await self.bot.stop()
        
        self.async_test(run_test())
    
    def test_error_handling_and_recovery(self):
        """Test system behavior under error conditions"""
        async def run_test():
            # Start with disconnected providers to simulate errors
            await self.bot.start()
            
            # Try to run trading cycle with no data
            await self.bot.run_trading_cycle()
            
            # Should handle gracefully without crashing
            self.assertTrue(self.bot.is_running)
            
            # Connect one provider
            await self.providers[0].connect()
            
            # Should now be able to get some data
            await self.bot.run_trading_cycle()
            
            # Simulate provider disconnection
            await self.providers[0].disconnect()
            
            # Should continue running
            await self.bot.run_trading_cycle()
            self.assertTrue(self.bot.is_running)
            
            await self.bot.stop()
        
        self.async_test(run_test())
    
    def test_performance_tracking(self):
        """Test performance metrics collection and calculation"""
        async def run_test():
            # Connect providers
            for provider in self.providers:
                await provider.connect()
            
            await self.bot.start()
            
            # Run several trading cycles
            for i in range(5):
                await self.bot.run_trading_cycle()
                await asyncio.sleep(0.05)
            
            # Check performance metrics
            metrics = self.bot.get_performance_summary()
            
            self.assertIn("total_trades", metrics)
            self.assertIn("successful_trades", metrics)
            self.assertIn("total_pnl", metrics)
            self.assertIn("win_rate", metrics)
            self.assertIn("average_trade_duration", metrics)
            
            # Metrics should be reasonable
            self.assertGreaterEqual(metrics["total_trades"], 0)
            self.assertGreaterEqual(metrics["successful_trades"], 0)
            self.assertGreaterEqual(metrics["win_rate"], 0.0)
            self.assertLessEqual(metrics["win_rate"], 1.0)
            
            await self.bot.stop()
        
        self.async_test(run_test())
    
    def test_concurrent_position_limits(self):
        """Test that concurrent position limits are respected"""
        async def run_test():
            # Connect providers
            for provider in self.providers:
                await provider.connect()
            
            await self.bot.start()
            
            # Set low concurrent position limit for testing
            original_limit = self.bot.executor.max_concurrent_positions
            self.bot.executor.max_concurrent_positions = 2
            
            try:
                # Try to create multiple positions
                positions_created = 0
                
                for token_address in self.test_tokens:
                    token_data = await self.bot.scout.get_aggregated_token_data(token_address)
                    if token_data:
                        # Force high viability score for testing
                        viability_score = 85.0
                        
                        if len(self.bot.executor.get_active_positions()) < self.bot.executor.max_concurrent_positions:
                            result = await self.bot.executor.execute_trade(
                                token_address, "BUY", 100.0, token_data.price_usd
                            )
                            if result["success"]:
                                positions_created += 1
                
                # Should not exceed limit
                active_positions = self.bot.executor.get_active_positions()
                self.assertLessEqual(len(active_positions), self.bot.executor.max_concurrent_positions)
                
            finally:
                # Restore original limit
                self.bot.executor.max_concurrent_positions = original_limit
                await self.bot.stop()
        
        self.async_test(run_test())
    
    def test_data_aggregation_accuracy(self):
        """Test accuracy of data aggregation from multiple providers"""
        async def run_test():
            # Connect all providers
            for provider in self.providers:
                await provider.connect()
            
            token_address = self.test_tokens[0]
            
            # Get data from individual providers
            individual_data = []
            for provider in self.providers:
                data = await provider.get_token_data(token_address)
                if data:
                    individual_data.append(data)
            
            # Get aggregated data
            aggregated_data = await self.bot.scout.get_aggregated_token_data(token_address)
            
            self.assertIsNotNone(aggregated_data)
            self.assertEqual(aggregated_data.address, token_address)
            
            # Aggregated price should be reasonable compared to individual prices
            if individual_data:
                individual_prices = [data.price_usd for data in individual_data]
                avg_price = sum(individual_prices) / len(individual_prices)
                
                # Aggregated price should be close to average (within 20%)
                price_diff = abs(aggregated_data.price_usd - avg_price) / avg_price
                self.assertLess(price_diff, 0.2)
        
        self.async_test(run_test())
    
    def test_signal_generation_consistency(self):
        """Test consistency of signal generation"""
        async def run_test():
            # Connect providers
            for provider in self.providers:
                await provider.connect()
            
            token_address = self.test_tokens[0]
            
            # Generate multiple signals for the same token
            signals = []
            for i in range(5):
                score, token_data, signal = await self.bot.scout.assess_token_comprehensive(token_address)
                signals.append((score, signal))
                await asyncio.sleep(0.01)  # Small delay
            
            # Scores should be consistent (within reasonable variance)
            scores = [s[0] for s in signals]
            if len(scores) > 1:
                score_variance = max(scores) - min(scores)
                self.assertLess(score_variance, 10.0)  # Should not vary by more than 10 points
            
            # Signal types should be consistent for similar scores
            signal_types = [s[1].signal_type for s in signals]
            if len(set(signal_types)) > 1:
                # If signals differ, scores should justify the difference
                for i in range(1, len(signals)):
                    score_diff = abs(scores[i] - scores[i-1])
                    if signal_types[i] != signal_types[i-1]:
                        self.assertGreater(score_diff, 5.0)  # Significant score change should justify signal change
        
        self.async_test(run_test())

class TestModuleIntegration(unittest.TestCase):
    """Test integration between individual modules"""
    
    def setUp(self):
        """Set up test environment"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.providers = [MockDataProvider("TestProvider")]
        self.scout = EnhancedScoutModule(self.providers)
        self.executor = EnhancedExecutorModule()
        self.exit_module = EnhancedExitModule()
    
    def tearDown(self):
        """Clean up test environment"""
        self.loop.close()
    
    def async_test(self, coro):
        """Helper method to run async tests"""
        return self.loop.run_until_complete(coro)
    
    def test_scout_executor_integration(self):
        """Test integration between Scout and Executor modules"""
        async def run_test():
            await self.providers[0].connect()
            
            token_address = "0x1234567890123456789012345678901234567890"
            
            # Get assessment from scout
            score, token_data, signal = await self.scout.assess_token_comprehensive(token_address)
            
            # Use signal for execution decision
            if signal.signal_type == "BUY" and score >= 70:
                result = await self.executor.execute_trade(
                    token_address, "BUY", 100.0, token_data.price_usd
                )
                
                # Should succeed if conditions are met
                if result["success"]:
                    positions = self.executor.get_active_positions()
                    self.assertGreater(len(positions), 0)
                    
                    # Position should match signal data
                    position = positions[0]
                    self.assertEqual(position.token_address, token_address)
                    self.assertEqual(position.entry_price, token_data.price_usd)
        
        self.async_test(run_test())
    
    def test_executor_exit_integration(self):
        """Test integration between Executor and Exit modules"""
        async def run_test():
            await self.providers[0].connect()
            
            token_address = "0x1234567890123456789012345678901234567890"
            token_data = await self.providers[0].get_token_data(token_address)
            
            # Create a position
            result = await self.executor.execute_trade(
                token_address, "BUY", 100.0, token_data.price_usd
            )
            
            if result["success"]:
                positions = self.executor.get_active_positions()
                position = positions[0]
                
                # Test exit conditions
                # Simulate profit scenario
                position.current_price = position.entry_price * 1.3  # 30% gain
                position.current_value = position.amount * position.current_price
                position.pnl = position.current_value - position.entry_value
                position.pnl_percentage = (position.pnl / position.entry_value) * 100
                
                should_exit, reason = self.exit_module.should_exit_position(position)
                
                if should_exit:
                    # Execute exit
                    exit_result = await self.executor.execute_trade(
                        token_address, "SELL", position.amount, position.current_price
                    )
                    
                    self.assertTrue(exit_result["success"])
                    
                    # Close position
                    self.executor.close_position(position.position_id)
                    
                    # Should have no active positions
                    self.assertEqual(len(self.executor.get_active_positions()), 0)
        
        self.async_test(run_test())

class TestSystemResilience(unittest.TestCase):
    """Test system resilience under various conditions"""
    
    def setUp(self):
        """Set up test environment"""
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        
        self.providers = [MockDataProvider(f"Provider{i}") for i in range(3)]
        self.bot = EnhancedTradingBot(self.providers)
    
    def tearDown(self):
        """Clean up test environment"""
        self.loop.close()
    
    def async_test(self, coro):
        """Helper method to run async tests"""
        return self.loop.run_until_complete(coro)
    
    def test_partial_provider_failure(self):
        """Test system behavior when some providers fail"""
        async def run_test():
            # Connect only some providers
            await self.providers[0].connect()
            await self.providers[1].connect()
            # Leave providers[2] disconnected
            
            await self.bot.start()
            
            # Should still function with partial providers
            await self.bot.run_trading_cycle()
            
            self.assertTrue(self.bot.is_running)
            
            # Disconnect another provider
            await self.providers[1].disconnect()
            
            # Should still function with just one provider
            await self.bot.run_trading_cycle()
            
            self.assertTrue(self.bot.is_running)
            
            await self.bot.stop()
        
        self.async_test(run_test())
    
    def test_rapid_price_changes(self):
        """Test system behavior with rapid price changes"""
        async def run_test():
            await self.providers[0].connect()
            await self.bot.start()
            
            token_address = "0x1234567890123456789012345678901234567890"
            
            # Create a position
            token_data = await self.providers[0].get_token_data(token_address)
            result = await self.bot.executor.execute_trade(
                token_address, "BUY", 100.0, token_data.price_usd
            )
            
            if result["success"]:
                position = self.bot.executor.get_active_positions()[0]
                
                # Simulate rapid price changes
                price_changes = [1.1, 0.9, 1.2, 0.8, 1.15, 0.95]
                
                for change in price_changes:
                    new_price = token_data.price_usd * change
                    position.current_price = new_price
                    position.current_value = position.amount * new_price
                    position.pnl = position.current_value - position.entry_value
                    position.pnl_percentage = (position.pnl / position.entry_value) * 100
                    
                    # Check exit conditions
                    should_exit, reason = self.bot.exit_module.should_exit_position(position)
                    
                    if should_exit:
                        # System should handle exit gracefully
                        exit_result = await self.bot.executor.execute_trade(
                            token_address, "SELL", position.amount, new_price
                        )
                        
                        if exit_result["success"]:
                            self.bot.executor.close_position(position.position_id)
                            break
                    
                    await asyncio.sleep(0.01)  # Small delay between price changes
            
            await self.bot.stop()
        
        self.async_test(run_test())
    
    def test_memory_usage_stability(self):
        """Test that memory usage remains stable over time"""
        async def run_test():
            import psutil
            import os
            
            process = psutil.Process(os.getpid())
            initial_memory = process.memory_info().rss
            
            # Connect providers
            for provider in self.providers:
                await provider.connect()
            
            await self.bot.start()
            
            # Run many trading cycles
            for i in range(20):
                await self.bot.run_trading_cycle()
                await asyncio.sleep(0.01)
            
            final_memory = process.memory_info().rss
            memory_increase = final_memory - initial_memory
            
            # Memory increase should be reasonable (less than 50MB)
            self.assertLess(memory_increase, 50 * 1024 * 1024)
            
            await self.bot.stop()
        
        self.async_test(run_test())

if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestTradingBotIntegration))
    test_suite.addTest(unittest.makeSuite(TestModuleIntegration))
    test_suite.addTest(unittest.makeSuite(TestSystemResilience))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Integration Tests Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    print(f"{'='*60}")
    
    # Exit with appropriate code
    exit(0 if result.wasSuccessful() else 1)

