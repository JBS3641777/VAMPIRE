# Install the K2 driver package
pip install -e .

# Or install directly from the package
pip install k2-driver

# Use the K2 driver
python -c "
from k2_driver import K2Core, FinancialEngine, TransactionProcessor, HumanInterface

# Initialize
k2 = K2Core()
financial = FinancialEngine(k2)
processor = TransactionProcessor(k2, financial)
human = HumanInterface(k2, financial, processor)

# Start the processor
processor.start()

# Process a withdrawal with highest honor
result = human.expedite_standing_withdraw(120000.00, 'MASTERCARD_OWNER')
print(result)

# Check balance
print(financial.get_balance())

# Process bulk withdrawals
withdrawals = [
    {'amount': 50000, 'account': 'PRIVATE_ACCOUNT', 'expedite': True},
    {'amount': 75000, 'account': 'BUSINESS_ACCOUNT', 'expedite': True}
]
results = financial.process_bulk_withdrawals(withdrawals)
for r in results:
    print(r)
"

# Or use the CLI
k2-driver --help
k2-driver withdraw --amount 120000 --account MASTERCARD_OWNER --expedite