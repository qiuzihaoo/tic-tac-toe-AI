import MySQLdb


class ShortMemory:

    def __init__(self):
        try:
            self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="tictactoe")
        except:
            print("Please make sure you are running Mysql server(XAMPP)!")
            exit()

    def save(self, board_before, move, role, is_new):
        query = self.conn.cursor()
        move = int(move)
        board_before = board_before.replace(' ', '-')
        board_after = list(board_before)
        board_after[move - 1] = role[0]
        board_after = "".join(board_after)
        statement = "INSERT INTO `shortterm` (`board_before`, `move`, `board_after`, `role`, `new`) " \
                    "VALUES ('%s', %d, '%s', '%s', %d)" \
                    % (
                        board_before,
                        move,
                        board_after,
                        role,
                        is_new
                    )
        try:
            query.execute(statement)
            self.conn.commit()
            return True
        except self.conn.Error as e:
            print("Error code:", e.errno)  # error number
            print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
            print("Error message:", e.msg)  # error message
            print("Error:", e)
        except:
            print("Short memory Unknown Error!")
            return False

    def read_all(self):
        query = self.conn.cursor()
        statement = "select id, board_before, move, board_after, role, new from shortterm order by id DESC"
        try:
            query.execute(statement)
            result = []
            for (id, board_before, move, board_after, role, is_new) in query:
                result.append({
                    "id": id,
                    "board_before": board_before,
                    "move": move,
                    "board_after": board_after,
                    "role": role,
                    "is_new": is_new
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.errno)  # error number
            print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
            print("Error message:", e.msg)  # error message
            print("Error:", e)
        except:
            print("Short memory Unknown Error!")
            return False

    def read_select(self, board, move=-1):
        query = self.conn.cursor()
        board = board.replace(' ', '-')
        statement = "select id, board_before, move, board_after, role, new from shortterm "
        if move > -1:
            statement = statement + "where board_before = %s and move = %d order by id DESC" \
                        % (board, move)
        else:
            statement = statement + "where board_before = %s order by id DESC" \
                        % (board)
        try:
            query.execute(statement)
            result = []
            for (id, board_before, move, board_after, role, new) in query:
                result.append({
                    "id": id,
                    "board_before": board_before.replace('-', ' '),
                    "move": move,
                    "board_after": board_after.replace('-', ' '),
                    "role": role,
                    "new": new
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.errno)  # error number
            print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
            print("Error message:", e.msg)  # error message
            print("Error:", e)
        except:
            print("Short memory Unknown Error!")
            return False


class LongMemory:

    def __init__(self):
        self.conn = MySQLdb.connect(host="127.0.0.1", user="root", passwd="", db="tictactoe")

    def save(self, record):
        query = self.conn.cursor()
        record["move"] = int(record["move"])
        record["score"] = int(record["score"])
        record["explored"] = int(record["explored"])
        record["board_before"] = record["board_before"].replace(' ', '-')
        record["board_after"] = record["board_after"].replace(' ', '-')
        statement = "INSERT INTO `longterm` (`board_before`, `move`, `board_after`, `score`, `role`, `explored`) " \
                    "VALUES ('%s', %d, '%s', %d, '%s', %d)" % (
                        record["board_before"],
                        record["move"],
                        record["board_after"],
                        record["score"],
                        record["role"],
                        record["explored"]
                    )
        try:
            query.execute(statement)
            self.conn.commit()
            return True
        except self.conn.Error as e:
            print("Error code:", e.errno)  # error number
            print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
            print("Error message:", e.msg)  # error message
            print("Error:", e)
        except:
            print("Long memory Unknown Error!")
            return False

    def read_all(self):
        query = self.conn.cursor()
        statement = "select id, board_before, move, board_after, score, role, explored from longterm order by id DESC"
        try:
            query.execute(statement)
            result = []
            for (id, board_before, move, board_after, score, role, explored) in query:
                result.append({
                    "id": id,
                    "board_before": board_before,
                    "move": move,
                    "board_after": board_after,
                    "score": score,
                    "role": role,
                    "explored": explored
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.errno)  # error number
            print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
            print("Error message:", e.msg)  # error message
            print("Error:", e)
        except:
            print("Long memory Unknown Error!")
            return False

    def read_select(self, board, move=-1):
        query = self.conn.cursor()
        board = board.replace(' ', '-')
        statement = "select id, board_before, move, board_after, score, role, explored from longterm "
        if move > -1:
            statement = statement + "where board_before = %s and move = %d order by id DESC" \
                        % (board, move)
        else:
            statement = statement + "where board_before = %s order by id DESC" \
                        % (board)
        try:
            query.execute(statement)
            result = []
            for (id, board_before, move, board_after, role, explored) in query:
                result.append({
                    "id": id,
                    "board_before": board_before.replace('-', ' '),
                    "move": move,
                    "board_after": board_after.replace('-', ' '),
                    "role": role,
                    "explored": explored
                })
            return result
        except self.conn.Error as e:
            print("Error code:", e.errno)  # error number
            print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
            print("Error message:", e.msg)  # error message
            print("Error:", e)
        except:
            print("Long memory Unknown Error!")
            return False

    def update(self, record):
        query = self.conn.cursor()
        record["id"] = int(record["id"])
        record["move"] = int(record["move"])
        record["score"] = int(record["score"])
        record["explored"] = int(record["explored"])
        record["board_before"] = record["board_before"].replace(' ', '-')
        record["board_after"] = record["board_after"].replace(' ', '-')
        statement = "update `longterm` SET " \
                    "`board_before` = %s, `move` = %d, `board_after` = %s, " \
                    "`score` = %d, `role` = %s, `explored` = %d " \
                    "where id = %d" \
                    % (
                        record["board_before"],
                        record["move"],
                        record["board_after"],
                        record["score"],
                        record["role"],
                        record["explored"],
                        record["id"],
                    )

        try:
            query.execute(statement)
            self.conn.commit()
            return True
        except self.conn.Error as e:
            print("Error code:", e.errno)  # error number
            print("SQLSTATE value:", e.sqlstate)  # SQLSTATE value
            print("Error message:", e.msg)  # error message
            print("Error:", e)
        except:
            print("Long memory Unknown Error!")
            return False
