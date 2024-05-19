from app import db

conn = db.engine.connect()

conn.execute("DROP TABLE IF EXISTS _alembic_tmp_post;")

conn.close()
