from flask import Flask, render_template, request
import cv2
from PIL import Image
import subprocess
import sys
import time

app = Flask(__name__)

class DummyUpiPayment:
    def __init__(self, sender_name, sender_upi_id, receiver_name, receiver_upi_id, amount):
        self.sender_name = sender_name
        self.sender_upi_id = sender_upi_id
        self.receiver_name = receiver_name
        self.receiver_upi_id = receiver_upi_id
        self.amount = amount

    def is_vpn_active(self):
        try:
            result = subprocess.check_output("ipconfig" if "win" in sys.platform else "ifconfig", shell=True, text=True)
            if "VPN" in result or ("tun" in result and "tap" in result):
                return True
        except subprocess.CalledProcessError:
            pass
        return False

    def initiate_payment(self):
        if self.is_vpn_active():
            return "VPN is active. Payment cannot be processed."

        return f"Payment of {self.amount} initiated successfully."

    def display_payment_details(self):
        return f"Sender: {self.sender_name} ({self.sender_upi_id})\nReceiver: {self.receiver_name} ({self.receiver_upi_id})\nAmount: {self.amount}"

    def capture_screenshot(self):
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            return "Error: Could not open camera."

        ret, frame = cap.read()

        if not ret:
            cap.release()
            return "Error: Could not read frame."

        cv2.imwrite("payment_snapshot.png", frame)
        cap.release()
        return "Payment snapshot captured successfully."

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/process_payment', methods=['POST'])
def process_payment():
    sender_name = request.form['sender_name']
    sender_upi_id = request.form['sender_upi_id']
    receiver_name = request.form['receiver_name']
    receiver_upi_id = request.form['receiver_upi_id']
    amount = float(request.form['amount'])

    dummy_payment = DummyUpiPayment(sender_name, sender_upi_id, receiver_name, receiver_upi_id, amount)

    payment_result = dummy_payment.initiate_payment()
    details_result = dummy_payment.display_payment_details()
    snapshot_result = dummy_payment.capture_screenshot()

    return render_template('result1.html', payment_result=payment_result, details_result=details_result, snapshot_result=snapshot_result)

from flask import Flask, render_template, request
import cv2
from PIL import Image
import subprocess
import sys
import time

app = Flask(__name__)

# ... (rest of the code remains the same)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Change the port number if needed

