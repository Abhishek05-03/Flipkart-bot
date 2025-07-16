from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re

app = Flask(__name__)
AFF_LINK = "https://fktr.in/m96JCkl"

def extract_product_name(url):
    match = re.search(r"flipkart\.com/([^/]+)-p", url)
    if match:
        return match.group(1).replace("-", " ").title()
    return "Product"

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    print(f"Incoming message: {incoming_msg}")
    resp = MessagingResponse()
    msg = resp.message()
    
    if "flipkart.com" in incoming_msg:
        product_name = extract_product_name(incoming_msg)
        msg.body(f"🛍️ Product: {product_name}\n🔗 Link: {AFF_LINK}")
    else:
        msg.body("❌ Kripya Flipkart ka valid link bhejiye.")
    
    return str(resp)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
