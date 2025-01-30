from flask import Flask, jsonify, request
from airflow.models import DagBag
from constant import DAG_ID
from airflow.api.common.trigger_dag import trigger_dag
from datetime import datetime, timezone

dag_bag = DagBag()
app = Flask(__name__)


@app.route('/trigger', methods=['POST'])
def trigger():
    try:
        data = request.get_json()
        if not data or 'datas' not in data:
            return jsonify({'message': 'no data provided'}), 400

        if DAG_ID not in dag_bag.dags:
            return jsonify({'message': 'DAG not found'}), 404

        now = datetime.now()
        trigger_dag(
            dag_id=DAG_ID,
            run_id=f"nest_js_hit_trigger_{now.isoformat()}",
            conf=data,
            execution_date=now.astimezone(timezone.utc)
        )

        return jsonify({"message": "ETL triggered successfully"}), 200
    except Exception as e:
        print(f"unexpected error occurred: {e}")
        return jsonify({'message': 'unexpected error occurred'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
