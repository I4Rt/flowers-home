from config import *
from model.controller import *
import webview


if __name__ == "__main__":
    print('App is running')
    with app.app_context():
        db.create_all()
        

        window = webview.create_window('Flowers🌺', app, text_select=True)
        webview.start()
        # app.run(host='0.0.0.0', port=3031, debug=True)