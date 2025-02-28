from flask import Flask  
from flask_restful import Api  
from flask_cors import CORS  # Import CORS class from flask_cors module
from routes import GetAllRecords, GetByCustId, GetByTransId, DeleteById, UpdateById, GetByMonth, PostTransaction, GetByDate  # Import route classes from routes module

app = Flask(__name__)  
api = Api(app)  
CORS(app)  # Enable Cross-Origin Resource Sharing (CORS) for the app

api.add_resource(GetAllRecords, "/v1/gpay/getall")  # To get all resources
api.add_resource(PostTransaction, "/v1/gpay/addTransaction")  # To add a transaction
api.add_resource(GetByCustId, "/v1/gpay/getById/<int:custId>")  # To get resources by customer ID
api.add_resource(GetByTransId, "/v1/gpay/getBytransId/<string:transId>")  # To get resources by transaction ID
api.add_resource(DeleteById, "/v1/gpay/deleteById/<int:custId>")  # To delete by customer ID
api.add_resource(UpdateById, "/v1/gpay/updateById/<int:custId>")  # To update by customer ID
api.add_resource(GetByMonth, "/v1/gpay/getByMonth/<int:month>")  # To get the resource by month
api.add_resource(GetByDate, "/v1/gpay/getByDate/<string:from_date>/<string:to_date>")  # To get transactions by date range

if __name__ == "__main__":  
    app.run(host="0.0.0.0", port=5000, debug=True)
