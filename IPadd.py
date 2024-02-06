import cv2
from PIL import Image
import subprocess
import sys
import time
import whois

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

    def get_vpn_ip_address(self):
        try:
            result = subprocess.check_output("ipconfig" if "win" in sys.platform else "ifconfig", shell=True, text=True)
            # Extract the first IPv4 address found in the result
            ip_address = result.split("IPv4 Address")[1].split(":")[1].strip().split()[0]
            return ip_address
        except (subprocess.CalledProcessError, IndexError, AttributeError):
            return None

    def get_whois_info(self, ip_address):
        try:
            w = whois.whois(ip_address)
            return w
        except whois.parser.PywhoisError:
            return None

    def initiate_payment(self):
        if self.is_vpn_active():
            print("VPN is active. Payment cannot be processed.")
            vpn_ip_address = self.get_vpn_ip_address()
            if vpn_ip_address:
                print(f"Detected VPN IP Address: {vpn_ip_address}")
                #whois_info = self.get_whois_info(vpn_ip_address)
                #if whois_info:
                    #print("WHOIS Information:")
                    #print(whois_info)
            else:
                print("WHOIS information not available for the detected IP address.")
            return

        print(f"Initiating UPI payment from {self.sender_name} to {self.receiver_name}...")

        # Simulating payment process
        time.sleep(2)  # Simulate processing time

        print(f"Payment of {self.amount} initiated successfully.")
        print("Waiting for confirmation...")

        # Simulate confirmation
        time.sleep(2)
        print("Payment confirmed!")

    def display_payment_details(self):
        print("\nPayment Details:")
        print(f"Sender: {self.sender_name} ({self.sender_upi_id})")
        print(f"Receiver: {self.receiver_name} ({self.receiver_upi_id})")
        print(f"Amount: {self.amount}")

    def capture_screenshot(self):
        # Open the front camera (usually index 0 for the default camera)
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Error: Could not open camera.")
            return

        # Read a frame from the camera
        ret, frame = cap.read()

        if not ret:
            print("Error: Could not read frame.")
            cap.release()
            return

        # Save the frame as a screenshot
        cv2.imwrite("payment_snapshot.png", frame)

        # Release the camera
        cap.release()
        print("Payment snapshot captured successfully.")

    def display_payment_snapshot(self):
        # Open the saved screenshot using Pillow
        image = Image.open("payment_snapshot.png")
        image.show()

if __name__ == "__main__":
    # Take input from the user
    sender_name = input("Enter sender's name: ")
    sender_upi_id = input("Enter sender's UPI ID: ")
    receiver_name = input("Enter receiver's name: ")
    receiver_upi_id = input("Enter receiver's UPI ID: ")
    amount = float(input("Enter the payment amount: "))

    # Create a dummy payment object
    dummy_payment = DummyUpiPayment(sender_name, sender_upi_id, receiver_name, receiver_upi_id, amount)

    # Display payment details
    dummy_payment.display_payment_details()

    # Initiate the dummy payment
    dummy_payment.initiate_payment()

    # Capture and display payment snapshot
    dummy_payment.capture_screenshot()
    dummy_payment.display_payment_snapshot()
