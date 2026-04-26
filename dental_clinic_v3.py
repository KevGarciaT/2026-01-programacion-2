"""
Project: Robust Dental Clinic Management System
Version: 3.0 - Stack & Queue Extension
Author: KevGarciaT

New in v3.0:
  - Stack (Pila): Urgent extraction patients, ordered nearest date → top
  - Queue (Cola): Daily attendance agenda, strict FIFO order
"""

from datetime import datetime, date

# ─────────────────────────────────────────────
#  PRICE TABLE
# ─────────────────────────────────────────────
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

# ─────────────────────────────────────────────
#  DATA STRUCTURES
# ─────────────────────────────────────────────

class Stack:
    """
    LIFO Stack — used for urgent extraction patients.
    Top of the stack = nearest appointment date (served first).
    Internal list: index 0 = bottom, index -1 = top.
    """
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Stack is empty.")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def to_list_top_first(self):
        """Returns a list from top (nearest date) to bottom (farthest)."""
        return list(reversed(self._data))


class Queue:
    """
    FIFO Queue — used for the daily attendance agenda.
    Front = next to be served (index 0).
    """
    def __init__(self):
        self._data = []

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Queue is empty.")
        return self._data.pop(0)

    def front(self):
        if self.is_empty():
            raise IndexError("Queue is empty.")
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def to_list(self):
        return list(self._data)


# ─────────────────────────────────────────────
#  INPUT HELPERS
# ─────────────────────────────────────────────

def get_non_empty_string(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("ERROR: Field cannot be empty.")

def get_valid_choice(prompt, options):
    while True:
        value = input(prompt).strip().capitalize()
        if value in options:
            return value
        print(f"ERROR: Choose from: {', '.join(options)}")

def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value > 0:
                return value
            print("ERROR: Must be greater than zero.")
        except ValueError:
            print("ERROR: Enter a numeric integer.")

def get_valid_date(prompt):
    """Accepts DD/MM/YYYY and rejects past dates."""
    while True:
        raw = input(prompt).strip()
        try:
            dt = datetime.strptime(raw, "%d/%m/%Y").date()
            if dt < date.today():
                print("ERROR: Date cannot be in the past.")
                continue
            return dt
        except ValueError:
            print("ERROR: Use format DD/MM/YYYY.")

def get_priority(prompt):
    options = ["Urgente", "Normal"]
    while True:
        value = input(prompt).strip().capitalize()
        if value in options:
            return value
        print(f"ERROR: Choose from: {', '.join(options)}")


# ─────────────────────────────────────────────
#  REGISTRATION
# ─────────────────────────────────────────────

def register_clients():
    """Collects patient records. Returns a flat list of client dicts."""
    clients = []
    print("\n" + "="*50)
    print("   DENTAL CLINIC — PATIENT REGISTRATION")
    print("="*50)

    while True:
        id_card = get_non_empty_string("\nID Card (or 'exit' to finish): ")
        if id_card.lower() == "exit":
            break

        name          = get_non_empty_string("Full Name: ")
        client_type   = get_valid_choice("Type (Particular, Eps, Prepaid): ", list(prices.keys()))
        available_svc = list(prices[client_type]["services"].keys())
        service_type  = get_valid_choice(
            f"Service ({', '.join(available_svc)}): ", available_svc
        )

        if service_type in ["Cleaning", "Diagnosis"]:
            quantity = 1
        else:
            quantity = get_positive_int(f"Quantity for {service_type}: ")

        appointment_date = get_valid_date("Appointment Date (DD/MM/YYYY): ")
        priority         = get_priority("Priority (Urgente, Normal): ")

        app_fee     = prices[client_type]["appointment_fee"]
        service_fee = prices[client_type]["services"][service_type]
        total       = app_fee + (service_fee * quantity)

        clients.append({
            "id":       id_card,
            "name":     name,
            "type":     client_type,
            "service":  service_type,
            "quantity": quantity,
            "date":     appointment_date,
            "priority": priority,
            "total":    total
        })
        print(f"  ✔ Record saved for {name}. Total: ${total:,}")

    return clients


# ─────────────────────────────────────────────
#  STACK — BUILD & REPORT
# ─────────────────────────────────────────────

def build_urgent_extraction_stack(clients):
    """
    Filters for Extraction + Urgente, sorts farthest→nearest,
    pushes onto stack so nearest date ends up on top.
    """
    filtered = [
        c for c in clients
        if c["service"] == "Extraction" and c["priority"] == "Urgente"
    ]

    # Sort farthest first so the last push (nearest) lands on top
    filtered.sort(key=lambda c: c["date"], reverse=True)

    stack = Stack()
    for client in filtered:
        stack.push(client)

    return stack


def print_stack_report(stack):
    print("\n" + "="*50)
    print("   URGENT EXTRACTION STACK — CALL ORDER")
    print("   (Top = nearest date, served FIRST)")
    print("="*50)

    if stack.is_empty():
        print("  No urgent extraction patients found.")
        return

    patients = stack.to_list_top_first()
    for position, c in enumerate(patients, start=1):
        print(
            f"  [{position}] {c['date'].strftime('%d/%m/%Y')} | "
            f"ID: {c['id']} | {c['name']} | "
            f"Type: {c['type']} | Total: ${c['total']:,}"
        )
    print(f"\n  Total urgent extractions pending: {stack.size()}")


# ─────────────────────────────────────────────
#  QUEUE — BUILD & ATTEND
# ─────────────────────────────────────────────

def build_daily_queue(clients, target_date):
    """
    Builds a FIFO queue for the given date, sorted by registration order
    (which reflects the agenda order for that day).
    """
    daily = [c for c in clients if c["date"] == target_date]
    # Preserve insertion order = agenda order
    queue = Queue()
    for c in daily:
        queue.enqueue(c)
    return queue


def print_queue_report(queue, target_date):
    date_str = target_date.strftime("%d/%m/%Y")
    print("\n" + "="*50)
    print(f"   DAILY QUEUE — {date_str}")
    print("   (Front = next to be attended)")
    print("="*50)

    if queue.is_empty():
        print(f"  No patients scheduled for {date_str}.")
        return

    patients = queue.to_list()
    for position, c in enumerate(patients, start=1):
        print(
            f"  [{position}] ID: {c['id']} | {c['name']} | "
            f"Service: {c['service']} | Priority: {c['priority']} | "
            f"Total: ${c['total']:,}"
        )
    print(f"\n  Patients in queue: {queue.size()}")


def attend_queue(queue):
    """Simulates serving patients one by one from the front of the queue."""
    print("\n--- BEGIN ATTENDANCE ---")
    order = 1
    while not queue.is_empty():
        patient = queue.dequeue()
        print(
            f"  Attending [{order}]: {patient['name']} "
            f"(ID: {patient['id']}) — {patient['service']} "
            f"[{patient['priority']}]"
        )
        order += 1
    print("  ✔ All patients for today have been attended.")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

def main():
    # 1. Registration
    clients = register_clients()

    if not clients:
        print("\nNo patients registered. Exiting.")
        return

    # 2. Stack — Urgent extractions
    urgent_stack = build_urgent_extraction_stack(clients)
    print_stack_report(urgent_stack)

    # 3. Queue — Daily agenda
    print("\n--- DAILY QUEUE SETUP ---")
    date_input = get_valid_date("Enter the date to generate the daily queue (DD/MM/YYYY): ")
    daily_queue = build_daily_queue(clients, date_input)
    print_queue_report(daily_queue, date_input)

    # 4. Simulate attendance
    if not daily_queue.is_empty():
        confirm = input("\nStart attending patients in queue? (yes/no): ").strip().lower()
        if confirm == "yes":
            # Rebuild queue — print_queue_report drained nothing, but attend_queue does
            daily_queue = build_daily_queue(clients, date_input)
            attend_queue(daily_queue)

    print("\n=== SESSION COMPLETE ===\n")


if __name__ == "__main__":
    main()
