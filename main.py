from app import app
from flask_wtf import CSRFProtect


csrf = CSRFProtect(app)



if __name__ == '__main__':
    app.run(debug=True)