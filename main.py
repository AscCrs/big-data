from config.db import init_db
from config.create_db import create_collections
from seed.data_generator import seed_all

if __name__ == "__main__":
    create_collections()
    init_db()
    seed_all()
