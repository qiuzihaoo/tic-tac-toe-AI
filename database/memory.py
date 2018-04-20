import MySQLdb


class Memory:

    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="tictactoe")

    def save(self, board_before, move, role, is_new):
        query = self.conn.cursor()
        move = int(move)
        board_before = board_before.replace(' ', '-')
        board_after = list(board_before)
        board_after[move - 1] = role[0]
        board_after = "".join(board_after)
        statement = "INSERT INTO `shortterm` (`board_before`, `move`, `board_after`, `role`, `is_new`) " \
                    "VALUES ('%s', %d, '%s', '%s', %d)" \
                    % (board_before, move, board_after, role, is_new)
        print(statement)
        query.execute(statement)
        return self.conn.commit()
