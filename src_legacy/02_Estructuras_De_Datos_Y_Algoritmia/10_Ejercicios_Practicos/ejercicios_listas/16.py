def filtro_logs(logs):
    lista_filtrada = [i for i in logs if 'ERROR' in i]
    return lista_filtrada

logs = [
    "2025-12-27 INFO: Usuario login OK",
    "2025-12-27 ERROR: DB connection failed",
    "2025-12-27 WARNING: Disk 90% full", 
    "2025-12-27 ERROR: File not found",
    "2025-12-27 INFO: Backup completed"
]

print("Logs originales:", len(logs))
errores = filtro_logs(logs)
print("Solo ERRORs:", errores)
print("Cantidad:", len(errores))