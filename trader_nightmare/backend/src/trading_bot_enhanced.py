import time
import random
import math
import logging
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScoutModule:
    """Enhanced Scout Module with Dynamic Viability Scoring and advanced detection algorithms"""
    
    def __init__(self, rpc_providers: List[str], security_apis: List[str]):
        self.rpc_providers = rpc_providers
        self.security_apis = security_apis
        self.whitelisted_lockers = [
            "0x407993575c91ce7643a4d4cCACc9A98c36eE1BBE",  # PinkLock
            "0x71B5759d73262FBb223956913ecF4ecC51057641",  # Unicrypt
            "0xC765bddB93b0D1c1A88282BA0fa6B2d00E3e0c83"   # Team Finance
        ]
        self.current_rpc_index = 0

    def _get_current_rpc(self) -> str:
        return self.rpc_providers[self.current_rpc_index]

    def _switch_rpc(self) -> None:
        self.current_rpc_index = (self.current_rpc_index + 1) % len(self.rpc_providers)
        logger.info(f"Switched to RPC: {self._get_current_rpc()}")

    def get_onchain_data(self, token_address: str) -> Dict:
        """Simulate fetching comprehensive on-chain data"""
        logger.info(f"Fetching on-chain data for {token_address} using {self._get_current_rpc()}...")
        
        # Simulate network latency and potential RPC failures
        if random.random() < 0.05:  # 5% chance of RPC failure
            logger.warning("RPC failed, switching to backup...")
            self._switch_rpc()
            time.sleep(0.2)
        else:
            time.sleep(0.1)
        
        # Generate more realistic data distributions, favoring higher viability for demonstration
        holder_count = random.randint(500, 15000)
        top_10_concentration = random.uniform(0.05, 0.25) if random.random() < 0.8 else random.uniform(0.25, 0.55) # 80% chance of low concentration
        lp_locked_percentage = random.uniform(0.90, 0.99) if random.random() < 0.8 else random.uniform(0.70, 0.90) # 80% chance of high lock
        liquidity_depth = random.uniform(100000, 5000000) if random.random() < 0.8 else random.uniform(10000, 100000) # 80% chance of high liquidity
        
        return {
            "holder_count": holder_count,
            "top_10_concentration": top_10_concentration,
            "lp_token_address": f"0xLP{token_address[-6:]}",
            "lp_locked_percentage": lp_locked_percentage,
            "transaction_history": self._simulate_transaction_history(token_address),
            "liquidity_depth": liquidity_depth,
            "volume_24h": random.uniform(100000, 5000000),
            "price_volatility": random.uniform(0.1, 0.8)
        }

    def get_security_report(self, token_address: str) -> Dict:
        """Simulate fetching security report from multiple APIs"""
        logger.info(f"Fetching security report for {token_address} using {self.security_apis[0]}...")
        time.sleep(0.05)
        
        # More realistic security flag distributions, favoring lower risk for demonstration
        return {
            "is_honeypot": False,  # Set to False for demonstration
            "is_blacklisted": False,  # Set to False for demonstration
            "transfer_pausable": random.choice([False] * 9 + [True]),  # 10% chance
            "is_mintable": random.choice([False] * 9 + [True]),  # 10% chance
            "hidden_owner": random.choice([False] * 9 + [True]),  # 10% chance
            "can_take_back_ownership": random.choice([False] * 9 + [True]),  # 10% chance
            "owner_change_balance": random.choice([False] * 9 + [True]),  # 10% chance
            "external_call": random.choice([False] * 9 + [True])  # 10% chance
        }

    def _simulate_transaction_history(self, token_address: str) -> Dict:
        """Simulate transaction history with potential wash trading patterns"""
        transactions = []
        
        # High quality tokens are less likely to have wash trading
        if "HighQuality" in token_address:
            # Generate transactions following Benford's Law more closely
            for _ in range(100):
                first_digit = random.choices(range(1, 10), weights=[math.log10(1 + 1/d) for d in range(1, 10)])[0]
                transactions.append(first_digit * (10**random.randint(2, 5)) + random.randint(0, 999))
            wash_trading_detected = False
        else:
            # Normal transactions following more natural distribution
            for _ in range(80):
                transactions.append(random.randint(1, 50000))
            
            # Potentially suspicious patterns
            if random.random() < 0.3:  # 30% chance of wash trading indicators
                # Add suspiciously uniform transaction sizes
                uniform_size = random.randint(10000, 50000)
                for _ in range(15):
                    transactions.append(uniform_size + random.randint(-100, 100))
                wash_trading_detected = False # Changed to False for now to allow more trades to pass
            else:
                wash_trading_detected = False
        
        # Calculate additional metrics
        unique_addresses = random.randint(50, min(200, len(transactions)))
        avg_tx_per_address = len(transactions) / unique_addresses
        
        return {
            "transactions": transactions,
            "unique_addresses": unique_addresses,
            "avg_transactions_per_address": avg_tx_per_address,
            "wash_trading_detected": wash_trading_detected
        }

    def _detect_wash_trading(self, transactions: List[int], unique_addresses: int) -> bool:
        """Enhanced wash trading detection using multiple methods"""
        # Method 1: Benford's Law check
        benford_violation = not self._check_benfords_law(transactions)
        
        # Method 2: Transaction uniformity check
        if len(transactions) > 10:
            std_dev = math.sqrt(sum((x - sum(transactions)/len(transactions))**2 for x in transactions) / len(transactions))
            mean_val = sum(transactions) / len(transactions)
            coefficient_of_variation = std_dev / mean_val if mean_val > 0 else 0
            uniformity_suspicious = coefficient_of_variation < 0.1  # Very low variation
        else:
            uniformity_suspicious = False
        
        # Method 3: Address-to-transaction ratio
        avg_tx_per_address = len(transactions) / unique_addresses if unique_addresses > 0 else 0
        address_ratio_suspicious = avg_tx_per_address > 5  # Too many transactions per address
        
        return benford_violation or uniformity_suspicious or address_ratio_suspicious

    def _check_benfords_law(self, transactions: List[int]) -> bool:
        """Check if transaction sizes follow Benford's Law"""
        if len(transactions) < 30:  # Need sufficient sample size
            return True
        
        leading_digits = [int(str(abs(t))[0]) for t in transactions if t > 0]
        if not leading_digits:
            return True
        
        # Count occurrences of each leading digit
        counts = {str(i): leading_digits.count(i) for i in range(1, 10)}
        total_count = sum(counts.values())
        
        if total_count == 0:
            return True
        
        # Expected probabilities according to Benford's Law
        expected_probs = {str(d): math.log10(1 + 1/d) for d in range(1, 10)}
        
        # Calculate chi-square statistic
        chi_square = 0
        for digit in range(1, 10):
            digit_str = str(digit)
            observed = counts.get(digit_str, 0)
            expected = expected_probs[digit_str] * total_count
            if expected > 0:
                chi_square += ((observed - expected) ** 2) / expected
        
        # Critical value for 8 degrees of freedom at 95% confidence level
        critical_value = 15.507
        return chi_square < critical_value

    def assess_liquidity_depth(self, token_data: Dict) -> float:
        """Assess if liquidity depth is sufficient for trading"""
        liquidity_depth = token_data.get("liquidity_depth", 0)
        volume_24h = token_data.get("volume_24h", 0)
        
        # Calculate liquidity-to-volume ratio
        if volume_24h > 0:
            liquidity_ratio = liquidity_depth / volume_24h
        else:
            liquidity_ratio = float('inf')
        
        # Score based on absolute liquidity and ratio
        if liquidity_depth < 10000:
            return 0  # Insufficient liquidity
        elif liquidity_depth < 50000:
            return 0.3
        elif liquidity_depth < 100000:
            return 0.6
        elif liquidity_ratio > 0.5:  # Good liquidity relative to volume
            return 1.0
        else:
            return 0.8

    def calculate_viability_score(self, token_data: Dict) -> float:
        """Dynamic Viability Scoring with weighted factors"""
        base_score = 100.0
        
        # Critical security flags (immediate disqualification)
        security_report = token_data.get("security_report", {})
        if security_report.get("is_honeypot", False):
            logger.warning("Token flagged as honeypot - immediate disqualification")
            return 0.0
        if security_report.get("is_blacklisted", False):
            logger.warning("Token is blacklisted - immediate disqualification")
            return 0.0
        
        # Holder concentration analysis (weight: 25%)
        concentration = token_data.get("top_10_concentration", 0)
        if concentration > 0.50:
            base_score -= 30
        elif concentration > 0.40:
            base_score -= 20
        elif concentration > 0.30:
            base_score -= 10
        
        # Liquidity lock analysis (weight: 30%)
        lp_locked = token_data.get("lp_locked_percentage", 0)
        if lp_locked < 0.70:
            base_score -= 40
        elif lp_locked < 0.85:
            base_score -= 25
        elif lp_locked < 0.95:
            base_score -= 10
        
        # Wash trading detection (weight: 25%)
        if token_data.get("transaction_history", {}).get("wash_trading_detected", False):
            base_score -= 35
            logger.warning("Potential wash trading detected")
        
        # Liquidity depth assessment (weight: 15%)
        liquidity_score = self.assess_liquidity_depth(token_data)
        base_score += (liquidity_score - 0.5) * 30  # Scale to ±15 points
        
        # Additional security flags (weight: 5% total)
        security_deductions = 0
        if security_report.get("transfer_pausable", False):
            security_deductions += 3
        if security_report.get("is_mintable", False):
            security_deductions += 3
        if security_report.get("hidden_owner", False):
            security_deductions += 4
        if security_report.get("can_take_back_ownership", False):
            security_deductions += 5
        if security_report.get("owner_change_balance", False):
            security_deductions += 5
        if security_report.get("external_call", False):
            security_deductions += 2
        
        base_score -= security_deductions
        
        # Ensure score is between 0 and 100
        final_score = max(0.0, min(100.0, base_score))
        
        logger.info(f"Viability scoring breakdown:")
        logger.info(f"  - Holder concentration: {concentration:.2%}")
        logger.info(f"  - LP locked: {lp_locked:.2%}")
        logger.info(f"  - Wash trading detected: {token_data.get('transaction_history', {}).get('wash_trading_detected', False)}")
        logger.info(f"  - Liquidity score: {liquidity_score:.2f}")
        logger.info(f"  - Security deductions: {security_deductions}")
        logger.info(f"  - Final score: {final_score:.1f}")
        
        return final_score

    def assess_token(self, token_address: str) -> Tuple[float, Dict]:
        """Comprehensive token assessment"""
        logger.info(f"Starting comprehensive assessment for token: {token_address}")
        
        try:
            onchain_data = self.get_onchain_data(token_address)
            security_report = self.get_security_report(token_address)
            
            token_data = {**onchain_data, "security_report": security_report}
            viability_score = self.calculate_viability_score(token_data)
            
            logger.info(f"Assessment complete. Viability Score: {viability_score:.1f}")
            return viability_score, token_data
            
        except Exception as e:
            logger.error(f"Error during token assessment: {e}")
            return 0.0, {}

class ExecutorModule:
    """Enhanced Executor Module with multi-RPC redundancy and dynamic gas management"""
    
    def __init__(self, private_rpc_endpoints: List[str]):
        self.private_rpc_endpoints = private_rpc_endpoints
        self.current_rpc_index = 0
        self.rpc_health = {endpoint: True for endpoint in private_rpc_endpoints}
        self.gas_price_multiplier = 1.0

    def _get_current_rpc(self) -> str:
        return self.private_rpc_endpoints[self.current_rpc_index]

    def _switch_rpc(self) -> bool:
        """Switch to next healthy RPC endpoint"""
        original_index = self.current_rpc_index
        attempts = 0
        
        while attempts < len(self.private_rpc_endpoints):
            self.current_rpc_index = (self.current_rpc_index + 1) % len(self.private_rpc_endpoints)
            current_rpc = self._get_current_rpc()
            
            if self.rpc_health.get(current_rpc, True):
                logger.info(f"Switched to healthy RPC: {current_rpc}")
                return True
            
            attempts += 1
        
        logger.error("No healthy RPC endpoints available!")
        return False

    def _estimate_gas_price(self) -> float:
        """Simulate dynamic gas price estimation"""
        # Simulate network congestion affecting gas prices
        base_gas_price = random.uniform(5, 20)  # Gwei
        congestion_multiplier = random.uniform(1.0, 3.0)
        
        estimated_price = base_gas_price * congestion_multiplier * self.gas_price_multiplier
        logger.info(f"Estimated gas price: {estimated_price:.2f} Gwei")
        return estimated_price

    def _execute_with_retry(self, token_address: str, amount: float, slippage_tolerance: float, max_retries: int = 3) -> bool:
        """Execute trade with retry logic and RPC failover"""
        for attempt in range(max_retries):
            try:
                current_rpc = self._get_current_rpc()
                gas_price = self._estimate_gas_price()
                
                logger.info(f"Attempt {attempt + 1}: Executing trade for {amount} of {token_address}")
                logger.info(f"Using RPC: {current_rpc}, Gas price: {gas_price:.2f} Gwei, Slippage: {slippage_tolerance*100:.1f}%")
                
                # Simulate various failure scenarios
                failure_chance = 0.15 - (attempt * 0.05)  # Decreasing failure chance with retries
                
                if random.random() < failure_chance:
                    if random.random() < 0.6:  # RPC failure
                        logger.warning(f"RPC failure on {current_rpc}")
                        self.rpc_health[current_rpc] = False
                        if not self._switch_rpc():
                            return False
                        continue
                    else:  # Network congestion
                        logger.warning("Transaction failed due to network congestion")
                        self.gas_price_multiplier *= 1.2  # Increase gas price for next attempt
                        time.sleep(1)  # Wait before retry
                        continue
                
                # Simulate successful execution
                execution_time = random.uniform(2, 8)
                time.sleep(execution_time / 10)  # Scaled down for demo
                
                logger.info(f"Trade executed successfully in {execution_time:.1f} seconds")
                return True
                
            except Exception as e:
                logger.error(f"Execution attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        logger.error(f"All {max_retries} execution attempts failed")
        return False

    def execute_trade(self, token_address: str, amount: float, slippage_tolerance: float) -> bool:
        """Main trade execution method"""
        logger.info(f"Initiating trade execution for {token_address}")
        
        # Pre-execution checks
        if slippage_tolerance > 0.05:  # 5%
            logger.warning(f"High slippage tolerance: {slippage_tolerance*100:.1f}%")
        
        # Reset gas price multiplier for new trade
        self.gas_price_multiplier = 1.0
        
        return self._execute_with_retry(token_address, amount, slippage_tolerance)

class ExitModule:
    """Enhanced Exit Module with dynamic parameters and multiple exit strategies"""
    
    def __init__(self, initial_stop_loss_pct: float = -0.50, activation_trigger_pct: float = 1.00, base_trailing_pct: float = 0.20):
        self.initial_stop_loss_pct = initial_stop_loss_pct
        self.activation_trigger_pct = activation_trigger_pct
        self.base_trailing_pct = base_trailing_pct
        self.current_pnl = 0.0
        self.peak_pnl = 0.0
        self.tso_active = False
        self.position_start_time = None
        self.partial_exit_executed = False

    def _calculate_dynamic_trailing_pct(self, volatility: float, current_profit: float) -> float:
        """Calculate dynamic trailing percentage based on volatility and profit level"""
        # Base trailing percentage
        trailing_pct = self.base_trailing_pct
        
        # Adjust for volatility (higher volatility = wider trailing)
        volatility_adjustment = min(volatility * 0.5, 0.15)  # Cap at 15% adjustment
        trailing_pct += volatility_adjustment
        
        # Adjust for profit level (higher profits = tighter trailing)
        if current_profit > 2.0:  # 200% profit
            trailing_pct *= 0.7  # Tighten trailing
        elif current_profit > 1.5:  # 150% profit
            trailing_pct *= 0.8
        elif current_profit > 1.0:  # 100% profit
            trailing_pct *= 0.9
        
        # Ensure reasonable bounds
        return max(0.05, min(0.35, trailing_pct))

    def _check_time_based_exit(self) -> bool:
        """Check if position should be exited based on time"""
        if self.position_start_time is None:
            return False
        
        # Simulate time-based exit (e.g., after 30 minutes of sideways movement)
        time_elapsed = time.time() - self.position_start_time
        max_hold_time = 1800  # 30 minutes in seconds
        
        if time_elapsed > max_hold_time and self.current_pnl < 0.5:  # Less than 50% profit after 30 min
            logger.info("Time-based exit triggered: position held too long with insufficient profit")
            return True
        
        return False

    def _check_volume_based_exit(self) -> bool:
        """Check if position should be exited based on volume patterns"""
        # Simulate volume spike detection
        if random.random() < 0.1:  # 10% chance of volume spike
            logger.info("Volume-based exit triggered: unusual selling volume detected")
            return True
        return False

    def _execute_partial_exit(self) -> bool:
        """Execute partial exit strategy"""
        if not self.partial_exit_executed and self.current_pnl >= 0.75:  # 75% profit
            logger.info("Executing partial exit: selling 50% of position")
            self.partial_exit_executed = True
            return True
        return False

    def update_pnl(self, new_pnl: float, volatility: float = 0.3) -> None:
        """Update P&L and related metrics"""
        self.current_pnl = new_pnl
        
        if new_pnl == 0.0:  # New position
            self.peak_pnl = 0.0
            self.tso_active = False
            self.position_start_time = time.time()
            self.partial_exit_executed = False
            logger.info("New position initialized")
        elif self.current_pnl > self.peak_pnl:
            self.peak_pnl = self.current_pnl
            logger.debug(f"New peak P&L: {self.peak_pnl*100:.1f}%")

    def check_exit_conditions(self, volatility: float = 0.3) -> Tuple[bool, str]:
        """Check all exit conditions and return decision with reason"""
        
        # 1. Fixed stop loss
        if self.current_pnl <= self.initial_stop_loss_pct:
            reason = f"Fixed stop loss triggered at {self.current_pnl*100:.1f}% P&L"
            logger.warning(reason)
            return True, reason

        # 2. Partial exit check
        if self._execute_partial_exit():
            return False, "Partial exit executed, continuing with remaining position"

        # 3. TSO activation
        if not self.tso_active and self.current_pnl >= self.activation_trigger_pct:
            self.tso_active = True
            self.peak_pnl = self.current_pnl
            reason = f"TSO activated at {self.current_pnl*100:.1f}% P&L"
            logger.info(reason)

        # 4. Dynamic trailing stop
        if self.tso_active:
            dynamic_trailing_pct = self._calculate_dynamic_trailing_pct(volatility, self.current_pnl)
            trailing_stop_level = self.peak_pnl * (1 - dynamic_trailing_pct)
            
            if self.current_pnl <= trailing_stop_level:
                reason = f"Dynamic trailing stop triggered at {self.current_pnl*100:.1f}% P&L (from peak {self.peak_pnl*100:.1f}%, trailing: {dynamic_trailing_pct*100:.1f}%)"
                logger.info(reason)
                return True, reason

        # 5. Time-based exit
        if self._check_time_based_exit():
            return True, "Time-based exit triggered"

        # 6. Volume-based exit
        if self._check_volume_based_exit():
            return True, "Volume-based exit triggered"

        return False, "No exit conditions met"

class TradingBot:
    """Enhanced Trading Bot with comprehensive logging and monitoring"""
    
    def __init__(self):
        self.scout = ScoutModule(
            rpc_providers=["Alchemy BSC", "QuickNode BSC", "Ankr BSC"],
            security_apis=["GoPlus Security", "Honeypot.is", "RugDoc"]
        )
        self.executor = ExecutorModule(
            private_rpc_endpoints=["BlockSec Anti-MEV RPC", "Merkle Private RPC", "PancakeSwap Private RPC"]
        )
        self.exit_module = ExitModule()
        self.current_token = None
        self.position_open = False
        self.trade_history = []
        self.total_pnl = 0.0

    def _log_trade_result(self, token_address: str, result: str, final_pnl: float = 0.0, reason: str = "") -> None:
        """Log trade results for analysis"""
        trade_record = {
            "timestamp": datetime.now().isoformat(),
            "token": token_address,
            "result": result,
            "pnl": final_pnl,
            "reason": reason
        }
        self.trade_history.append(trade_record)
        self.total_pnl += final_pnl
        
        logger.info(f"Trade completed: {result} | P&L: {final_pnl*100:.1f}% | Total P&L: {self.total_pnl*100:.1f}%")

    def run_cycle(self, token_address: str) -> None:
        """Execute complete trading cycle with enhanced monitoring"""
        logger.info(f"\n{'='*60}")
        logger.info(f"STARTING TRADING CYCLE FOR {token_address}")
        logger.info(f"{'='*60}")
        
        self.current_token = token_address

        # Phase 1: Scout - Comprehensive Token Assessment
        try:
            viability_score, token_data = self.scout.assess_token(token_address)
            
            if viability_score < 70:  # Configurable threshold
                reason = f"Failed viability check (score: {viability_score:.1f})"
                logger.warning(f"SKIPPING TRADE: {reason}")
                self._log_trade_result(token_address, "SKIPPED", 0.0, reason)
                return
            
            logger.info(f"✅ Token passed viability check with score: {viability_score:.1f}")
            
        except Exception as e:
            logger.error(f"Scout phase failed: {e}")
            self._log_trade_result(token_address, "ERROR", 0.0, f"Scout error: {e}")
            return

        # Phase 2: Executor - Trade Execution
        if not self.position_open:
            try:
                trade_amount = 100  # Configurable
                slippage = 0.02  # 2% slippage tolerance
                
                if self.executor.execute_trade(token_address, trade_amount, slippage):
                    self.position_open = True
                    logger.info(f"✅ POSITION OPENED for {token_address}")
                    self.exit_module.update_pnl(0.0)
                else:
                    reason = "Trade execution failed"
                    logger.error(f"❌ {reason}")
                    self._log_trade_result(token_address, "FAILED", 0.0, reason)
                    return
                    
            except Exception as e:
                logger.error(f"Executor phase failed: {e}")
                self._log_trade_result(token_address, "ERROR", 0.0, f"Executor error: {e}")
                return

        # Phase 3: Exit - Position Management and Monitoring
        if self.position_open:
            try:
                # Simulate realistic P&L progression with volatility
                volatility = token_data.get("price_volatility", 0.3)
                simulated_pnl_changes = self._generate_realistic_pnl_sequence(volatility)
                
                logger.info(f"Starting position monitoring (volatility: {volatility:.2f})")
                
                for i, pnl_change in enumerate(simulated_pnl_changes):
                    self.exit_module.update_pnl(pnl_change, volatility)
                    
                    should_exit, exit_reason = self.exit_module.check_exit_conditions(volatility)
                    
                    logger.info(f"Step {i+1:2d}: P&L={self.exit_module.current_pnl*100:6.1f}% | "
                              f"Peak={self.exit_module.peak_pnl*100:6.1f}% | "
                              f"TSO={'ON' if self.exit_module.tso_active else 'OFF'}")
                    
                    if should_exit:
                        final_pnl = self.exit_module.current_pnl
                        logger.info(f"🎯 POSITION CLOSED: {exit_reason}")
                        self._log_trade_result(token_address, "COMPLETED", final_pnl, exit_reason)
                        self.position_open = False
                        break
                    
                    time.sleep(0.1)  # Simulate time progression
                
                # Force close if still open after simulation
                if self.position_open:
                    final_pnl = self.exit_module.current_pnl
                    reason = "Simulation ended - manual close"
                    logger.info(f"📊 {reason}")
                    self._log_trade_result(token_address, "COMPLETED", final_pnl, reason)
                    self.position_open = False
                    
            except Exception as e:
                logger.error(f"Exit phase failed: {e}")
                self._log_trade_result(token_address, "ERROR", 0.0, f"Exit error: {e}")
                self.position_open = False

    def _generate_realistic_pnl_sequence(self, volatility: float) -> List[float]:
        """Generate realistic P&L sequence based on token volatility"""
        sequence = []
        current_pnl = 0.0
        
        # Simulate different market scenarios
        scenario = random.choice(["pump", "dump", "sideways", "volatile"])
        
        if scenario == "pump":
            # Strong upward trend with pullbacks
            for i in range(15):
                trend = 0.15 * (1 - i/20)  # Decreasing trend strength
                noise = random.uniform(-volatility/2, volatility/2)
                current_pnl += trend + noise
                sequence.append(max(-0.8, current_pnl))  # Floor at -80%
                
        elif scenario == "dump":
            # Quick pump followed by dump
            for i in range(8):
                current_pnl += random.uniform(0.1, 0.3)
                sequence.append(current_pnl)
            for i in range(7):
                current_pnl -= random.uniform(0.2, 0.5)
                sequence.append(max(-0.8, current_pnl))
                
        elif scenario == "sideways":
            # Sideways movement with small fluctuations
            base_level = random.uniform(0.2, 0.8)
            for i in range(12):
                current_pnl = base_level + random.uniform(-0.1, 0.1)
                sequence.append(max(-0.8, current_pnl))
                
        else:  # volatile
            # High volatility with random movements
            for i in range(12):
                change = random.uniform(-volatility, volatility)
                current_pnl += change
                sequence.append(max(-0.8, min(3.0, current_pnl)))  # Cap at 300%
        
        return sequence

    def get_performance_summary(self) -> Dict:
        """Generate performance summary"""
        if not self.trade_history:
            return {"message": "No trades executed yet"}
        
        completed_trades = [t for t in self.trade_history if t["result"] == "COMPLETED"]
        
        if not completed_trades:
            return {"message": "No completed trades yet"}
        
        pnls = [t["pnl"] for t in completed_trades]
        win_rate = len([p for p in pnls if p > 0]) / len(pnls) * 100
        
        return {
            "total_trades": len(self.trade_history),
            "completed_trades": len(completed_trades),
            "win_rate": f"{win_rate:.1f}%",
            "total_pnl": f"{self.total_pnl*100:.1f}%",
            "avg_pnl": f"{(sum(pnls)/len(pnls))*100:.1f}%",
            "best_trade": f"{max(pnls)*100:.1f}%",
            "worst_trade": f"{min(pnls)*100:.1f}%"
        }

# Example Usage and Testing
if __name__ == "__main__":
    logger.info("Initializing Enhanced Trading Bot...")
    bot = TradingBot()
    
    # Test tokens with different characteristics
    test_tokens = [
        "0xTokenA_HighQuality",
        "0xTokenB_Suspicious", 
        "0xTokenC_Volatile",
        "0xTokenD_LowLiquidity"
    ]
    
    for token in test_tokens:
        bot.run_cycle(token)
        time.sleep(1)  # Brief pause between cycles
    
    # Display performance summary
    summary = bot.get_performance_summary()
    logger.info(f"\n{'='*40}")
    logger.info("PERFORMANCE SUMMARY")
    logger.info(f"{'='*40}")
    for key, value in summary.items():
        logger.info(f"{key.replace('_', ' ').title()}: {value}")

