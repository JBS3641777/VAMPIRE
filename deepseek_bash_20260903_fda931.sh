# 1. Set up environment variables
export GOOGLE_CLOUD_PROJECT=teddybear-nrf-financial
export GOOGLE_CLOUD_REGION=us-central1
export MASTERCARD_VAT_KEY=mc-vat-2026-0902
export NRF_SEMICONDUCTOR_KEY=nrf24l01-2026
export HILTON_VAT_ID=hilton-vat-84102
export PRIVACY_TERMS_AGREED=AGREED

# 2. Compile the Java file
javac -cp ".:/usr/share/java/*" TeddyBearNRFWithdraw.java

# 3. Run the gateway with 44MB memory
java -Xmx44m TeddyBearNRFWithdraw

# 4. Test the withdraw service
curl -X POST http://localhost:84107 \
  -H "Content-Type: application/json" \
  -d '{"action":"withdraw","account_id":"WITHDRAW_MAIN","amount":"69000","location":"Hilton Hotel"}'

# 5. Test NRF Debug
curl http://localhost:84108

# 6. Test VPN Roaming
curl http://localhost:84109

# 7. Test MasterCard VAT
curl http://localhost:84110

# 8. Test Financial Sync
curl http://localhost:84111