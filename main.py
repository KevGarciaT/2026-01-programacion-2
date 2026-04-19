# Mapeo de precios según la tabla del consultorio
precios = {
    "Particular": {
        "cita": 80000,
        "atenciones": {"Limpieza": 60000, "Calzas": 80000, "Extracción": 100000, "Diagnóstico": 50000}
    },
    "Eps": {
        "cita": 5000,
        "atenciones": {"Limpieza": 0, "Calzas": 40000, "Extracción": 40000, "Diagnóstico": 0}
    },
    "Prepagada": {
        "cita": 30000,
        "atenciones": {"Limpieza": 0, "Calzas": 10000, "Extracción": 10000, "Diagnóstico": 0}
    }
}

clientes = []

while True:
    print("\n--- REGISTRO DE CITA ODONTOLÓGICA ---")
    cedula = input("Cédula (o 'fin' para terminar): ")
    if cedula.lower() == 'fin': break
    
    nombre = input("Nombre: ")
    tipo_cliente = input("Tipo Cliente (Particular, EPS, Prepagada): ").capitalize()
    tipo_atencion = input("Atención (Limpieza, Calzas, Extracción, Diagnóstico): ").capitalize()
    
    if tipo_atencion in ["Limpieza", "Diagnóstico"]:
        cantidad = 1
    else:
        cantidad = int(input("Cantidad: "))
        
    # Cálculos
    v_cita = precios[tipo_cliente]["cita"]
    v_atencion = precios[tipo_cliente]["atenciones"][tipo_atencion]
    total_pagar = v_cita + (v_atencion * cantidad)
    
    # Guardar datos
    clientes.append({
        "cedula": cedula,
        "nombre": nombre,
        "atencion": tipo_atencion,
        "total": total_pagar
    })

# --- REPORTES FINALES ---
if clientes:
    print(f"\nTotal Clientes: {len(clientes)}")
    print(f"Ingresos Totales: ${sum(c['total'] for c in clientes)}")
    
    # Ordenar por valor de mayor a menor
    clientes_ordenados = sorted(clientes, key=lambda x: x['total'], reverse=True)
    
    print("\n--- LISTA DE CLIENTES (MAYOR A MENOR PAGO) ---")
    for c in clientes_ordenados:
        print(f"Nombre: {c['nombre']} - Total: ${c['total']}")