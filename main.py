from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re
import requests
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
AFF_LINK = "https://fktr.in/m96JCkl"

# Expand any short link to real destination
def expand_url(url):
    try:
        response = requests.get(url, allow_redirects=True, timeout=3)
        final_url = response.url
        logging.info(f"Expanded URL: {final_url}")
        return final_url
    except Exception as e:
        logging.error(f"URL Expansion Failed: {e}")
        return url

# Extract product name from any e-commerce link (Flipkart, Amazon, etc.)
def extract_product_name(url):
    url = expand_url(url)
    product_name = "Product"

    try:
        # Try Flipkart pattern
        match = re.search(r"flipkart\.com/([^/?]+)", url)
        if match:
            product_name = match.group(1).replace("-", " ").title()
            return product_name
        
        # Try Amazon pattern
        match = re.search(r"amazon\.(?:in|com)/(?:gp/product|dp)/([^/?]+)", url)
        if match:
            product_name = match.group(1).replace("-", " ").title()
            return product_name

        # Generic fallback
        match = re.search(r"/([^/?]+)", url)
        if match:
            product_name = match.group(1).replace("-", " ").title()
            return product_name
    except:
        pass

    return product_name

# Find all links in the message
def extract_all_links(text):
    return re.findall(r'https?://[^\s]+', text)

# Final response generator
def generate_reply(msg):
    links = extract_all_links(msg)
    if not links:
        return "❌ Kripya ek valid product link bhejiye."

    final_reply = ""
    for link in links:
        product_name = extract_product_name(link)
        final_reply += f"🛍️ Product: {product_name}\n🔗 Link: {AFF_LINK}\n\n"

    return final_reply.strip()

# WhatsApp message handler
@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    logging.info(f"Incoming message: {incoming_msg}")
    resp = MessagingResponse()
    msg = resp.message()
    msg.body(generate_reply(incoming_msg))
    return str(resp)

# For testing
@app.route("/bot", methods=["GET"])
def test():
    return "🟢 Bot route is working!"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
