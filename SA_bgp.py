# Script para determinar si un número de AS de BGP es público o privado

as_number = int(input("Ingrese el número de AS de BGP: "))

if (64512 <= as_number <= 65534) or (4200000000 <= as_number <= 4294967294):
    print(f"AS {as_number}: Es un AS privado.")
elif 1 <= as_number <= 4294967295:
    print(f"AS {as_number}: Es un AS público.")
else:
    print("Número de AS no válido.")
