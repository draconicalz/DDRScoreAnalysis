from src.database import initializeDatabase, loadJsonToDatabase

def main():
    initializeDatabase()
    loadJsonToDatabase()

if __name__ == "__main__":
    main()