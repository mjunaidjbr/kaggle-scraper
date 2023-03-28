from database_initialize import Base, engine, Record 
Base.metadata.create_all(engine)