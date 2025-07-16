from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
import logging
import requests

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
AFF_LINK = "https://fktr.in/m96JCkl"

def expand_url(short_url):
    try:
        response = requests.get(short_url, allow_redirects=True, timeout=5)
        final_url = response.url
        logging.info(f"Expanded URL: {final_url}")
        return final_url
    except Exception as e:
        logging.error(f"Failed to expand URL: {e}")
        return short_url

def extract_product_name(url):
    # Expand short links like fkrt.co
    if "fkrt.co" in url:
        url = expand_url(url)

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
    
    if "flipkart.com" in incoming_msg or "fkrt.co" in incoming_msg:
        product_name = extract_product_name(incoming_msg)
        msg.body(f"🛍️ Product: {product_name}\n🔗 Link: {AFF_LINK}")
    else:
        msg.body("❌ Kripya Flipkart ka valid link bhejiye.")
    
    return str(resp)

# GET route for testing
@app.route("/bot", methods=["GET"])
def test():
    return "🟢 Bot route is working!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
