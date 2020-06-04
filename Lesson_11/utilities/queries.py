from Lesson_11.utilities import context_manager as cm


class Query:
    def __init__(self):
        self.db = "telebot.db"

    def add_feedback(self, info):
        sql = "INSERT INTO feedback ('chat_id', 'full_name', 'phone', 'email', 'address', 'feedback') " \
              "VALUES (?,?,?,?,?,?)"
        try:
            with cm.MyDBManager(self.db, "w") as db:
                db.executemany(sql, [(info['chat_id'], info['full_name'], info['phone'], info['email'], info['address'],
                                      info['feedback'])])
                return True
        except (TypeError, KeyError):
            return False
