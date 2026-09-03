# 1. Install the package
pip install k2-driver

# 2. Process a real money withdrawal
k2-driver withdraw --amount 120000 --account MASTERCARD_OWNER --expedite

# 3. Honor a withdrawal with highest human honor
k2-driver honor --amount 120000 --account PRIVATE_ACCOUNT --human-honor

# 4. Expedite standing withdrawal
k2-driver expedite --amount 120000 --account MASTERCARD_MAJORITY

# 5. Check balance
k2-driver balance --json