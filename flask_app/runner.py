from appl import app, db
from models import User, Entry, EntryPh, Chats, Comments, Sub, Likes, MesText


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)