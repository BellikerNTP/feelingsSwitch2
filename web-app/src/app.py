from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/run-script', methods=['POST'])
def run_script():
    data = request.json
    qntPosts = data.get('qntPosts', 100)
    cntMax = data.get('cntMax', 100)
    startDate = data.get('startDate', None)
    endDate = data.get('endDate', None)

    try:
        # Ejecuta el script Python con los parámetros
        result = subprocess.run(
            ['python', 'pruebaGuardar.py', str(qntPosts), str(cntMax), startDate, endDate],
            capture_output=True,
            text=True
        )
        return jsonify({'output': result.stdout, 'error': result.stderr})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)