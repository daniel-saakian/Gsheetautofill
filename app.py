import json
from flask import Flask, request, jsonify
from pull_demographics import profile_address   # your existing script
 
app = Flask(__name__)
 
 
@app.route("/profile")
def profile():
    address = request.args.get("address", "").strip()
    if not address:
        return jsonify({"error": "Missing 'address' query parameter"}), 400
 
    try:
        result = profile_address(address)
        return jsonify(result)
    except ValueError as e:
        # geocoding failure, bad address, etc.
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": f"Internal error: {e}"}), 500
 
 
@app.route("/health")
def health():
    return jsonify({"status": "ok"})
 
 
if __name__ == "__main__":
    # Use PORT env var for Cloud Run compatibility
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)