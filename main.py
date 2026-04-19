"""
Project: Dental Clinic Management System
Version: 1.0
Author: KevGarciaT
Description: Calculates appointment costs based on client type and service,
             stores records, and generates sorted reports.
"""

# Price mapping dictionary: Using a nested structure for O(1) lookup efficiency
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

# In-memory array to store client records (Acting as a temporary database)
clients = []

while True:
    print("\n--- DENTAL CLINIC REGISTRATION SYSTEM ---")
    
    # Primary Key equivalent: ID Card
    id_card = input("ID Card Number (or type 'exit' to finish): ")
    if id_card.lower() == 'exit': 
        break
    
    name = input("Client Name: ")
    
    # .capitalize() ensures input matches dictionary keys regardless of user casing
    client_type = input("Client Type (Particular, Eps, Prepaid): ").capitalize()
    service_type = input("Service (Cleaning, Fillings, Extraction, Diagnosis): ").capitalize()
    
    # Logical constraint: Cleaning and Diagnosis are always single-unit services
    if service_type in ["Cleaning", "Diagnosis"]:
        quantity = 1
    else:
        # Cast input to integer for mathematical operations
        quantity = int(input("Quantity of teeth/fillings: "))
        
    # Data Retrieval: Accessing the nested price dictionary
    app_fee = prices[client_type]["appointment_fee"]
    service_fee = prices[client_type]["services"][service_type]
    
    # Business Logic: Total = Base Fee + (Unit Price * Quantity)
    total_to_pay = app_fee + (service_fee * quantity)
    
    # Data persistence: Appending a dictionary object to our list
    clients.append({
        "id": id_card,
        "name": name,
        "service": service_type,
        "total": total_to_pay
    })

# --- DATA ANALYSIS AND REPORTING ---
if clients:
    # Aggregation: Calculating total revenue across all records
    total_revenue = sum(c['total'] for c in clients)
    
    # Filtering: Counting specific service occurrences (Extractions)
    extractions_count = len([c for c in clients if c['service'] == "Extraction"])
    
    print(f"\nTotal Clients processed: {len(clients)}")
    print(f"Total Revenue collected: ${total_revenue}")
    print(f"Total Extractions performed: {extractions_count}")
    
    # Sorting: Ordering the list by 'total' value using a lambda function (Descending)
    sorted_clients = sorted(clients, key=lambda x: x['total'], reverse=True)
    
    print("\n--- REVENUE REPORT (SORTED HIGHEST TO LOWEST) ---")
    for c in sorted_clients:
        print(f"Name: {c['name']} | ID: {c['id']} | Total Paid: ${c['total']}")