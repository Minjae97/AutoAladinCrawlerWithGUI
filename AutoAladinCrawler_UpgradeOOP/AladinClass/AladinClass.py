from tkinter import *
from tkinter.filedialog import *
from selenium import webdriver
from bs4 import BeautifulSoup
import time

class AladinCrawler:
####################전역변수부############################
    def __init__(self):
        self.path = ""
        self.driver = ""
        self.index = ""
        self.value = ""
        self.booklist = []
        self.storelist = []
        self.idx = 1
        self.root = Tk()

        self.root.configure(width="140m", height="170m")
        self.root.title("알라딘 중고서점 자동화 프로그램1.1v")

        self.root.bind('<Key>',self.key_input) #키보드 input을 위한 명령문

        self.SearchEntry = Entry(self.root)
        self.SearchEntry.place(x=10, y=100, width=170, height= 30)

        self.Listbox1 = Listbox(self.root)
        self.Listbox1.place(x=10, y=150, width=170, height= 400)
        self.Listbox1.bind('<<ListboxSelect>>', self.onselect)

        self.Listbox2 = Listbox(self.root)
        self.Listbox2.place(x=320, y=150, width=170, height= 400)


        self.InstructionLB = Label(self.root, text = "경로를 찾아주세요")
        self.InstructionLB.place(x=100, y=10, width=300, height=30)


        Button(self.root, text="경로 찾기", command=self.GetFilePath).place(x=10, y=10, width=100, height=30)
        Button(self.root, text="브라우저 열기", command=self.OpenBrowser).place(x=10, y=50, width=100, height=30)
        Button(self.root, text="책 추가", command=self.InsertName).place(x=200, y=100, width=100, height=30)
        Button(self.root, text="책 조회", command=self.SearchBooks).place(x=200, y=150, width=100, height=30)
        Button(self.root, text="지점 검색", command=self.LookStores).place(x=200, y=200,width=100, height=30)
        Button(self.root, text="책 삭제", command=self.DeleteInListbox1).place(x=200, y=250,width=100, height=30)


####################함수부################################
    def GetFilePath(self):
        self.path = askopenfilename()
        print(self.path)
        self.InstructionLB = Label(self.root, text=self.path)
        self.InstructionLB.place(x=100, y=10, width=300, height=30)

    def OpenBrowser(self):
        self.driver = webdriver.Chrome(self.path)
        time.sleep(1)
        self.driver.get("http://used.aladin.co.kr/usedstore/wgate.aspx")
        time.sleep(1)
        self.InstructionLB = Label(self.root, text="브라우저가 열렸습니다.")
        self.InstructionLB.place(x=100, y=10, width=300, height=30)

    def InsertName(self):
        self.bookname = self.SearchEntry.get()
        if self.bookname.strip() == "":
            pass
        else:
            self.Listbox1.insert(self.idx, self.bookname)
            self.SearchEntry.delete(0,END)
            self.booklist.append(self.bookname)
            # print(booklist)
            self.InstructionLB = Label(self.root, text="책이 추가되었습니다")
            self.InstructionLB.place(x=100, y=10, width=300, height=30)
            self.idx += 1

    def SearchBooks(self):
        # global driver, booklist, storelist, InstructionLB
        self.InstructionLB = Label(self.root, text="책을 조회중입니다. 만지지 마세요.")
        self.InstructionLB.place(x=100, y=10, width=300, height=30)
        for book in self.booklist:
            self.SearchBox = self.driver.find_element_by_xpath('//*[@id="SearchWord"]')
            self.SearchBox.send_keys("\b"*50+book)
            self.SearchBox.submit()
            time.sleep(2)
            self.html = self.driver.page_source
            self.s1 = BeautifulSoup(self.html, "html.parser")
            self.s2 = self.s1.find("div", class_="usedshop_off_text2_box")
            # print(s2)
            if self.s2 == None:
                self.storelist.append("검색 결과 없음")
                # print("검색 결과 없음")
            else:
                # print(s2.text.split(", "))
                self.storelist.append(self.s2.text.split(", "))

            # print(storelist)
        self.InstructionLB = Label(self.root, text="조회가 완료되었습니다.")
        self.InstructionLB.place(x=100, y=10, width=300, height=30)

    def onselect(self, evt):
        # global index, value
        self.w = evt.widget
        self.index = self.w.curselection() #index 0부터 시작
        self.value = self.w.get(self.index)
        print(self.index, self.value)

    def LookStores(self):
        # global index, value, booklist, storelist, Listbox2, InstructionLB
        if self.index == "":
            self.InstructionLB = Label(self.root, text="책을 선택하세요")
            self.InstructionLB.place(x=100, y=10, width=300, height=30)
        else:
            print(self.booklist[self.index[0]])
            print(self.storelist[self.index[0]])
            self.Listbox2.delete(0,END)
            for store in self.storelist[self.index[0]]:
                if type(self.index[0]) == str: # 검색 결과 없음 떄문에 추가함
                    self.Listbox2.insert("end", self.index[0])
                else:
                    self.Listbox2.insert("end", store)

    def DeleteInListbox1(self):
        # global index, value, Listbox1, InstructionLB
        if self.index == "":
            self.InstructionLB = Label(self.root, text="책을 선택하세요")
            self.InstructionLB.place(x=100, y=10, width=300, height=30)
        else:
            self.Listbox1.delete(self.index[0], self.index[0]) #0번쨰 인덱스 지우는 걸 어떻게 처리할까?
            del self.booklist[self.index[0]]

    def key_input(self, value):
        if value.keysym == "Return":
            self.InsertName()
        elif value.keysym == "F5":
            self.OpenBrowser()
            time.sleep(2)
            self.SearchBooks()
