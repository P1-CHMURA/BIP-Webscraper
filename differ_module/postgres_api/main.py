from flask import Flask, request, jsonify
import psycopg2

DB_NAME = "postgres"
DB_USER = "postgres"
DB_PASSWORD = "postgres"
DB_HOST = "differ_postgres"
DB_PORT = "5432"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
app = Flask(__name__)

@app.route("/sources", methods=["POST"])
def create_source():
    data = request.get_json()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (data["name"],))
        if cur.fetchone():
            return jsonify({"error": "Źródło o tej nazwie już istnieje."}), 400
        cur.execute("INSERT INTO sources (name) VALUES (%s) RETURNING id", (data["name"], ))
        source_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"id": source_id, "name": data["name"]}), 201

@app.route("/sources", methods=["GET"])
def list_sources():
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM sources")
        rows = cur.fetchall()
        return jsonify([{"id": r[0], "name": r[1]} for r in rows])

@app.route("/sources/<path:source_name>", methods=["GET"])
def get_source(source_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name FROM sources WHERE name = %s", (source_name, ))
        row = cur.fetchone()
        if row:
            return jsonify({"id": row[0], "name": row[1]})
        return jsonify({"error": "Nie znaleziono źródła."}), 404

@app.route("/sources/<path:source_name>", methods=["DELETE"])
def delete_source(source_name):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM sources WHERE name = %s RETURNING id", (source_name, ))
        result = cur.fetchone()
        conn.commit()
        if result:
            return jsonify({"message": f"Źródło '{source_name}' zostało usunięte."})
        return jsonify({"error": "Nie znaleziono źródła."}), 404

@app.route("/documents/<path:source_name>", methods=["POST"])
def create_document(source_name):
    data = request.get_json()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name, ))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("SELECT id FROM documents WHERE name = %s", (data["name"], ))
        if cur.fetchone():
            return jsonify({"error": "Dokument już istnieje."}), 400
        cur.execute("INSERT INTO documents (name, source_id, typ) VALUES (%s, %s, %s) RETURNING id", (data["name"], src[0], data["typ"]))
        doc_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"id": doc_id, "name": data["name"], "source_id": src[0], "name": data["typ"]}), 201

@app.route("/documents/<path:source_name>", methods=["GET"])
def list_documents(source_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name, ))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("SELECT id, name, typ FROM documents WHERE source_id = %s", (src[0],))
        docs = cur.fetchall()
        return jsonify([{"id": d[0], "name": d[1],"typ": d[2], "source_name": source_name} for d in docs])

@app.route("/documents/<path:document_name>", methods=["DELETE"])
def delete_document(document_name):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM documents WHERE name = %s RETURNING id", (document_name, ))
        result = cur.fetchone()
        conn.commit()
        if result:
            return jsonify({"message": f"Dokument '{document_name}' został usunięty."})
        return jsonify({"error": "Nie znaleziono dokumentu."}), 404

@app.route("/documents/<path:document_name>/latest", methods=["GET"])
def get_latest_version(document_name):
    with conn.cursor() as cur:
        
        cur.execute("SELECT id FROM documents WHERE name = %s", (document_name, ))
        doc = cur.fetchone()
        if not doc:
            return jsonify({"error": "Nie znaleziono dokumentu."}), 404

        cur.execute("SELECT id, document_id, content, date FROM versions WHERE document_id = %s ORDER BY date DESC LIMIT 1",(doc[0], ))
        ver = cur.fetchone()
        if not ver:
            return jsonify({"error": "Brak wersji dla tego dokumentu."}), 404

        version_id, document_id, content, date = ver
        return jsonify({"id": version_id,"document_id": document_id, "document_name": document_name, "content": content,"date": date.isoformat()})

@app.route("/versions/<path:document_name>", methods=["POST"])
def create_version(document_name):
    data = request.get_json()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM documents WHERE name = %s", (document_name, ))
        doc = cur.fetchone()
        if not doc:
            return jsonify({"error": "Nie znaleziono dokumentu."}), 404
        cur.execute("INSERT INTO versions (document_id, content) VALUES (%s, %s) RETURNING id, date", (doc[0], data["content"]))
        version_id, date = cur.fetchone()
        conn.commit()
        return jsonify({"id": version_id, "document_id": doc[0], "document_name": document_name, "content": data["content"], "date": date.isoformat()}), 201

@app.route("/versions/<path:document_name>", methods=["GET"])
def list_versions(document_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM documents WHERE name = %s", (document_name, ))
        doc = cur.fetchone()
        if not doc:
            return jsonify({"error": "Nie znaleziono dokumentu."}), 404
        cur.execute("SELECT id, content, date FROM versions WHERE document_id = %s", (doc[0], ))
        vers = cur.fetchall()
        return jsonify([{"id": v[0], "document_id": doc[0], "document_name": document_name, "content": v[1], "date": v[2].isoformat()} for v in vers])

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
