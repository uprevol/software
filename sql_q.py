import mysql.connector
from datetime import datetime
import json

# mydb = mysql.connector.connect(
#   host="35.200.196.93",
#   user="root",
#   password="UPrEVOL",
#   database="uprevol"
# )
def mydb_func():
    global mydb
    mydb = mysql.connector.connect(
        host="uprevolins.cryjzxrydmbi.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="Uprevol1234",
        database="uprevol"
    )

ls = []
ls2 = []
check = ['sus-', 'ver-', 'rec-', 'work-', 'worker-', 'adm-', 'apply-', 'del-']

class sql_queries():

    def sus_display(self, adm_id):
        cur = mydb.cursor()
        cur.execute("SELECT sn,sus_id,rec_id,worker_id,message,assigned_date,review_message FROM suspicious WHERE assigned_to = %s AND (passed IS NULL AND action IS NULL )", [adm_id])
        rows_dic = cur.fetchall()
        print(rows_dic)
        return rows_dic
    def sus_history(self, adm_id):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT sn,sus_id,rec_id,worker_id,message,message_to_user,passed_note,passed_date,action,action_date FROM suspicious WHERE assigned_to = %s AND (passed IS NOT NULL OR action IS NOT NULL ) ", [adm_id])  #OR action IS NOT NULL
        data = mycursor.fetchall()
        return data

    def sus_passed(self, sid, passed_note):
        now = datetime.now()
        passed_date = now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE suspicious SET passed = 1, passed_note = %s, passed_date = %s WHERE sus_id = %s ", (passed_note, passed_date, sid))
        mydb.commit()
        print("done")

    def ver_display(self, adm_id):
        cur = mydb.cursor()
        cur.execute("SELECT sn,ver_id,worker_id,message,assigned_date,review_message FROM verification WHERE assigned_to = %s AND (passed IS NULL AND ver_status IS NULL )", [adm_id])
        data = cur.fetchall()
        print(data)
        return data

    def ver_history(self, adm_id):
        cur = mydb.cursor()
        cur.execute("SELECT sn,ver_id,worker_id,message,message_to_user,passed_note,passed_date,ver_status,ver_date FROM verification WHERE assigned_to = %s AND (passed IS NOT NULL OR ver_status IS NOT NULL)", [adm_id])
        data = cur.fetchall()
        print(data)
        return data

    def ver_passed(self, ver_id, passed_note):
        now = datetime.now()
        passed_date = now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()
        print(passed_note)
        mycursor.execute("UPDATE verification SET passed = 1, passed_note = %s, passed_date = %s WHERE ver_id = %s", (passed_note, passed_date, ver_id))
        mydb.commit()
        print("done")

    def del_display(self, adm_id):
        cur = mydb.cursor()
        cur.execute("SELECT sn,delete_id,rec_id,worker_id,message,assigned_date,review_message FROM delete_req WHERE assigned_to = %s AND (passed IS NULL AND action IS NULL )", [adm_id])
        rows_dic = cur.fetchall()
        return rows_dic

    def del_history(self, adm_id):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT sn,delete_id,rec_id,worker_id,message,message_to_user,passed_note,passed_date,action,action_date FROM delete_req WHERE assigned_to = %s AND (passed IS NOT NULL OR action IS NOT NULL ) ", [adm_id])
        data = mycursor.fetchall()
        return data

    def del_passed(self, did, passed_note):
        now = datetime.now()
        passed_date = now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE delete_req SET passed = 1, passed_note = %s, passed_date = %s WHERE delete_id = %s", (passed_note, passed_date, did))
        mydb.commit()

    def ver_action(self, ver_status, message, message_to_user, ver_id):
        now = datetime.now()
        ver_date = now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE verificatio"
                         "n SET ver_date = %s, ver_status = %s, message = %s, message_to_user = %s WHERE ver_id = %s", (ver_date, ver_status, message, message_to_user , ver_id))
        mydb.commit()
        print("done")

    def sus_action(self, sid, message, message_to_user, action):
        now = datetime.now()
        action_date = now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE suspicious SET action_date = %s, action = %s, message = %s, message_to_user = %s WHERE sus_id = %s", (action_date, action, message, message_to_user, sid))
        mydb.commit()
        print("done")

    def del_action(self, did, message, message_to_user, action):
        now = datetime.now()
        action_date = now.strftime("%Y-%m-%d")
        mycursor = mydb.cursor()
        mycursor.execute("UPDATE delete_req SET action_date = %s, action = %s, message = %s, message_to_user = %s WHERE delete_id = %s", (action_date, action, message, message_to_user, did))
        mydb.commit()

    def review(self, adm_id):
        mycursor = mydb.cursor()
        print(adm_id)
        mycursor.execute("SELECT delete_id,review_message FROM delete_req WHERE assigned_to = %s AND review = 1", [adm_id])
        data = mycursor.fetchall()
        mycursor1 = mydb.cursor()
        mycursor1.execute("SELECT sus_id,review_message FROM suspicious WHERE assigned_to = %s AND review = 1", [adm_id])
        data1 = mycursor1.fetchall()
        mycursor2 = mydb.cursor()
        mycursor2.execute("SELECT ver_id,review_message FROM verification WHERE assigned_to = %s AND review = 1", [adm_id])
        data2 = mycursor2.fetchall()
        # "SELECT (SELECT * FROM suspicious WHERE assigned_to = %s AND review = 1 ),"
        # "(SELECT * FROM verification WHERE assigned_to = %s AND review = 1 ),"
        # "(SELECT * FROM delete_req WHERE assigned_to = %s AND review = 1 ) ", (adm_id, adm_id, adm_id))

        data.extend(data1)
        data.extend(data2)

        print("done")
        return data

    def dashboard(self, adm_id):
        cur = mydb.cursor()
        cur.execute("SELECT (SELECT COUNT(*) FROM suspicious),"
                    "(SELECT COUNT(*) FROM verification),"
                    "(SELECT COUNT(*) FROM delete_req),"
                    "(SELECT COUNT(*) FROM suspicious WHERE action IS NOT NULL),"
                    "(SELECT COUNT(*) FROM verification WHERE ver_status IS NOT NULL),"
                    "(SELECT COUNT(*) FROM delete_req WHERE action IS NOT NULL),"
                    "(SELECT COUNT(*) FROM suspicious WHERE assigned_to = %s),"
                    "(SELECT COUNT(*) FROM verification WHERE assigned_to = %s),"
                    "(SELECT COUNT(*) FROM delete_req WHERE assigned_to = %s),"
                    "(SELECT COUNT(*) FROM suspicious WHERE action IS NOT NULL AND assigned_to = %s),"
                    "(SELECT COUNT(*) FROM verification WHERE ver_status IS NOT NULL AND assigned_to = %s), "
                    "(SELECT COUNT(*) FROM delete_req WHERE action IS NOT NULL AND assigned_to = %s)", (adm_id,adm_id,adm_id,adm_id,adm_id,adm_id))
        rows_dic = cur.fetchall()
        return rows_dic

    def login(self, username, password):
        cur = mydb.cursor()
        cur.execute("SELECT name, admin_id FROM admins WHERE username = %s AND password = %s", (username, password))
        body = cur.fetchall()
        print(body)
        try:
            name = body[0][0]
            adm_id = body[0][1]
            data = {'result': "success", 'status': 200, 'name': name, 'adm_id': adm_id}
        except:
            data = {'result': "failed", 'status': 200}
        return data


    def build_tree(self, sid):
        global ls, ls2, dic_main
        ls = []
        ls2 = []
        dic_main = {}
        self.algo(sid)
        self.main()
        return dic_main

    def main(self):
        global ls, ls2, check
        for a in ls2:
            for a2 in a.values():
                for x in a2.values():
                    for y in check:
                        if (x not in ls) and (y in x):
                            print("<<", x, y)
                            self.algo(x)
                        else:
                            pass
    def algo(self, id):
        dic = {}
        global ls, ls2, check, dic_main
        for y in check:
            if y in id:
                if y == "sus-":
                    table = "suspicious"
                    colm = "sus_id"
                elif y == "ver-":
                    table = "verification"
                    colm = "ver_id"
                elif y == "rec-":
                    table = "recruiter"
                    colm = "rec_id"
                elif y == "work-":
                    table = "work"
                    colm = "work_id"
                elif y == "worker-":
                    table = "worker"
                    colm = "worker_id"
                elif y == "adm-":
                    table = "admins"
                    colm = "admin_id"
                elif y == "del-":
                    table = "delete_req"
                    colm = "delete_id"
                else:
                    table = "applied"
                    colm = "apply_id"
                cur2 = mydb.cursor()
                cur2.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = %s ORDER BY ORDINAL_POSITION",
                    [table])
                colm_data = cur2.fetchall()
                colm_data = [item1 for t1 in colm_data for item1 in t1]
                cur = mydb.cursor()
                query = f"SELECT * FROM {table} WHERE {colm} = '{id}'"
                print(query)
                cur.execute(query)
                row_data = cur.fetchall()
                row_data = [item for t in row_data for item in t]
                row = []
                for x in row_data:
                    x = str(x)
                    row.append(x)
                if len(row_data) != 0:
                    node_dic = {colm_data[i]: row[i] for i in range(len(colm_data))}
                    dic[id] = node_dic
                    dic_main[id] = node_dic
                    ls2.append(dic)
                ls.append(id)

                break
            else:
                pass

mydb_func()