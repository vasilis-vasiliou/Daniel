from datetime import datetime, timedelta

def break_into_timechunks(base_text, start_date, end_date, chunk_size=10):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    
    queries = []
    current_start = start
    
    while current_start < end:
        current_end = min(current_start + timedelta(days=chunk_size - 1), end)
        query = f"{base_text} until:{current_end.strftime('%Y-%m-%d')} since:{current_start.strftime('%Y-%m-%d')}"
        queries.append(query)
        current_start = current_end + timedelta(days=1)
    
    return queries


