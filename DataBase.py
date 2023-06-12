import psycopg2


class DataBase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getAdminClaims(self):
        sql = "SELECT claims.id, claims.date, routes.route, drivers.surname, buses.number, users.name, claims.amount, claims.sum from claims " \
              "left join routes on claims.route_id = routes.id left join drivers on claims.driver_id = drivers.id " \
              "left join buses on claims.bus_id = buses.id left join users on claims.user_id = users.id;"
        try:
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            if res:
                return res
        except psycopg2.Error as e:
            print(e)
            return False

    def showAdminClaim(self, id_claim):
        try:
            self.__cur.execute(f"SELECT claims.date, routes.route, users.name, claims.amount, claims.sum from claims "
                               f"left join routes on claims.route_id = routes.id left join users on claims.user_id = users.id WHERE claims.id={id_claim} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res
        except psycopg2.Error:
            return False

    def updateClaim(self, id_claim, id_worker, id_bus):
        try:
            self.__cur.execute(f"UPDATE claims SET driver_id='{id_worker}', bus_id='{id_bus}' WHERE id={id_claim}")
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def deleteClaim(self, id_claim):
        try:
            self.__cur.execute(f"DELETE FROM claims WHERE id={id_claim}")
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def addUser(self, name, login, psw):
        try:
            self.__cur.execute("INSERT INTO users (name, login, password) VALUES"
                               "(%s, %s, %s);", (name, login, psw))
            self.__db.commit()
        except psycopg2.Error as e:
            return False
        return True

    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                return False
            return res
        except psycopg2.Error as e:
            return False

    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE login = '{email}' LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                return False
            else:
                return res
        except psycopg2.Error as e:
            return False

    def getUserClaims(self, user_id):
        try:
            self.__cur.execute(f"SELECT claims.date, routes.route, drivers.surname, buses.number, claims.amount, claims.sum FROM claims left join routes on claims.route_id = routes.id "
                               f"left join drivers on claims.driver_id = drivers.id left join buses on claims.bus_id = buses.id WHERE user_id = {user_id}")
            res = self.__cur.fetchall()
            if not res:
                return False
            else:
                return res
        except psycopg2.Error as e:
            return False

    def newUserClaim(self, route_id, user_id, date, amount, sum):
        try:
            self.__cur.execute("INSERT INTO claims (route_id, user_id, date, amount, sum) VALUES (%s, %s, %s, %s, %s);", (route_id, user_id, date, amount, sum))
            self.__db.commit()
        except psycopg2.Error:
            return False
        return True

    def addWorker(self, name, surname, second_name, age, passport):
        try:
            self.__cur.execute("INSERT INTO drivers (name, surname, second_name, age, passport) VALUES"
                               "(%s, %s, %s, %s, %s);", (name, surname, second_name, age, passport))
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def showWorkers(self):
        try:
            self.__cur.execute("SELECT * FROM drivers")
            res = self.__cur.fetchall()
            if not res:
                return False
            else:
                return res
        except psycopg2.Error as e:
            print(e)
            return False

    def getWorkerId(self, driver):
        try:
            self.__cur.execute(f"SELECT id FROM drivers WHERE surname = '{driver}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res[0]
            else:
                return False
        except psycopg2.Error:
            return False

    def worker(self, id_worker):
        try:
            self.__cur.execute(f"SELECT * FROM drivers WHERE id={id_worker} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                return False
            else:
                return res
        except psycopg2.Error:
            return False

    def updateWorker(self, id_worker, name, surname, second_name, age, passport):
        try:
            self.__cur.execute(f"UPDATE drivers SET name='{name}', surname='{surname}', second_name='{second_name}', age='{age}',"
                               f"passport='{passport}' WHERE id={id_worker}")
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def deleteWorker(self, id_worker):
        try:
            self.__cur.execute(f"DELETE FROM drivers WHERE id={id_worker}")
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def bus(self, id_bus):
        try:
            self.__cur.execute(f"SELECT * FROM buses WHERE id={id_bus} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                return False
            else:
                return res
        except psycopg2.Error:
            return False

    def showBuses(self):
        try:
            self.__cur.execute("SELECT * FROM buses")
            res = self.__cur.fetchall()
            if not res:
                return False
            else:
                return res
        except psycopg2.Error as e:
            print(e)
            return False

    def getBusId(self, bus):
        try:
            self.__cur.execute(f"SELECT id FROM buses WHERE number = '{bus}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res[0]
            else:
                return False
        except psycopg2.Error:
            return False

    def addBus(self, number, model, year):
        try:
            self.__cur.execute("INSERT INTO buses (number, model, year) VALUES "
                               "(%s, %s, %s);", (number, model, year))
            self.__db.commit()
        except psycopg2.Error:
            return False
        return True

    def updateBus(self, id_bus, number, model, year):
        try:
            self.__cur.execute(f"UPDATE buses SET number='{number}', model='{model}', year='{year}' WHERE id={id_bus}")
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def deleteBus(self, id_bus):
        try:
            self.__cur.execute(f"DELETE FROM buses WHERE id={id_bus}")
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def route(self, id_route):
        try:
            self.__cur.execute(f"SELECT * FROM routes WHERE id={id_route} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                return False
            else:
                return res
        except psycopg2.Error:
            return False

    def allRoutes(self):
        try:
            self.__cur.execute("SELECT * FROM routes")
            res = self.__cur.fetchall()
            if res:
                return res
            else:
                return False
        except psycopg2.Error:
            return False

    def getRoutes(self):
        try:
            self.__cur.execute("SELECT route FROM routes")
            res = self.__cur.fetchall()
            if res:
                return res
            else:
                return False
        except psycopg2.Error:
            return False

    def getRouteId(self, route):
        try:
            self.__cur.execute(f"SELECT id FROM routes WHERE route = '{route}' LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res[0]
            else:
                return False
        except psycopg2.Error:
            return False

    def getRoutePrice(self, route_id):
        try:
            self.__cur.execute(f"SELECT price FROM routes WHERE id = {route_id} LIMIT 1")
            res = self.__cur.fetchone()
            if res:
                return res[0]
            else:
                return False
        except psycopg2.Error:
            return False

    def addRoute(self, route, days, price):
        try:
            self.__cur.execute("INSERT INTO routes (route, days, price) VALUES"
                               "(%s, %s, %s);", (route, days, price))
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def updateRoute(self, route_id, route, days, price):
        try:
            self.__cur.execute(f"UPDATE routes SET route='{route}', days='{days}', price='{price}' WHERE id={route_id}")
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True

    def deleteRoute(self, route_id):
        try:
            self.__cur.execute(f"DELETE FROM routes WHERE id={route_id}")
            self.__db.commit()
        except psycopg2.Error as e:
            print(e)
            return False
        return True
