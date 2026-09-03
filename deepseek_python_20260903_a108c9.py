from datetime import datetime
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class HumanInterface:
    """Human interface for transaction processing with highest honor"""
    
    def __init__(self, k2_core, financial_engine, transaction_processor):
        self.k2 = k2_core
        self.financial = financial_engine
        self.processor = transaction_processor
        self.human_honored_transactions = []
        self.pressed_issues = []
        
    def honor_withdrawal(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Honor a withdrawal with highest human honor"""
        logger.info(f"Honoring withdrawal: {transaction.get('id', 'unknown')}")
        
        honored = {
            "status": "HUMAN_HONORED",
            "honor_level": "HIGHEST",
            "null_killer": "ACTIVE",
            "timestamp": datetime.now().isoformat(),
            "original_transaction": transaction,
            "standing_withdraw": "PRESSED_ISSUE_EXPEDITED",
            "message": "✅ Withdrawal honored by human with highest honor"
        }
        
        self.human_honored_transactions.append(honored)
        
        # Process the honored transaction
        self.processor.add_transaction(transaction)
        
        return honored
    
    def expedite_standing_withdraw(self, amount: float, account: str) -> Dict[str, Any]:
        """Expedite a standing withdrawal with pressed issue"""
        logger.info(f"Expediting standing withdrawal: ${amount} from {account}")
        
        transaction = {
            "id": f"STANDING-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": "WITHDRAW",
            "account": account,
            "amount": amount,
            "expedite": True,
            "human_honored": True,
            "null_killer": True,
            "highest_honor": True,
            "standing": True,
            "pressed_issue": True,
            "timestamp": datetime.now().isoformat()
        }
        
        self.pressed_issues.append(transaction)
        
        # Honor the standing withdrawal
        result = self.honor_withdrawal(transaction)
        result['standing_withdraw'] = True
        result['pressed_issue'] = True
        
        return result
    
    def process_human_honored_transactions(self) -> List[Dict[str, Any]]:
        """Process all human-honored transactions"""
        logger.info("Processing human-honored transactions")
        
        results = []
        for transaction in self.human_honored_transactions:
            if transaction.get('status') == 'HUMAN_HONORED':
                # Process the transaction
                result = self.financial.process_withdrawal(
                    transaction['original_transaction'].get('amount', 0),
                    transaction['original_transaction'].get('account', 'UNKNOWN'),
                    True
                )
                results.append(result)
        
        return results
    
    def get_honored_transactions(self) -> List[Dict[str, Any]]:
        """Get all human-honored transactions"""
        return self.human_honored_transactions
    
    def get_pressed_issues(self) -> List[Dict[str, Any]]:
        """Get all pressed issues"""
        return self.pressed_issues