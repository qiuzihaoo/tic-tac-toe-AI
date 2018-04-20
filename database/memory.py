import MySQLdb


class Memory:

    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="tictactoe")

    def save(self, board_before, move, role, is_new):
        db = self.conn.cursor()
        move = int(move)
        board_before = board_after = board_before.replace(' ', '-')
        board_after[move] = role
        query = "INSERT INTO `shortterm` (`board_before`, `move`, `board_after`, `role`, `is_new`) VALUES ('%s', %d, '%s', '%s', %d)" % (board_before, move, board_after, role, is_new)
        print(query)
        db.execute(query)
        self.conn.commit()
