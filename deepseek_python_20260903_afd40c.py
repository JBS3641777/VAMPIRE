import threading
import queue
import time
from datetime import datetime
from typing import Dict, Any, List
import logging

logger = logging.getLogger(__name__)

class TransactionProcessor:
    """Real-time transaction processor with K2 integration"""
    
    def __init__(self, k2_core, financial_engine):
        self.k2 = k2_core
        self.financial = financial_engine
        self.transaction_queue = queue.Queue()
        self.processing_thread = None
        self.is_processing = False
        self.processed_transactions = []
        
    def start(self):
        """Start the transaction processor thread"""
        if self.processing_thread and self.processing_thread.is_alive():
            logger.warning("Transaction processor already running")
            return
        
        self.is_processing = True
        self.processing_thread = threading.Thread(target=self._process_loop)
        self.processing_thread.daemon = True
        self.processing_thread.start()
        logger.info("Transaction processor started")
    
    def stop(self):
        """Stop the transaction processor"""
        self.is_processing = False
        if self.processing_thread:
            self.processing_thread.join(timeout=10)
        logger.info("Transaction processor stopped")
    
    def add_transaction(self, transaction: Dict[str, Any]):
        """Add transaction to processing queue"""
        self.transaction_queue.put(transaction)
        logger.info(f"Transaction added to queue: {transaction.get('id', 'unknown')}")
    
    def _process_loop(self):
        """Main processing loop"""
        while self.is_processing:
            try:
                transaction = self.transaction_queue.get(timeout=1)
                if transaction:
                    result = self._process_single_transaction(transaction)
                    self.processed_transactions.append(result)
                    logger.info(f"Transaction processed: {transaction.get('id', 'unknown')}")
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Transaction processing error: {e}")
    
    def _process_single_transaction(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Process a single transaction"""
        try:
            if transaction.get('type', '').upper() == 'WITHDRAW':
                return self.financial.process_withdrawal(
                    transaction.get('amount', 0),
                    transaction.get('account', 'UNKNOWN'),
                    transaction.get('expedite', False)
                )
            elif transaction.get('type', '').upper() == 'TRANSFER':
                return self._process_transfer(transaction)
            else:
                return {
                    "status": "ERROR",
                    "message": "Unknown transaction type",
                    "transaction": transaction
                }
        except Exception as e:
            logger.error(f"Transaction processing error: {e}")
            return {
                "status": "ERROR",
                "message": str(e),
                "transaction": transaction
            }
    
    def _process_transfer(self, transaction: Dict[str, Any]) -> Dict[str, Any]:
        """Process a transfer transaction"""
        # Implementation for transfers
        return {
            "status": "PROCESSED",
            "type": "TRANSFER",
            "transaction": transaction,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get queue status"""
        return {
            "queue_size": self.transaction_queue.qsize(),
            "processed_count": len(self.processed_transactions),
            "is_processing": self.is_processing,
            "timestamp": datetime.now().isoformat()
        }
    
    def expedite_withdrawal(self, amount: float, account: str) -> Dict[str, Any]:
        """Expedite a withdrawal with highest honor"""
        logger.info(f"Expediting withdrawal: ${amount} from {account}")
        
        transaction = {
            "id": f"EXPEDITE-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": "WITHDRAW",
            "account": account,
            "amount": amount,
            "expedite": True,
            "human_honored": True,
            "null_killer": True,
            "highest_honor": True,
            "timestamp": datetime.now().isoformat()
        }
        
        self.add_transaction(transaction)
        
        return {
            "status": "EXPEDITED",
            "message": "✅ Withdrawal expedited with highest honor",
            "transaction": transaction,
            "human_honored": True,
            "null_killer": "ACTIVE"
        }