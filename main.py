from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re

app = Flask(__name__)
AFF_LINK = "https://fktr.in/m96JCkl"

def extract_product_name(url):
    m = re.search(r"flipkart\.com/([^/]+)-p/", url)
    return m.group(1).replace('-', ' ') if m else "Product"

@app.route("/bot", methods=["POST"])
def bot():
    txt = request.values.get('Body','').strip()
    resp = MessagingResponse()
    msg = resp.message()
    if "flipkart.com" in txt:
        name = extract_product_name(txt)
        msg.body(f"🛍️ Product: {name}\n🔗 Link: {AFF_LINK}")
    else:
        msg.body("❌ Kripya Flipkart ka valid link bhejiye.")
    return str(resp)

if __name__ == "__main__":
    app.run()
