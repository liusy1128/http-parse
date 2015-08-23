
import sqlite3

def opendata():
        conn = sqlite3.connect("mydb.db")
        cur = conn.execute("""create table if not exists tianjia(
id integer primary key autoincrement, username varchar(128), passworld varchar(128),
address varchar(125), telnum varchar(128))""")
        return cur, conn
#查询全部的信息
 
 
def showalldata():
        print "-------------------处理后后的数据-------------------"
        hel = opendata()
        cur = hel[1].cursor()
        cur.execute("select * from tianjia")
        res = cur.fetchall()
        for line in res:
                for h in line:
                        print h,
                print
        cur.close()
#输入信息

def into():
        username1 = str(raw_input("请输入您的用户名："))
        passworld1 = str(raw_input("请输入您的密码："))
        address1 = str(raw_input("请输入您的地址："))
        telnum1 = str(raw_input("请输入您的联系电话："))
        return username1, passworld1, address1, telnum1
#  (添加)  往数据库中添加内容
 
 
def adddata():
        welcome = """-------------------欢迎使用添加数据功能---------------------"""
        print welcome
        person = into()
        hel = opendata()
        hel[1].execute("insert into tianjia(username, passworld, address, telnum)values (?,?,?,?)",
                                        (person[0], person[1], person[2], person[3]))
        hel[1].commit()
        print "-----------------恭喜你数据，添加成功----------------"
        showalldata()
        hel[1].close()
#  （删除）删除数据库中的内容
 
 
def deldata():
        welcome = "------------------欢迎您使用删除数据库功能------------------"
        print welcome
        delchoice = raw_input("请输入您想要删除用户的编号：")
        hel = opendata()              # 返回游标conn
        hel[1].execute("delete from tianjia where id ="+delchoice)
        hel[1].commit()
        print "-----------------恭喜你数据，删除成功----------------"
        showalldata()
        hel[1].close()
# （修改）修改数据的内容
 
 
def alter():
        welcome = "--------------------欢迎你使用修改数据库功能-----------------"
        print welcome
        changechoice = raw_input("请输入你想要修改的用户的编号:")
        hel =opendata()
        person = into()
        hel[1].execute("update tianjia set username=?, passworld= ?,address=?,telnum=? where id="+changechoice,
                                (person[0], person[1], person[2], person[3]))
        hel[1].commit()
        showalldata()
        hel[1].close()
# 查询数据
 
 
def searchdata():
        welcome = "--------------------欢迎你使用查询数据库功能-----------------"
        print welcome
        choice = str(raw_input("请输入你要查询的用户的编号："))
        hel = opendata()
        cur = hel[1].cursor()
        cur.execute("select * from tianjia where id="+choice)
        hel[1].commit()
        row = cur.fetchone()
        id1 = str(row[0])
        username = str(row[1])
        passworld = str(row[2])
        address = str(row[3])
        telnum = str(row[4])
        print "-------------------恭喜你，你要查找的数据如下---------------------"
        print ("您查询的数据编号是%s" % id1)
        print ("您查询的数据名称是%s" % username)
        print ("您查询的数据密码是%s" % passworld)
        print ("您查询的数据地址是%s" % address)
        print ("您查询的数据电话是%s" % telnum)
        cur.close()
        hel[1].close()
# 是否继续
 
 
def contnue1(a):
        choice = raw_input("是否继续？（y or n):")
        if choice == 'y':
                a = 1
        else:
                a = 0
        return a
 
 
if __name__ == "__main__":
        flag = 1
        while flag:
                welcome = "---------欢迎使用仙宝数据库通讯录---------"
                print welcome
                choiceshow = """
请选择您的进一步选择：
(添加)往数据库里面添加内容
(删除)删除数据库中内容
(修改)修改书库的内容
（查询）查询数据的内容
选择您想要的进行的操作：
"""
                choice = raw_input(choiceshow)
                print choice + 'start'
                test = "添加"
                print test
                if choice == "add":
                        adddata()
                        contnue1(flag)
                elif choice == "删除":
                        deldata()
                        contnue1(flag)
                elif choice == "修改":
                        alter()
                        contnue1(flag)
                elif choice == "dir":
                        searchdata()
                        contnue1(flag)
                else:
                        print "你输入错误，请重新输入"
