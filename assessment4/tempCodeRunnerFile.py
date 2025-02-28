@app.route('/v1/gpay/deleteById/<custId>', methods=['DELETE'])
def delete_by_id(custId):
    try:
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM Bank WHERE custId = '{custId}'")
        conn.commit()
        return jsonify({"message": f"Customer {custId} deleted successfully"}), 200
    except Exception as e:
        raise ValidationError(str(e))