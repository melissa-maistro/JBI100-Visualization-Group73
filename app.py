#app.py
from jbi100_app.main import app

if __name__ == '__main__':
    # Nelle nuove versioni di Dash si usa .run() invece di .run_server()
    app.run(debug=True, port=8050)