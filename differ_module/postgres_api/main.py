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
        cur.execute("INSERT INTO sources (name, url) VALUES (%s, %s) RETURNING id", (data["name"], data["url"]))
        source_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"id": source_id, "name": data["name"], "url": data["url"]}), 201

@app.route("/sources", methods=["GET"])
def list_sources():
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, url FROM sources")
        rows = cur.fetchall()
        return jsonify([{"id": r[0], "name": r[1], "url": r[2]} for r in rows])

@app.route("/sources/<string:source_name>", methods=["GET"])
def get_source(source_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, url FROM sources WHERE name = %s", (source_name,))
        row = cur.fetchone()
        if row:
            return jsonify({"id": row[0], "name": row[1], "url": row[2]})
        return jsonify({"error": "Nie znaleziono źródła."}), 404

@app.route("/sources/<string:source_name>", methods=["DELETE"])
def delete_source(source_name):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM sources WHERE name = %s RETURNING id", (source_name,))
        result = cur.fetchone()
        conn.commit()
        if result:
            return jsonify({"message": f"Źródło '{source_name}' zostało usunięte."})
        return jsonify({"error": "Nie znaleziono źródła."}), 404

@app.route("/documents/<string:source_name>", methods=["POST"])
def create_document(source_name):
    data = request.get_json()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("SELECT id FROM documents WHERE name = %s AND source_id = %s", (data["name"], src[0]))
        if cur.fetchone():
            return jsonify({"error": "Dokument już istnieje."}), 400
        cur.execute("INSERT INTO documents (name, source_id) VALUES (%s, %s) RETURNING id", (data["name"], src[0]))
        doc_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"id": doc_id, "name": data["name"], "source_id": src[0]}), 201

@app.route("/documents/<string:source_name>", methods=["GET"])
def list_documents(source_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("SELECT id, name FROM documents WHERE source_id = %s", (src[0],))
        docs = cur.fetchall()
        return jsonify([{"id": d[0], "name": d[1], "source_name": source_name} for d in docs])

@app.route("/documents/<string:source_name>/<string:document_name>", methods=["DELETE"])
def delete_document(source_name, document_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("DELETE FROM documents WHERE name = %s AND source_id = %s RETURNING id", (document_name, src[0]))
        result = cur.fetchone()
        conn.commit()
        if result:
            return jsonify({"message": f"Dokument '{document_name}' został usunięty."})
        return jsonify({"error": "Nie znaleziono dokumentu."}), 404

@app.route("/documents/<string:source_name>/<string:document_name>/latest", methods=["GET"])
def get_latest_version(source_name, document_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404

        cur.execute("SELECT id FROM documents WHERE name = %s AND source_id = %s", (document_name, src[0]))
        doc = cur.fetchone()
        if not doc:
            return jsonify({"error": "Nie znaleziono dokumentu."}), 404

        cur.execute("SELECT id, document_id, name, content, date FROM versions WHERE document_id = %s ORDER BY date DESC LIMIT 1",(doc[0],))
        ver = cur.fetchone()
        if not ver:
            return jsonify({"error": "Brak wersji dla tego dokumentu."}), 404

        version_id, document_id, name, content, date = ver
        return jsonify({"id": version_id,"document_id": document_id,"name": name,"content": content,"date": date.isoformat()})

@app.route("/versions/<string:source_name>/<string:document_name>", methods=["POST"])
def create_version(source_name, document_name):
    data = request.get_json()
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("SELECT id FROM documents WHERE name = %s AND source_id = %s", (document_name, src[0]))
        doc = cur.fetchone()
        if not doc:
            return jsonify({"error": "Nie znaleziono dokumentu."}), 404
        cur.execute("SELECT id FROM versions WHERE name = %s AND document_id = %s", (data["name"], doc[0]))
        if cur.fetchone():
            return jsonify({"error": "Wersja już istnieje."}), 400
        cur.execute("INSERT INTO versions (document_id, name, content) VALUES (%s, %s, %s) RETURNING id, date", (doc[0], data["name"], data["content"]))
        version_id, date = cur.fetchone()
        conn.commit()
        return jsonify({"id": version_id, "document_id": doc[0], "name": data["name"], "content": data["content"], "date": date.isoformat()}), 201

@app.route("/versions/<string:source_name>/<string:document_name>", methods=["GET"])
def list_versions(source_name, document_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("SELECT id FROM documents WHERE name = %s AND source_id = %s", (document_name, src[0]))
        doc = cur.fetchone()
        if not doc:
            return jsonify({"error": "Nie znaleziono dokumentu."}), 404
        cur.execute("SELECT id, name, content, date FROM versions WHERE document_id = %s", (doc[0],))
        vers = cur.fetchall()
        return jsonify([{"id": v[0], "document_id": doc[0], "name": v[1], "content": v[2], "date": v[3].isoformat()} for v in vers])

@app.route("/versions/<string:source_name>/<string:document_name>/<string:version_name>", methods=["GET"])
def get_version(source_name, document_name, version_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("SELECT id FROM documents WHERE name = %s AND source_id = %s", (document_name, src[0]))
        doc = cur.fetchone()
        if not doc:
            return jsonify({"error": "Nie znaleziono dokumentu."}), 404
        cur.execute("SELECT id, document_id, name, content, date FROM versions WHERE name = %s AND document_id = %s", (version_name, doc[0]))
        ver = cur.fetchone()
        if ver:
            return jsonify({"id": ver[0], "document_id": ver[1], "name": ver[2], "content": ver[3], "date": ver[4].isoformat()})
        return jsonify({"error": "Nie znaleziono wersji."}), 404

@app.route("/versions/<string:source_name>/<string:document_name>/<string:version_name>", methods=["DELETE"])
def delete_version(source_name, document_name, version_name):
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM sources WHERE name = %s", (source_name,))
        src = cur.fetchone()
        if not src:
            return jsonify({"error": "Nie znaleziono źródła."}), 404
        cur.execute("SELECT id FROM documents WHERE name = %s AND source_id = %s", (document_name, src[0]))
        doc = cur.fetchone()
        if not doc:
            return jsonify({"error": "Nie znaleziono dokumentu."}), 404
        cur.execute("DELETE FROM versions WHERE name = %s AND document_id = %s RETURNING id", (version_name, doc[0]))
        result = cur.fetchone()
        conn.commit()
        if result:
            return jsonify({"message": f"Wersja '{version_name}' została usunięta."})
        return jsonify({"error": "Nie znaleziono wersji."}), 404

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
