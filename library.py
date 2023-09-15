import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
import sqlite3 as sq


def change_frame(f1, f2):
    f1.pack_forget()
    f2.pack()


def search_book():
    if search_entry.get():
        index_num = 0
        for i in book_result.get_children():
            book_result.delete(i)
        for i in book_list:
            if search_entry.get() in i["title"]:
                index_num += 1
                book_result.insert("", "end", values=list(i.values()), iid=str(index_num))
        search_entry.delete(0, "end")


def log_in():
    global user_info, ben_check, bp_num_entry, bp_name_entry

    user_info.append(bp_num_entry.get())
    user_info.append(bp_name_entry.get())
    cur.execute("SELECT * FROM user_list")
    for i in cur.fetchall():
        if i[3]:
            ben_user_list.append(i[1])

    cur.execute("SELECT * FROM user_list")
    for i in cur.fetchall():
        if user_info[0] == i[1] and user_info[1] == i[2]:
            if user_info[1] in ben_user_list:
                change_frame(frame_login, frame_home)
            else:
                msg.showwarning("이용 정지", "연체 또는 기타 사유로 인해 현재 이용 불가 상태입니다.")


def borrow():
    global book_result, get_value, cur, user_info
    get_value = book_result.item(book_result.focus())["values"]
    if get_value[4] == "대출가능":
        if ben_check:
            cur.execute(f"INSERT INTO user (num, name, booknum) VALUES('{user_info[0]}', '{user_info[1]}', '{get_value[3]}');")
            con.commit()
            for i in book_list:
                if i["code"] == get_value[2]:
                    i["byn"] = "대출불가"
                    print(i["byn"])
                    print("대출불가설정완료")
            cur.execute("SELECT * FROM user;")
            print(cur)
            cur.fetchall()
            msg.showinfo(f"대출 완료", "도서를 대출하였습니다.\n반납 예정일 : {}")
        else:
            msg.showwarning("이용 정지", f"연체 또는 기타 사유로 인해 현재 이용 불가 상태입니다.\n학번 : {user_info[0]}\n이름 : {user_info[1]}")
    else:
        msg.askokcancel("도서관 알림", "이미 대출중인 도서입니다.")


def read_loan():
    global user_info, cur
    cur.execute(f"SELECT * FROM user WHERE num = {int(user_info[0])} AND name = '{user_info[1]}';")
    print(cur.fetchone())


user_info = []
ben_user_list = []
ben_check = False

book_list = [{"title": "언더아이디어", "writer": "김하랑", "code": "아813", "number": "YS0000000", "byn": "대출가능"},
             {"title": "언더코딩", "writer": "aaa", "code": "adf", "number": "32144514", "byn": "대출가능"},
             {"title": "코딩에듀", "writer": "ㅗㅂㄷ", "code": "ㅁㄷㅎ", "number": "15425454465", "byn": "대출불가"}]

window_xy = [1000, 700]

window = tk.Tk()
window.title("yslib")
window.geometry(f"{window_xy[0]}x{window_xy[1]}")

con = sq.connect("loan_data.db")
cur = con.cursor()

# window - pack

# 프로그램 로고
logo = tk.PhotoImage(file="logo.gif")
tk.Label(window, image=logo, text="자료검색", compound="top", font=("", 15, "bold"), relief="groove", borderwidth=2).pack(
    side="top", fill="x", expand=False, padx=5, ipadx=window_xy[0] / 2 - 77, ipady=6, pady=(5, 0))

#로그인 프레임
frame_login = tk.Frame(window)
frame_login.pack()

tk.Label(frame_login, text="로그인", font=("", 15, "bold")).grid(row=0, column=0, columnspan=3, pady=(5, 0))
tk.Label(frame_login, text="학번").grid(row=1, column=0)
tk.Label(frame_login, text="이름").grid(row=2, column=0)
bp_num_entry = tk.Entry(frame_login)
bp_num_entry.grid(row=1, column=1, columnspan=2)
bp_name_entry = tk.Entry(frame_login)
bp_name_entry.grid(row=2, column=1, columnspan=2)
enter_button = tk.Button(frame_login, text="확인", command=log_in)
enter_button.grid(row=3, column=0, columnspan=3, pady=(5, 0))

signup_page = tk.LabelFrame(frame_login, borderwidth=2, relief="groove")
signup_page.grid(row=4, column=0, columnspan=3, pady=(15, 5), ipadx=10)
tk.Label(signup_page, text="처음 이용한다면?").pack()
tk.Button(signup_page, text="회원등록하기").pack(pady=(0, 3))

# 작업 선택 프레임
frame_home = tk.Frame(window)

tk.Button(frame_home, text="대출")
tk.Button(frame_home, text="반납")
tk.Button(frame_home, text="대출정보조회")

#검색 프레임
frame_search = tk.Frame(window)

frame_search_entry = tk.LabelFrame(frame_search)
frame_search_entry.pack()

tk.Label(frame_search_entry, text="제목").grid(row=0, column=0)
search_entry = tk.Entry(frame_search_entry, width=50)
search_entry.grid(row=0, column=1, columnspan=3)
tk.Button(frame_search_entry, text="검색", command=search_book).grid(row=0, column=4)

book_result = ttk.Treeview(frame_search, columns=["title", "writer", "code", "number", "byn"])
book_result.column("#0", width=50, anchor="center")
book_result.heading("#0", text="번호")
book_result.column("title", anchor="center")
book_result.heading("title", text="제목")
book_result.column("writer", width=150, anchor="center")
book_result.heading("writer", text="저자")
book_result.column("code", anchor="center")
book_result.heading("code", text="청구기호")
book_result.column("number", anchor="center")
book_result.heading("number", text="일련번호")
book_result.column("byn", width=90, anchor="center")
book_result.heading("byn", text="대출여부")

book_result.pack()

window.mainloop()
