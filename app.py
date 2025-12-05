from jbi100_app.main import app

if __name__ == '__main__':
    # Avvia il server
    # debug=True ti permette di vedere gli errori nel browser
    app.run_server(debug=True, port=8050)