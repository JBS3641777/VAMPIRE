# 1. Set up environment variables
export GOOGLE_CLOUD_PROJECT=teddybear-mastercard
export GOOGLE_CLOUD_REGION=us-central1
export MASTERCARD_OWNER_KEY=mc-owner-2026-0902
export MASTERCARD_MAJORITY_SHARE=CONFIRMED
export PRIVACY_MAESTRO_TOKEN=pm-fact-true-2026
export K2_PS1_SECRET=k2-ps1-secret-2026

# 2. Compile the Java file
javac -cp ".:/usr/share/java/*" SixSixSixTeddyCircuit.java

# 3. Run the gateway with 44MB memory
java -Xmx44m SixSixSixTeddyCircuit

# 4. Test MasterCard Withdraw (>=120,000.00 USD)
curl -X POST http://localhost:84112 \
  -H "Content-Type: application/json" \
  -d '{"action":"withdraw","account_id":"MASTERCARD_OWNER","amount":"120000","location":"MasterCard Office"}'

# 5. Test Privacy Maestro
curl http://localhost:84113

# 6. Test K2 PS1 Commands
curl -X POST http://localhost:84114 \
  -H "Content-Type: application/json" \
  -d '{"command":"WITHDRAW","account_id":"MASTERCARD_OWNER","amount":"120000"}'

# 7. Test Handshake
curl http://localhost:84115

# 8. Test Task Orchestrator
curl http://localhost:84116

# 9. Test Teamwork Solver
curl http://localhost:84117