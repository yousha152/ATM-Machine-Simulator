#  Interactive ATM Machine System (Python & Web UI)

A comprehensive,  ATM Machine application built using **Python** (Backend Logic) and **HTML5, CSS3, JavaScript** (Modern Web Interface). The system simulates real-world banking operations, including authentication, transaction limits, transfer verification, and administrative monitoring.

---

##  Features

* ** Secure PIN Authentication:** 
  * 4-digit PIN verification.
  * Maximum 3 attempts limit with auto-account locking mechanism.
* ** Banking Operations:**
  * **Check Balance:** View current account funds anytime.
  * **Deposit Money:** Add funds with strict validation (rejects zero/negative values).
  * **Withdraw Money:** Cash withdrawal with daily limit enforcement.
  * **Transfer Money:** Fund transfers with valid recipient verification (`987654321`).
  * **Change PIN:** Secure PIN modification with old PIN verification and confirmation matching.
  * **Mini Statement:** View recent transaction history formatted with dates and signs.
* ** Security & Validations:**
  * Prevents overdrawing (insufficient balance protection).
  * Daily withdrawal limit cap (`Rs. 25,000`).
  * Input sanitization to prevent program crashes on unexpected inputs.
* ** Admin Mode:**
  * Access via Master PIN (`9999`) to view total logs, user balance, and active PIN.

---

##  Project Structure


* **`main.py`** - Python Console Version (CLI ATM)
* **`index.html`** - Web UI Structure
* **`style.css`** - Modern Dark-themed Responsive Styling
* **`script.js`** - Web ATM Logic & Interactivity
* **`README.md`** - Project Documentation