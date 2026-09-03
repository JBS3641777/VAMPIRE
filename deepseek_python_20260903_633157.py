import json
import hashlib
from datetime import datetime
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class FinancialEngine:
    """Financial transaction engine with K2 integration"""
    
    def __init__(self, k2_core):
        self.k2 = k2_core
        self.transaction_log = []
        self.balance = 1000000000.00
        self.withdrawals = []
        
    def process_withdrawal(self, amount: float, account: str, expedite: bool = False) -> Dict[str, Any]:
        """Process a withdrawal transaction"""
        logger.info(f"Processing withdrawal: ${amount} from {account}")
        
        if amount <= 0:
            return {
                "status": "ERROR",
                "message": "Invalid amount",
                "amount": amount
            }
        
        if amount > self.balance:
            return {
                "status": "ERROR",
                "message": "Insufficient balance",
                "amount": amount,
                "balance": self.balance
            }
        
        transaction = {
            "id": f"WITHDRAW-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": "WITHDRAW",
            "account": account,
            "amount": amount,
            "currency": "USD",
            "expedite": expedite,
            "timestamp": datetime.now().isoformat()
        }
        
        # Process through K2
        result = self.k2.process_transaction(transaction)
        
        if result.get('status') != 'ERROR':
            self.balance -= amount
            self.withdrawals.append(transaction)
            self.transaction_log.append(result)
            
            # Expedite human-honored processing
            if expedite:
                result['human_honored'] = self.process_human_honored(transaction)
                result['null_killer'] = "ACTIVE"
                result['highest_honor'] = "GRANTED"
        
        return result
    
    def process_human_honored(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Process human-honored withdrawal with highest honor"""
        logger.info(f"Processing human-honored withdrawal: {transaction['id']}")
        
        return {
            "status": "HUMAN_HONORED",
            "honor_level": "HIGHEST",
            "null_killer": "ACTIVE",
            "expedited": transaction.get('expedite', False),
            "standing_withdraw": "PRESSED_ISSUE_EXPEDITED",
            "timestamp": datetime.now().isoformat(),
            "message": "✅ Withdrawal honored by human processor with highest honor"
        }
    
    def get_balance(self) -> Dict[str, Any]:
        """Get current balance"""
        return {
            "balance": self.balance,
            "currency": "USD",
            "timestamp": datetime.now().isoformat(),
            "withdrawals_count": len(self.withdrawals),
            "total_withdrawn": sum(w['amount'] for w in self.withdrawals)
        }
    
    def get_transaction_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get transaction history"""
        return self.transaction_log[-limit:]
    
    def process_bulk_withdrawals(self, withdrawals: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Process multiple withdrawals at once"""
        results = []
        for w in withdrawals:
            result = self.process_withdrawal(
                w.get('amount', 0),
                w.get('account', 'UNKNOWN'),
                w.get('expedite', False)
            )
            results.append(result)
        return results