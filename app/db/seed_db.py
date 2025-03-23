from sqlalchemy.orm import Session
from .database import SessionLocal
from .seeds import seed_all

def main():
    db = SessionLocal()
    try:
        print("Iniciando seed...")
        seed_all(db)
        print("Seed finalizado")
    except Exception as e:         
        print(f"Erro ao executar seed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    main()        
