from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
import logging

# Logging for debugging (logs will show in Render)
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
AFF_LINK = "https://fktr.in/m96JCkl"

def extract_product_name(url):
    # 🟢 FIXED: More accurate regex for Flipkart product URL
    match = re.search(r"flipkart\.com/([^/]+)/p", url)
    if match:
        return match.group(1).replace("-", " ").title()
    return "Product"

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    logging.info(f"Incoming message: {incoming_msg}")
    resp = MessagingResponse()
    msg = resp.message()
    
    if "flipkart.com" in incoming_msg:
        product_name = extract_product_name(incoming_msg)
        msg.body(f"🛍️ Product: {product_name}\n🔗 Link: {AFF_LINK}")
    else:
        msg.body("❌ Kripya Flipkart ka valid link bhejiye.")
    
    return str(resp)

# ✅ For browser test (GET)
@app.route("/bot", methods=["GET"])
def test():
    return "🟢 Bot route is working!"

# ✅ App run config
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
