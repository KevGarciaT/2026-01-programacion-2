# Price mapping based on the dental clinic's business rules
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

while True:
    print("\n--- DENTAL CLINIC REGISTRATION SYSTEM ---")
    id_card = input("ID Card Number (or type 'exit' to finish): ")
    if id_card.lower() == 'exit': 
        break
    
    name = input("Client Name: ")
    client_type = input("Client Type (Particular, Eps, Prepaid): ").capitalize()
    service_type = input("Service (Cleaning, Fillings, Extraction, Diagnosis): ").capitalize()
    
    # Validation for quantity according to rules
    if service_type in ["Cleaning", "Diagnosis"]:
        quantity = 1
    else:
        quantity = int(input("Quantity of teeth/fillings: "))
        
    # Financial calculations
    app_fee = prices[client_type]["appointment_fee"]
    service_fee = prices[client_type]["services"][service_type]
    total_to_pay = app_fee + (service_fee * quantity)
    
    # Storing data in a list of dictionaries
    clients.append({
        "id": id_card,
        "name": name,
        "service": service_type,
        "total": total_to_pay
    })

# --- FINAL REPORTS ---
if clients:
    total_revenue = sum(c['total'] for c in clients)
    extractions_count = len([c for c in clients if c['service'] == "Extraction"])
    
    print(f"\nTotal Clients: {len(clients)}")
    print(f"Total Revenue: ${total_revenue}")
    print(f"Number of Extraction services: {extractions_count}")
    
    # Sorting by total value paid (Highest to Lowest)
    sorted_clients = sorted(clients, key=lambda x: x['total'], reverse=True)
    
    print("\n--- CLIENT LIST (SORTED BY HIGHEST REVENUE) ---")
    for c in sorted_clients:
        print(f"Name: {c['name']} | ID: {c['id']} | Total: ${c['total']}")