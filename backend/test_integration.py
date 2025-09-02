"""Integration tests for the enhanced trading system."""

import asyncio
import os
import sys
import unittest

# Allow importing the src package
sys.path.append(os.path.dirname(__file__))

from src.enhanced_trading_system import EnhancedTradingSystem


class TestTradingSystemIntegration(unittest.TestCase):
    """Minimal integration tests for :class:`EnhancedTradingSystem`."""

    def setUp(self) -> None:  # noqa: D401 - short description
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.system = EnhancedTradingSystem()

    def tearDown(self) -> None:  # noqa: D401 - short description
        self.loop.close()

    def async_test(self, coro):
        """Helper to run asynchronous tests."""
        return self.loop.run_until_complete(coro)

    def test_start_and_stop(self):
        """System can start and stop without errors."""

        async def run():
            await self.system.start_system()
            self.assertTrue(self.system.is_running)
            await self.system.stop_system()
            self.assertFalse(self.system.is_running)

        self.async_test(run())

    def test_run_cycle(self):
        """Running a single trading cycle executes without raising."""

        async def run():
            await self.system.start_system()
            token = "0x1234567890123456789012345678901234567890"
            await self.system.run_enhanced_cycle(token)
            await self.system.stop_system()

        self.async_test(run())


if __name__ == "__main__":  # pragma: no cover - convenience
    unittest.main()

