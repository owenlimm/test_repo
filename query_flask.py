from flask import Flask, render_template, jsonify
import boto3

app = Flask(__name__)

def display_highest_total_count_per_robot():
    try:
        dynamodb = boto3.resource('dynamodb')
        table_name = 'cnc_kendek'
        table = dynamodb.Table(table_name)
        
        highest_total_counts = {}
        response = table.scan()

        for item in response['Items']:
            robot_id = item.get('robot_id')
            total_count = item.get('total_count')
            if robot_id and total_count:
                if robot_id not in highest_total_counts:
                    highest_total_counts[robot_id] = total_count
                else:
                    highest_total_counts[robot_id] = max(highest_total_counts[robot_id], total_count)

        return highest_total_counts

    except Exception as e:
        print(f"Error: {e}")
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    highest_total_counts = display_highest_total_count_per_robot()
    return jsonify(highest_total_counts)

if __name__ == '__main__':
    app.run(debug=True)
