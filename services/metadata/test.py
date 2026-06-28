from db.meta_manager import MetaDatabaseManager

db = MetaDatabaseManager()

result = db.search("bow_ufj234")

print(type(result))
