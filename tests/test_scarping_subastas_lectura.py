# test_scraping_subastas_lectura.py
from scraping_subastas_lectura import lectura

def test_lectura_runs_without_error():
    try:
        lectura()
    except Exception as e:
        assert False, f"lectura raised an exception: {e}"