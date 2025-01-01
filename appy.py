from flask import Flask, request, redirect
import paypalrestsdk
import logging

app = Flask(__name__)

# Configure PayPal SDK (use live credentials for production)
paypalrestsdk.configure({
    "mode": "live",  # Switch to live mode for production
    "client_id": "YOUR_LIVE_CLIENT_ID",  # Replace with your live PayPal client ID
    "client_secret": "YOUR_LIVE_CLIENT_SECRET"  # Replace with your live PayPal secret
})

# Set up logging for error tracking
logging.basicConfig(level=logging.INFO)

@app.route('/payment/execute', methods=['GET'])
def payment_execute():
    payment_id = request.args.get('paymentId')  # PayPal sends the payment ID
    payer_id = request.args.get('PayerID')  # PayPal sends the payer ID

    if payment_id and payer_id:
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({"payer_id": payer_id}):
                logging.info(f"Payment executed successfully. Transaction ID: {payment.transactions[0].related_resources[0].sale.id}")
                return redirect("https://your-live-domain.com/success")  # Redirect to success page
            else:
                logging.error(f"Payment execution failed: {payment.error}")
                return redirect("https://your-live-domain.com/failure")  # Redirect to failure page
        except Exception as e:
            logging.error(f"Error during payment execution: {e}")
            return redirect("https://your-live-domain.com/failure")
    
    return redirect("https://your-live-domain.com/cancel")  # Redirect to cancel page

@app.route('/payment/cancel', methods=['GET'])
def payment_cancel():
    return "Payment cancelled. Please try again later."

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=3000)  # Use a production WSGI server like Gunicorn