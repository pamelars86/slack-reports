from datetime import datetime, timedelta

def split_date_range(start_date, end_date):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    chunks = []

    while start < end:
        # Si la fecha de fin está en el mismo mes que el inicio, no avanzamos al siguiente mes
        if start.month == end.month and start.year == end.year:
            chunks.append((start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")))
            break

        # Establecer el final del mes (primer día del siguiente mes)
        month_end = (start.replace(day=28) + timedelta(days=4)).replace(day=1)
        
        # Si el final del mes es mayor que la fecha final, tomamos el valor de end_date
        if month_end > end:
            month_end = end

        # Añadir el rango de fechas para el chunk
        chunks.append((start.strftime("%Y-%m-%d"), month_end.strftime("%Y-%m-%d")))
        
        # Avanzar al siguiente mes
        start = month_end

    return chunks