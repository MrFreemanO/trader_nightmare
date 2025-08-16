import asyncio
import websockets
import json
import requests
import time
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import threading
from queue import Queue

logger = logging.getLogger(__name__)

@dataclass
class TokenData:
    """Data structure for token information"""
    address: str
    symbol: str
    name: str
    price_usd: float
    volume_24h: float
    liquidity: float
    market_cap: float
    holder_count: int
    timestamp: datetime

@dataclass
class TradeData:
    """Data structure for trade information"""
    token_address: str
    price: float
    volume: float
    side: str  # 'buy' or 'sell'
    timestamp: datetime
    exchange: str
    transaction_hash: str

class DataProvider:
    """Base class for data providers"""
    
    def __init__(self, name: str):
        self.name = name
        self.is_connected = False
        self.last_update = None
    
    async def connect(self):
        """Connect to data source"""
        raise NotImplementedError
    
    async def disconnect(self):
        """Disconnect from data source"""
        raise NotImplementedError
    
    async def get_token_data(self, token_address: str) -> Optional[TokenData]:
        """Get token data"""
        raise NotImplementedError
    
    async def subscribe_to_trades(self, token_address: str, callback):
        """Subscribe to real-time trade data"""
        raise NotImplementedError

class BitqueryProvider(DataProvider):
    """Bitquery API provider for blockchain data"""
    
    def __init__(self, api_key: str):
        super().__init__("Bitquery")
        self.api_key = api_key
        self.base_url = "https://graphql.bitquery.io"
        self.headers = {
            "X-API-KEY": api_key,
            "Content-Type": "application/json"
        }
    
    async def connect(self):
        """Test connection to Bitquery API"""
        try:
            # Test query to verify connection
            query = """
            {
              ethereum {
                blocks(limit: 1) {
                  height
                }
              }
            }
            """
            response = requests.post(
                self.base_url,
                json={"query": query},
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                self.is_connected = True
                logger.info(f"Connected to {self.name}")
                return True
            else:
                logger.error(f"Failed to connect to {self.name}: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Connection error to {self.name}: {e}")
            return False
    
    async def get_token_data(self, token_address: str) -> Optional[TokenData]:
        """Get comprehensive token data from Bitquery"""
        if not self.is_connected:
            await self.connect()
        
        query = f"""
        {{
          ethereum(network: bsc) {{
            dexTrades(
              baseCurrency: {{is: "{token_address}"}}
              date: {{since: "2024-01-01"}}
              options: {{limit: 1, desc: "timeInterval.minute"}}
            ) {{
              baseCurrency {{
                symbol
                name
                address
              }}
              quoteCurrency {{
                symbol
              }}
              quotePrice
              baseAmount
              quoteAmount
              trades: count
              timeInterval {{
                minute(count: 1)
              }}
            }}
            transfers(
              currency: {{is: "{token_address}"}}
              date: {{since: "2024-01-01"}}
              options: {{limit: 1000}}
            ) {{
              sender {{
                address
              }}
              receiver {{
                address
              }}
              amount
            }}
          }}
        }}
        """
        
        try:
            response = requests.post(
                self.base_url,
                json={"query": query},
                headers=self.headers,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                
                if 'data' in data and 'ethereum' in data['data']:
                    trades = data['data']['ethereum']['dexTrades']
                    transfers = data['data']['ethereum']['transfers']
                    
                    if trades:
                        trade = trades[0]
                        
                        # Calculate holder count from unique addresses
                        unique_addresses = set()
                        for transfer in transfers:
                            unique_addresses.add(transfer['sender']['address'])
                            unique_addresses.add(transfer['receiver']['address'])
                        
                        # Calculate volume and liquidity estimates
                        volume_24h = sum(float(t.get('quoteAmount', 0)) for t in trades)
                        
                        return TokenData(
                            address=token_address,
                            symbol=trade['baseCurrency']['symbol'],
                            name=trade['baseCurrency']['name'],
                            price_usd=float(trade.get('quotePrice', 0)),
                            volume_24h=volume_24h,
                            liquidity=volume_24h * 2,  # Rough estimate
                            market_cap=0,  # Would need total supply
                            holder_count=len(unique_addresses),
                            timestamp=datetime.now()
                        )
            
            logger.warning(f"No data found for token {token_address}")
            return None
            
        except Exception as e:
            logger.error(f"Error fetching token data from {self.name}: {e}")
            return None

class ZeroXProvider(DataProvider):
    """0x API provider for DEX aggregation and pricing"""
    
    def __init__(self, api_key: Optional[str] = None):
        super().__init__("0x")
        self.api_key = api_key
        self.base_url = "https://api.0x.org"
        self.headers = {}
        if api_key:
            self.headers["0x-api-key"] = api_key
    
    async def connect(self):
        """Test connection to 0x API"""
        try:
            # Test with a simple price query
            response = requests.get(
                f"{self.base_url}/swap/v1/price",
                params={
                    "sellToken": "WETH",
                    "buyToken": "USDC",
                    "sellAmount": "1000000000000000000"  # 1 ETH in wei
                },
                headers=self.headers,
                timeout=10
            )
            if response.status_code == 200:
                self.is_connected = True
                logger.info(f"Connected to {self.name}")
                return True
            else:
                logger.error(f"Failed to connect to {self.name}: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Connection error to {self.name}: {e}")
            return False
    
    async def get_token_price(self, token_address: str, vs_token: str = "USDC") -> Optional[float]:
        """Get token price from 0x"""
        if not self.is_connected:
            await self.connect()
        
        try:
            response = requests.get(
                f"{self.base_url}/swap/v1/price",
                params={
                    "sellToken": token_address,
                    "buyToken": vs_token,
                    "sellAmount": "1000000000000000000"  # 1 token (assuming 18 decimals)
                },
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return float(data.get('price', 0))
            else:
                logger.warning(f"Failed to get price for {token_address}: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching price from {self.name}: {e}")
            return None

class WebSocketDataStream:
    """WebSocket data stream for real-time updates"""
    
    def __init__(self, url: str, headers: Dict[str, str] = None):
        self.url = url
        self.headers = headers or {}
        self.websocket = None
        self.is_running = False
        self.callbacks = {}
        self.message_queue = Queue()
    
    async def connect(self):
        """Connect to WebSocket"""
        try:
            self.websocket = await websockets.connect(
                self.url,
                extra_headers=self.headers
            )
            self.is_running = True
            logger.info(f"WebSocket connected to {self.url}")
            return True
        except Exception as e:
            logger.error(f"WebSocket connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from WebSocket"""
        self.is_running = False
        if self.websocket:
            await self.websocket.close()
            logger.info("WebSocket disconnected")
    
    async def subscribe(self, channel: str, callback):
        """Subscribe to a channel"""
        self.callbacks[channel] = callback
        
        # Send subscription message
        subscribe_msg = {
            "method": "subscribe",
            "params": [channel]
        }
        await self.websocket.send(json.dumps(subscribe_msg))
        logger.info(f"Subscribed to channel: {channel}")
    
    async def listen(self):
        """Listen for incoming messages"""
        while self.is_running and self.websocket:
            try:
                message = await self.websocket.recv()
                data = json.loads(message)
                
                # Route message to appropriate callback
                if 'channel' in data and data['channel'] in self.callbacks:
                    callback = self.callbacks[data['channel']]
                    await callback(data)
                else:
                    # Put in general queue
                    self.message_queue.put(data)
                    
            except websockets.exceptions.ConnectionClosed:
                logger.warning("WebSocket connection closed")
                break
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                break

class DataAggregator:
    """Aggregates data from multiple providers"""
    
    def __init__(self):
        self.providers: List[DataProvider] = []
        self.websocket_streams: List[WebSocketDataStream] = []
        self.token_cache = {}
        self.cache_ttl = 60  # Cache for 60 seconds
        self.is_running = False
    
    def add_provider(self, provider: DataProvider):
        """Add a data provider"""
        self.providers.append(provider)
        logger.info(f"Added provider: {provider.name}")
    
    def add_websocket_stream(self, stream: WebSocketDataStream):
        """Add a WebSocket stream"""
        self.websocket_streams.append(stream)
        logger.info(f"Added WebSocket stream: {stream.url}")
    
    async def start(self):
        """Start all data providers and streams"""
        self.is_running = True
        
        # Connect to all providers
        for provider in self.providers:
            await provider.connect()
        
        # Connect to all WebSocket streams
        for stream in self.websocket_streams:
            await stream.connect()
            # Start listening in background
            asyncio.create_task(stream.listen())
        
        logger.info("Data aggregator started")
    
    async def stop(self):
        """Stop all data providers and streams"""
        self.is_running = False
        
        # Disconnect from all providers
        for provider in self.providers:
            if hasattr(provider, 'disconnect'):
                await provider.disconnect()
        
        # Disconnect from all WebSocket streams
        for stream in self.websocket_streams:
            await stream.disconnect()
        
        logger.info("Data aggregator stopped")
    
    async def get_token_data(self, token_address: str) -> Optional[TokenData]:
        """Get token data with caching"""
        # Check cache first
        cache_key = f"token_{token_address}"
        if cache_key in self.token_cache:
            cached_data, timestamp = self.token_cache[cache_key]
            if time.time() - timestamp < self.cache_ttl:
                return cached_data
        
        # Try each provider until we get data
        for provider in self.providers:
            if provider.is_connected:
                try:
                    data = await provider.get_token_data(token_address)
                    if data:
                        # Cache the result
                        self.token_cache[cache_key] = (data, time.time())
                        return data
                except Exception as e:
                    logger.error(f"Error getting data from {provider.name}: {e}")
                    continue
        
        logger.warning(f"No data available for token {token_address}")
        return None
    
    async def get_token_price(self, token_address: str) -> Optional[float]:
        """Get current token price"""
        for provider in self.providers:
            if hasattr(provider, 'get_token_price') and provider.is_connected:
                try:
                    price = await provider.get_token_price(token_address)
                    if price:
                        return price
                except Exception as e:
                    logger.error(f"Error getting price from {provider.name}: {e}")
                    continue
        
        return None
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get health status of all providers"""
        status = {
            "aggregator_running": self.is_running,
            "providers": {},
            "websocket_streams": {},
            "cache_size": len(self.token_cache)
        }
        
        for provider in self.providers:
            status["providers"][provider.name] = {
                "connected": provider.is_connected,
                "last_update": provider.last_update
            }
        
        for i, stream in enumerate(self.websocket_streams):
            status["websocket_streams"][f"stream_{i}"] = {
                "running": stream.is_running,
                "url": stream.url
            }
        
        return status

# Example usage and testing
async def main():
    """Example usage of the data integration module"""
    logger.info("Initializing Data Integration Module...")
    
    # Create data aggregator
    aggregator = DataAggregator()
    
    # Add providers (with placeholder API keys)
    bitquery_provider = BitqueryProvider("YOUR_BITQUERY_API_KEY")
    zerox_provider = ZeroXProvider("YOUR_0X_API_KEY")
    
    aggregator.add_provider(bitquery_provider)
    aggregator.add_provider(zerox_provider)
    
    # Start the aggregator
    await aggregator.start()
    
    # Test token data retrieval
    test_tokens = [
        "0x55d398326f99059fF775485246999027B3197955",  # USDT on BSC
        "0xe9e7CEA3DedcA5984780Bafc599bD69ADd087D56",  # BUSD on BSC
    ]
    
    for token in test_tokens:
        logger.info(f"Fetching data for token: {token}")
        token_data = await aggregator.get_token_data(token)
        if token_data:
            logger.info(f"Token: {token_data.symbol} | Price: ${token_data.price_usd:.4f} | Volume: ${token_data.volume_24h:.2f}")
        else:
            logger.warning(f"No data found for token: {token}")
    
    # Get health status
    health = aggregator.get_health_status()
    logger.info(f"Health Status: {json.dumps(health, indent=2, default=str)}")
    
    # Stop the aggregator
    await aggregator.stop()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    asyncio.run(main())

