rm social.db
sqlite3 social.db < social_schema.sql
sqlite3 social.db < starting-data.sql

python3 my_db.py