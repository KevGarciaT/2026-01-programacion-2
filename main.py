"""
Project: Robust Dental Clinic Management System
Version: 2.0 (Security Hardened)
Author: KevGarciaT
"""

# Price mapping dictionary
prices = {
    "Particular": {
        "appointment_fee": 80000,
        "services": {"Cleaning": 60000, "Fillings": 80000, "Extraction": 100000, "Diagnosis": 50000}
    },
    "Eps": {
        "appointment_fee": 5000,
        "services": {"Cleaning": 0, "Fillings": 40000, "Extraction": 40000, "Diagnosis": 0}
    },
    "Prepaid": {
        "appointment_fee": 30000,
        "services": {"Cleaning": 0, "Fillings": 10000, "Extraction": 10000, "Diagnosis": 0}
    }
}

clients = []

def get_non_empty_string(prompt):
    """Guarantees the user provides a string that is not just whitespace."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("ERROR: Field cannot be empty. Please provide a valid entry.")

def get_valid_choice(prompt, options):
    """Forces the user to pick from a specific list of valid categories."""
    while True:
        value = input(prompt).strip().capitalize()
        if value in options:
            return value
        print(f"ERROR: Invalid choice. Please select from: {', '.join(options)}")

def get_positive_int(prompt):
    """Forces the user to enter a numeric value greater than zero."""
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("ERROR: Quantity must be greater than zero.")
        except ValueError:
            print("ERROR: Invalid input. Please enter a numeric integer.")

# --- MAIN LOOP ---
while True:
    print("\n--- SECURE DENTAL REGISTRATION SYSTEM ---")
    
    # 1. ID Validation (Can't be empty)
    id_card = get_non_empty_string("ID Card Number (or type 'exit' to finish): ")
    if id_card.lower() == 'exit': 
        break
    
    # 2. Name Validation (Can't be empty)
    name = get_non_empty_string("Client Name: ")
    
    # 3. Type Validation (Must be in our dictionary)
    client_type = get_valid_choice("Client Type (Particular, Eps, Prepaid): ", list(prices.keys()))
    
    # 4. Service Validation (Must be in our list of services)
    available_services = list(prices[client_type]["services"].keys())
    service_type = get_valid_choice("Service (Cleaning, Fillings, Extraction, Diagnosis): ", available_services)
    
    # 5. Quantity Validation
    if service_type in ["Cleaning", "Diagnosis"]:
        quantity = 1
    else:
        quantity = get_positive_int(f"Enter quantity for {service_type}: ")
        
    # Calculation
    app_fee = prices[client_type]["appointment_fee"]
    service_fee = prices[client_type]["services"][service_type]
    total_to_pay = app_fee + (service_fee * quantity)
    
    clients.append({
        "id": id_card,
        "name": name,
        "service": service_type,
        "total": total_to_pay
    })
    print(f"SUCCESS: Record added for {name}. Total to pay: ${total_to_pay}")

# --- REPORTING ---
if clients:
    print(f"\nProcessing complete. Total Records: {len(clients)}")
    sorted_clients = sorted(clients, key=lambda x: x['total'], reverse=True)
    for c in sorted_clients:
        print(f"ID: {c['id']} | Name: {c['name']} | Total: ${c['total']}")