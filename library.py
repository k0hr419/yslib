import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg
import sqlite3 as sq
import openpyxl as xl


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
    global user_info, ben_check, bp_id_entry, bp_pw_entry

    user_idpw = []
    user_info.append(bp_id_entry.get())
    user_info.append(bp_pw_entry.get())
    cur.execute("SELECT * FROM user_list")
    for i in cur.fetchall():
        if i[3]:
            ben_user_list.append(i[1])

    cur.execute("SELECT name, pw FROM user_list")
    for i in cur.fetchall():
        user_idpw.append(list(i))

    if user_info in user_idpw:
        if user_info[0] in ben_user_list:
            msg.showwarning("이용 정지", "연체 또는 기타 사유로 인해 현재 이용 불가 상태입니다.")
        else:
            bp_id_entry.delete(0, "end")
            bp_pw_entry.delete(0, "end")
            change_frame(frame_login, frame_home)
    else:
        msg.showwarning("로그인 불가", "아이디 또는 비밀번호가 잘못되었습니다.\n가입하지 않으셨다면 먼저 회원등록을 진행해주시기 바랍니다.")


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


class Signup:
    def __init__(self):
        self.check_id = False
        self.get_userid = []

        self.sign_up_page = tk.Toplevel(window)
        self.sign_up_page.title("회원 등록하기")

        signup = tk.Frame(self.sign_up_page)
        signup.pack(padx=20, pady=20)
        tk.Label(signup, text="회원등록", font=("", 15, "bold")).grid(row=0, column=0, padx=40, pady=(0, 10))

        tk.Label(signup, text="아이디", font=("", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=(5, 0))
        self.signup_id = tk.Entry(signup, width=25)
        self.signup_id.grid(row=2, column=0)
        tk.Label(signup, text="영문/숫자 10자이내").grid(row=3, column=0, sticky=tk.W)
        tk.Button(signup, text="중복확인", command=self.same_id).grid(row=4, column=0, sticky=tk.W)

        tk.Label(signup, text="비밀번호", font=("", 10, "bold")).grid(row=5, column=0, sticky=tk.W, pady=(5, 0))
        self.signup_pw = tk.Entry(signup, width=25, show="●")
        self.signup_pw.grid(row=6, column=0)

        tk.Label(signup, text="비밀번호확인", font=("", 10, "bold")).grid(row=7, column=0, sticky=tk.W, pady=(5, 0))
        self.signup_pwre = tk.Entry(signup, width=25, show="●")
        self.signup_pwre.grid(row=8, column=0)
        tk.Label(signup, text="한번 더 입력해주세요.").grid(row=9, column=0, sticky=tk.W)

        tk.Label(signup, text="학번/이름 (예: 3204김하랑)", font=("", 10, "bold")).grid(row=10, column=0, sticky=tk.W, pady=(5, 0))
        self.signup_school = tk.Entry(signup, width=25)
        self.signup_school.grid(row=11, column=0)
        tk.Label(signup, text="타인 정보도용 금지").grid(row=12, column=0, sticky=tk.W)

        tk.Button(signup, text="등록하기", font=("", 10, "bold"), command=self.input_check).grid(row=13, column=0, pady=(10, 0))

    def input_check(self):
        global cur
        if self.check_id:
            if self.signup_id.get() and self.signup_pw.get() and self.signup_school.get():
                if len(self.signup_id.get()) > 10:
                    msg.showwarning("알림", "아이디는 10글자 내로 입력해주세요.")
                elif self.signup_pw.get() != self.signup_pwre.get():
                    msg.showwarning("알림", "비밀번호와 비밀번호 재입력 값이 서로 다릅니다.")
                else:
                    cur.execute(f"insert into user_list (name, pw, scdata) values ('{self.signup_id.get()}', '{self.signup_pw.get()}', '{self.signup_school.get()}');")
                    con.commit()
                    self.signup_id.delete(0, "end")
                    self.signup_pw.delete(0, "end")
                    self.signup_pwre.delete(0, "end")
                    self.signup_school.delete(0, "end")
                    self.sign_up_page.destroy()
                    msg.showinfo("알림", "회원가입이 완료되었습니다.")
            else:
                msg.showwarning("알림", "아이디, 비밀번호, 개인정보 값이 제대로 입력되어있는지 확인해주세요.")
        else:
            msg.showwarning("알림", "아이디 중복확인을 완료해주세요.")

    def same_id(self):
        global cur
        cur.execute("select name from user_list")
        for i in cur.fetchall():
            self.get_userid.append(i[0])

        if self.signup_id.get() in self.get_userid:
            msg.showwarning("알림", "이미 사용중인 아이디입니다.")
        else:
            msg.showinfo("알림", "사용 가능한 아이디입니다.")
            self.check_id = True


def log_out():
    global user_info
    msg.askquestion("알림", "정말 로그아웃 하시겠습니까?")
    change_frame(frame_home, frame_login)
    user_info = []


user_info = []
ben_user_list = []

book_list = [{"title": "언더아이디어", "writer": "김하랑", "code": "아813", "number": "YS0000000", "byn": "대출가능"},
             {"title": "언더코딩", "writer": "aaa", "code": "adf", "number": "32144514", "byn": "대출가능"},
             {"title": "코딩에듀", "writer": "ㅗㅂㄷ", "code": "ㅁㄷㅎ", "number": "15425454465", "byn": "대출불가"}]

window_xy = [1000, 700]

window = tk.Tk()
window.title("yslib")
window.geometry(f"{window_xy[0]}x{window_xy[1]}")

con = sq.connect("loan_data.db")
cur = con.cursor()

user_list = xl.load_workbook("통합 문서1.xlsx", data_only=True)
load_ws = user_list["sheet1"]
print(load_ws.cell(1, 1).value)

# window - pack

# 프로그램 로고
logo = tk.PhotoImage(file="logo.gif")
tk.Label(window, image=logo, text="도서관", compound="top", font=("", 15, "bold"), relief="groove", borderwidth=2).pack(
    side="top", fill="x", expand=False, padx=5, ipadx=window_xy[0] / 2 - 77, ipady=6, pady=(5, 0))

# 로그인 프레임
frame_login = tk.Frame(window, borderwidth=2, relief="groove")
frame_login.pack(pady=20)

tk.Label(frame_login, text="로그인", font=("", 15, "bold")).grid(row=0, column=0, columnspan=3, pady=(5, 0))
tk.Label(frame_login, text="아이디").grid(row=1, column=0, padx=(15, 0))
tk.Label(frame_login, text="비밀번호").grid(row=2, column=0, padx=(15, 0))
bp_id_entry = tk.Entry(frame_login)
bp_id_entry.grid(row=1, column=1, columnspan=2, padx=(0, 15))
bp_pw_entry = tk.Entry(frame_login, show="●")
bp_pw_entry.grid(row=2, column=1, columnspan=2, padx=(0, 15))
enter_button = tk.Button(frame_login, text="확인", command=log_in)
enter_button.grid(row=3, column=0, columnspan=3, pady=(5, 0))

signup_page = tk.LabelFrame(frame_login, borderwidth=2, relief="groove")
signup_page.grid(row=4, column=0, columnspan=3, pady=(15, 5), ipadx=10)
tk.Label(signup_page, text="처음 이용한다면?").pack()
tk.Button(signup_page, text="회원등록하기", command=lambda: Signup()).pack(pady=(0, 3))

# 작업 선택 프레임
frame_home = tk.Frame(window)

frame_home_button = tk.LabelFrame(frame_home, pady=100, borderwidth=0)
frame_home_button.pack()
tk.Button(frame_home_button, text="대출", width=10, height=5, font=("", 15, "bold"), command=lambda: change_frame(frame_home, frame_search)).grid(row=0, column=0, ipadx=5)
tk.Button(frame_home_button, text="반납", width=10, height=5, font=("", 15, "bold"), command=lambda: change_frame(frame_home, frame_search)).grid(row=0, column=1, ipadx=5)
tk.Button(frame_home_button, text="대출정보조회", width=10, height=5, font=("", 15, "bold"), command=lambda: change_frame(frame_home, frame_loan)).grid(row=0, column=2, ipadx=5)
tk.Button(frame_home, text="로그아웃", command=log_out).pack()

# 검색 프레임
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
tk.Button(frame_search, text="뒤로가기", command=lambda: change_frame(frame_search, frame_home)).pack()

# 내 정보
frame_loan = tk.Frame(window)

book_loan = ttk.Treeview(frame_loan, columns=["title", "writer", "number", "loan_date", "return"])
book_loan.column("#0", width=50, anchor="center")
book_loan.heading("#0", text="번호")
book_loan.column("title", anchor="center")
book_loan.heading("title", text="제목")
book_loan.column("writer", width=150, anchor="center")
book_loan.heading("writer", text="저자")
book_loan.column("number", anchor="center")
book_loan.heading("number", text="일련번호")
book_loan.column("loan_date", anchor="center")
book_loan.heading("loan_date", text="대출일자")
book_loan.column("return", width=90, anchor="center")
book_loan.heading("return", text="반납일자")
book_loan.pack()
tk.Button(frame_loan, text="뒤로가기", command=lambda: change_frame(frame_loan, frame_home)).pack()

window.mainloop()
