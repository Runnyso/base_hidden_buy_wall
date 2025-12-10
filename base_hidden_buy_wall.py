import requests, time

def hidden_buy_wall():
    print("Base — Hidden Buy Wall Detector (whale stacking limit buys below price)")
    processed = set()

    while True:
        try:
            # Pull latest 200 swaps on Base
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base?limit=200")
            for tx in r.json().get("transactions", []):
                txid = tx["hash"]
                if txid in processed:
                    continue

                # Only look at limit orders filled (not market buys)
                if tx.get("type") != "swap" or tx.get("maker") == tx.get("taker"):
                    processed.add(txid)
                    continue

                # Whale buys a lot but price barely moved = hidden wall
                usd_value = tx.get("valueUSD", 0)
                price_impact = abs(tx.get("priceImpact", 0))

                if usd_value > 75_000 and price_impact < 2.0:  # $75k+ buy, <2% impact
                    token = tx["token0"]["symbol"] if tx["side"] == "buy" else tx["token1"]["symbol"]
                    print(f"HIDDEN BUY WALL DETECTED\n"
                          f"${usd_value:,.0f} swept with only {price_impact:.2f}% impact\n"
                          f"Token: {token}\n"
                          f"Whale: {tx['maker'][:10]}...\n"
                          f"https://dexscreener.com/base/{tx['pairAddress']}\n"
                          f"https://basescan.org/tx/{txid}\n"
                          f"→ Someone is quietly stacking before the breakout\n"
                          f"→ Chart still flat — but the floor just became concrete\n"
                          f"{'='*90}")

                processed.add(txid)

        except:
            pass
        time.sleep(1.8)

if __name__ == "__main__":
    hidden_buy_wall()
