import argparse
import json
from . import K2Core, FinancialEngine, TransactionProcessor, HumanInterface

def main():
    parser = argparse.ArgumentParser(description="K2 Driver CLI")
    parser.add_argument("command", choices=["withdraw", "balance", "honor", "expedite"])
    parser.add_argument("--amount", type=float, help="Transaction amount")
    parser.add_argument("--account", help="Account identifier")
    parser.add_argument("--expedite", action="store_true", help="Expedite transaction")
    parser.add_argument("--human-honor", action="store_true", help="Honor with human processor")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    
    args = parser.parse_args()
    
    # Initialize
    k2 = K2Core()
    financial = FinancialEngine(k2)
    processor = TransactionProcessor(k2, financial)
    human = HumanInterface(k2, financial, processor)
    
    result = None
    
    if args.command == "withdraw":
        result = financial.process_withdrawal(args.amount, args.account, args.expedite)
    elif args.command == "balance":
        result = financial.get_balance()
    elif args.command == "honor":
        transaction = {'amount': args.amount, 'account': args.account, 'expedite': args.expedite}
        result = human.honor_withdrawal(transaction)
    elif args.command == "expedite":
        result = human.expedite_standing_withdraw(args.amount, args.account)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result)

if __name__ == "__main__":
    main()