// System Data
let userPin = "1234";
let accountBalance = 50000.0;
let transactionHistory = [];
let attempts = 3;

const validRecipient = "987654321";
const maxDailyWithdraw = 25000.0;
let withdrawnToday = 0.0;
let currentMode = "login";

const adminCode = "9999";

function updateOutput(text, isError = false) {
    const output = document.getElementById("output");
    output.innerText = text;
    output.style.color = isError ? "#fca5a5" : "#fef08a";
}

function verifyPin() {
    const inputField = document.getElementById("atm-input");
    const enteredPin = inputField.value.trim();

    // Admin Access Check
    if (enteredPin === adminCode) {
        showAdminPanel();
        inputField.value = "";
        return;
    }

    if (enteredPin.length !== 4 || isNaN(enteredPin)) {
        updateOutput("Invalid PIN! Enter exactly 4 numbers.", true);
        return;
    }

    if (enteredPin === userPin) {
        document.getElementById("screen-title").innerText = "MAIN MENU";
        document.getElementById("screen-desc").innerText = "Select an operation below:";
        inputField.classList.add("hidden");
        document.getElementById("action-btn").classList.add("hidden");
        document.getElementById("login-controls").classList.add("hidden");
        document.getElementById("menu-buttons").classList.remove("hidden");
        updateOutput("Login successful! Welcome.");
        inputField.value = "";
    } else {
        attempts--;
        if (attempts > 0) {
            updateOutput(`Incorrect PIN! ${attempts} attempt(s) remaining.`, true);
        } else {
            updateOutput("Maximum attempts reached. Account locked.", true);
            document.getElementById("login-controls").classList.add("hidden");
            inputField.disabled = true;
        }
    }
}

function showAdminPanel() {
    document.getElementById("screen-title").innerText = "ADMIN CONTROL PANEL";
    document.getElementById("screen-desc").innerText = "System Details & Logs:";
    document.getElementById("atm-input").classList.add("hidden");
    document.getElementById("action-btn").classList.add("hidden");
    document.getElementById("login-controls").classList.add("hidden");
    document.getElementById("menu-buttons").classList.remove("hidden");

    let logText = `User Balance: Rs. ${accountBalance.toLocaleString()}\nUser PIN: ${userPin}\nTotal Txns: ${transactionHistory.length}`;
    
    if (transactionHistory.length > 0) {
        logText += "\n\nRecent System Activity:\n";
        let recent = transactionHistory.slice(-3);
        recent.forEach((t, i) => {
            logText += `${i+1}. ${t.type} - Rs. ${t.amount.toLocaleString()}\n`;
        });
    }

    updateOutput(logText);
}

function showCheckBalance() {
    hideInputControls();
    updateOutput(`Available Balance: Rs. ${accountBalance.toLocaleString()}`);
}

function setupDeposit() {
    showInputControls("Enter deposit amount (Rs.):", "deposit", "e.g. 5000");
}

function setupWithdraw() {
    showInputControls("Enter withdrawal amount (Rs.):", "withdraw", "e.g. 2000");
}

function setupTransfer() {
    showInputControls("Enter Recipient Account Number:", "transfer_acc", "Account Number");
}

function setupChangePin() {
    showInputControls("Enter Current PIN:", "pin_current", "Current PIN");
}

function showInputControls(descText, mode, placeholder = "") {
    currentMode = mode;
    document.getElementById("screen-desc").innerText = descText;
    const input = document.getElementById("atm-input");
    input.classList.remove("hidden");
    input.type = mode.includes("pin") ? "password" : "text";
    input.placeholder = placeholder;
    input.value = "";
    document.getElementById("action-btn").classList.remove("hidden");
    updateOutput("");
}

function hideInputControls() {
    document.getElementById("atm-input").classList.add("hidden");
    document.getElementById("action-btn").classList.add("hidden");
    document.getElementById("screen-desc").innerText = "Select an operation below:";
}

function handleAction() {
    const inputVal = document.getElementById("atm-input").value.trim();
    
    if (currentMode === "deposit") {
        let amount = parseFloat(inputVal);
        if (isNaN(amount) || amount <= 0) {
            updateOutput("Deposit amount must be greater than zero.", true);
            return;
        }
        accountBalance += amount;
        transactionHistory.push({ type: "Deposit", amount: amount, sign: "+" });
        updateOutput(`Rs. ${amount.toLocaleString()} deposited.\nNew Balance: Rs. ${accountBalance.toLocaleString()}`);
        hideInputControls();

    } else if (currentMode === "withdraw") {
        let amount = parseFloat(inputVal);
        if (isNaN(amount) || amount <= 0) {
            updateOutput("Withdrawal amount must be greater than zero.", true);
            return;
        }
        if (withdrawnToday + amount > maxDailyWithdraw) {
            let left = maxDailyWithdraw - withdrawnToday;
            updateOutput(`Daily limit exceeded! Remaining limit: Rs. ${left.toLocaleString()}`, true);
            return;
        }
        if (amount > accountBalance) {
            updateOutput("Transaction failed! Insufficient balance.", true);
            return;
        }
        accountBalance -= amount;
        withdrawnToday += amount;
        transactionHistory.push({ type: "Withdrawal", amount: amount, sign: "-" });
        updateOutput(`Rs. ${amount.toLocaleString()} withdrawn.\nRemaining: Rs. ${accountBalance.toLocaleString()}`);
        hideInputControls();

    } else if (currentMode === "transfer_acc") {
        if (inputVal !== validRecipient) {
            updateOutput("Invalid recipient account number!", true);
            return;
        }
        showInputControls("Enter Transfer Amount (Rs.):", "transfer_amount", "e.g. 1000");

    } else if (currentMode === "transfer_amount") {
        let amount = parseFloat(inputVal);
        if (isNaN(amount) || amount <= 0) {
            updateOutput("Transfer amount must be greater than zero.", true);
            return;
        }
        if (amount > accountBalance) {
            updateOutput("Transfer failed! Insufficient balance.", true);
            return;
        }
        accountBalance -= amount;
        transactionHistory.push({ type: "Transfer", amount: amount, sign: "-" });
        updateOutput(`Rs. ${amount.toLocaleString()} transferred successfully.`);
        hideInputControls();

    } else if (currentMode === "pin_current") {
        if (inputVal !== userPin) {
            updateOutput("Incorrect current PIN.", true);
            return;
        }
        showInputControls("Enter New 4-digit PIN:", "pin_new", "New PIN");

    } else if (currentMode === "pin_new") {
        if (inputVal.length !== 4 || isNaN(inputVal)) {
            updateOutput("New PIN must contain exactly 4 digits.", true);
            return;
        }
        userPin = inputVal;
        updateOutput("Your PIN has been changed successfully.");
        hideInputControls();
    }
}

function miniStatement() {
    hideInputControls();
    if (transactionHistory.length === 0) {
        updateOutput("No transactions available.");
        return;
    }

    let text = "MINI STATEMENT:\n";
    let recent = transactionHistory.slice(-4);
    recent.forEach(t => {
        text += `${t.type}: ${t.sign}Rs. ${t.amount.toLocaleString()}\n`;
    });
    updateOutput(text);
}

function logout() {
    document.getElementById("screen-title").innerText = "NATIONAL BANK ATM";
    document.getElementById("screen-desc").innerText = "Enter your 4-digit PIN to continue:";
    const input = document.getElementById("atm-input");
    input.type = "password";
    input.placeholder = "Enter PIN";
    input.classList.remove("hidden");
    document.getElementById("action-btn").classList.add("hidden");
    document.getElementById("login-controls").classList.remove("hidden");
    document.getElementById("menu-buttons").classList.add("hidden");
    attempts = 3;
    updateOutput("Logged out successfully.");
}

function exitATM() {
    logout();
    updateOutput("Thank you for using our ATM.");
}