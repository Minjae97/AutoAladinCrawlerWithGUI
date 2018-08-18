from AladinClass.AladinClass import AladinCrawler

crawler = AladinCrawler()   # 이렇게 했을 떄 뜨는 에러에 대해서 물어보기.
# crawler2 = AladinCrawler(root2) # 객체이면은 서로 영향을 안끼치니까 에러가 안나야 정상 아닌지 물어보기
crawler.root.mainloop()
# root2.mainloop()
