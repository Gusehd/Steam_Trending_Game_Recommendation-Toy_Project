from PyQt5.QtWidgets import *
from PyQt5 import uic
import sys
import urllib.request as req
from bs4 import BeautifulSoup
import random

#steam trending game random Recommendation - kor

#robots.txt
#Host: store.steampowered.com
#User-Agent: *
#Disallow: /share/
#Disallow: /news/externalpost/
#Disallow: /account/emailoptout/?*token=
#Disallow: /login/?*guestpasskey=
#Disallow: /join/?*redir=
#Disallow: /account/ackgift/
#Disallow: /email/
#Disallow: /widget/

game_category = {1:"&category=rogue_like_rogue_lite" , 2:"&category=rpg" , 3:"Action&tagid=19" ,
                 4:"Action%20Roguelike&tagid=42804" , 5:"&category=arcade_rhythm" , 6:"Beat%20%27em%20up&tagid=4158",
                 7:"&category=fighting_martial_arts", 8:"&category=action_fps" , 9:"&category=action_run_jump",
                 10:"&category=action_tps" , 11:"=&category=adventure_and_casual", 12:"Adventure&tagid=21",
                 13:"&category=adventure_rpg" , 14:"Casual&tagid=597" , 15:"Metroidvania&tagid=1628",
                 16:"&category=puzzle_matching" , 17:"&category=interactive_fiction" , 18:"Visual%20Novel&tagid=3799",
                 19:"Action%20RPG&tagid=4231" ,20:"JRPG&tagid=4434" , 21:"Party-Based%20RPG&tagid=10695",
                 22:"&category=rpg_strategy_tactics" , 23:"&category=rpg_turn_based" , 24:"Simulation&tagid=599" ,
                 25:"&category=sim_building_automation" , 26:"&category=sim_business_tycoon" , 27:"&category=sim_dating",
                 28:"&category=sim_farming_crafting" , 29:"&category=sim_life" , 30:"&category=sim_physics_sandbox",
                 31:"&category=sim_space_flight" , 32:"&category=strategy" , 33:"&category=strategy_card_board" ,
                 34:"&category=strategy_cities_settlements" ,35:"&category=strategy_grand_4x" , 36:"&category=strategy_military",
                 37:"RTS&tagid=1676" , 38:"Tower%20Defense&tagid=1645" , 39:"Turn-Based%20Strategy&tagid=1741" ,
                 40:"&category=sports_and_racing" , 41:"Sports&tagid=701" , 42:"&category=sports_fishing_hunting" ,
                 43:"&category=sports_individual" , 44:"Racing&tagid=699" , 45:"&category=racing_sim" ,
                 46:"&category=sports_sim" , 47:"&category=sports_team"}


tr_name = []
tr_url = []

def find_price(st):
    return st.find("???")

def evalu(url_review):
    url = url_review.replace("\\", "")
    headers = req.Request(url, headers={"Accept-Language": "ko-KR"})
    code = req.urlopen(headers)
    soup = BeautifulSoup(code, "html.parser")

    review = soup.select("div.summary.column span.game_review_summary")
    date = soup.select("div.date")
    dev_n_pub = soup.select("div.summary.column > a")
    price1 = soup.select_one("div.discount_original_price")
    price2 = soup.select_one("div.game_purchase_price.price")
    if len(review) == 1:
        review_1 = str(review[0]).replace("user","??????").replace("reviews","??????").replace("Very","??????").replace("Positive"
                    ,"?????????").replace("Mostly","?????????").replace("Mixed","?????????").replace("Negative","?????????").replace("Overwhelmingly","???????????????")
        main_dialog.textBrowser.append("?????? ?????? : " + review_1)
    elif len(review) >= 2:
        review_1 = str(review[0]).replace("user", "??????").replace("reviews", "??????").replace("Very", "??????").replace(
            "Positive", "?????????").replace("Mostly", "?????????").replace("Mixed", "?????????").replace("Negative", "?????????").replace(
            "Overwhelmingly", "???????????????")
        review_2 = str(review[1]).replace("user", "??????").replace("reviews", "??????").replace("Very", "??????").replace(
            "Positive", "?????????").replace("Mostly", "?????????").replace("Mixed", "?????????").replace("Negative", "?????????").replace(
            "Overwhelmingly", "???????????????")
        main_dialog.textBrowser.append("?????? ?????? : " + review_1)
        main_dialog.textBrowser.append("?????? ?????? : " + review_2)
    if len(date) != 0:
        date_str = str(date[0].string).replace(" Jan","??? 1???").replace(" Feb","??? 2???").replace(" Mar","??? 3???").replace(" Apr","??? 4???").replace(
            " May","??? 5???").replace(" Jun","??? 6???").replace(" Jul","??? 7???").replace(" Aug","??? 8???").replace(" Sep","??? 9???").replace(" Oct","??? 10???").replace(
            " Nov","??? 11???").replace(" Dec","??? 12???")
        main_dialog.textBrowser.append("?????? ?????? : " + date_str)
    if len(dev_n_pub) != 0:
        main_dialog.textBrowser.append("????????? : " + dev_n_pub[0].string)
    if len(dev_n_pub) >= 2 :
        main_dialog.textBrowser.append("????????? : " + dev_n_pub[1].string)
    if price1 != None:
        price1_idx = find_price(price1.get_text())
        if price1_idx == -1:
            main_dialog.textBrowser.append("?????? : ??????")
        else:
            main_dialog.textBrowser.append("?????? : " + price1.get_text()[price1_idx:price1_idx+10])
        #main_dialog.textBrowser.append("?????? : " + str(price1))
    else:
        price2_idx = find_price(price2.get_text())
        if price2_idx == -1:
            main_dialog.textBrowser.append("?????? : ??????")
        else:
            main_dialog.textBrowser.append("?????? : " + price2.get_text()[price2_idx:price2_idx + 10])
        #main_dialog.textBrowser.append("?????? : " + str(price2))



def search(idx, category):
    headers = req.Request(
        "https://store.steampowered.com/contenthub/querypaginated/category/NewReleases/render/?query=&start={}&count=15&cc=KR&l=english&v=4&tag={}".format(
            idx, category), headers={"Accept-Language": "ko-KR"})
    code = req.urlopen(headers)
    soup = BeautifulSoup(code, "html.parser")

    # gama name
    game_name = str(soup).replace("/div", "</div>")
    soup1 = BeautifulSoup(game_name, "html.parser")
    trending_name = soup1.findAll('div', attrs={'class': "\\\"tab_item_name\\\""})

    # game url
    game_url = str(soup).replace("\\r", "</a>")
    soup2 = BeautifulSoup(game_url, "html.parser")
    trending_url = soup2.findAll('a')

    for i,k in zip(trending_name,trending_url):
        main_dialog.textBrowser.append("?????? ?????? : " + (i.string).replace("<\\", ""))
        tr_name.append((i.string).replace("<\\", ""))
        main_dialog.textBrowser.append("?????? url : " + k.get('href').replace("\\\"", ""))
        tr_url.append(k.get('href').replace("\\\"", ""))
        main_dialog.textBrowser.append("\n")

    main_dialog.textBrowser.append(" <== ?????? ?????? ????????? ????????? ?????? : " + str(len(tr_name)) + " ??? ( ??? ???????????? ?????? 15??? ) ===>\n")


ui_file = "./steam.ui"
class MainDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self,None)
        uic.loadUi(ui_file,self)
        self.initUI()
        self.setWindowTitle("?????? ?????? ????????? ?????? ??? ?????? ??????")

        self.pushButton.clicked.connect(self.btnclick)

    def btnclick(self):
        self.textBrowser.clear()
        global tr_name
        global tr_url

        tr_name = []
        tr_url = []

        game_cate_num = self.category_box.currentIndex()
        start_idx = self.startbox.currentIndex()
        end_idx = self.endbox.currentIndex()

        if start_idx > end_idx:
            self.textBrowser.setPlainText("????????? ?????? ??????")
        else:
            for i in range(start_idx,end_idx+1):
                search((i  * 15),game_category[game_cate_num + 1])

        if len(tr_name) >= 5:
            self.textBrowser.append("\n"+"\n"+"==============================================================" +
                                    "\n"+"\n" + " < ?????? ??? ????????? ??? ?????? ?????? ?????? > "+"\n"+"\n")
            random_list = random.sample(range(0, len(tr_name)), 5)
            for i in random_list:
                self.textBrowser.append("?????? ?????? : " + tr_name[int(i)])
                evalu(tr_url[int(i)])
                self.textBrowser.append("?????? url : " + tr_url[int(i)])
                self.textBrowser.append("\n")
                self.textBrowser.append("\n")

        else:
            self.textBrowser.append("?????? ?????? ?????? ??????")



    def initUI(self):
        self.category_box.setStyleSheet("QComboBox { combobox-popup: 0; font: 11pt;}")
        self.startbox.setStyleSheet("QComboBox { combobox-popup: 0; font: 11pt; }")
        self.endbox.setStyleSheet("QComboBox { combobox-popup: 0; font: 11pt; }")

        # 1:??????????????? 2:rpg , 3:?????? , 4:?????? ??????????????? 5:???????????? ??????: 6:????????? 7:?????? ??? ??????
        # 8 1?????? ?????? / 9 ???????????? ?????? / 10 3?????? ?????? / 11 ???????????? ????????? / 12 ???????????? / 13 ???????????? ????????? /
        # 14 ????????? / 15 ?????????????????? / 16 ?????? / 17 ????????? ????????? / 18 ????????? ?????? / 19 ?????? ????????? / 20 J?????????
        # 21 ?????? ?????? / 22 ?????? ???????????? / 23 ?????? / 24 ??????????????? / 25 ?????? ??? ????????? / 26 ?????? ??? ?????? / 27 ??????
        # 28 ?????? ??? ?????? / 29 ?????? ??? ????????? / 30 ???????????? ??? ?????? / 31 ?????? ??? ?????? / 32 ?????? / 33 ?????? ??? ??????
        # 34 ?????? ??? ?????? / 35 ????????? ??? 4X / 36 ?????? / 37 ????????? ?????? / 38 ?????? ????????? / 39 ?????? ?????? / 40 ????????? ??? ?????????
        # 41 ?????? ????????? / 42 ?????? ??? ?????? / 43 ?????? ????????? / 44 ????????? / 45 ????????? ??????????????? / 46 ????????? ???????????????
        # 47 ??? ?????????

        self.category_box.addItem("???????????????")
        self.category_box.addItem("????????????")
        self.category_box.addItem("??????")
        self.category_box.addItem("?????? ???????????????")
        self.category_box.addItem("???????????? ??????")
        self.category_box.addItem("?????????")
        self.category_box.addItem("?????? ??? ??????")
        self.category_box.addItem("1?????? ??????")
        self.category_box.addItem("???????????? ??????")
        self.category_box.addItem("3?????? ??????")
        self.category_box.addItem("???????????? ?????????")
        self.category_box.addItem("????????????")
        self.category_box.addItem("???????????? ?????????")
        self.category_box.addItem("?????????")
        self.category_box.addItem("??????????????????")
        self.category_box.addItem("??????")
        self.category_box.addItem("????????? ?????????")
        self.category_box.addItem("????????? ??????")
        self.category_box.addItem("?????? RPG")
        self.category_box.addItem("JRPG")
        self.category_box.addItem("?????? ??????")
        self.category_box.addItem("?????? ????????????")
        self.category_box.addItem("??????")
        self.category_box.addItem("???????????????")
        self.category_box.addItem("?????? ??? ?????????")
        self.category_box.addItem("?????? ??? ??????")
        self.category_box.addItem("??????")
        self.category_box.addItem("?????? ??? ??????")
        self.category_box.addItem("?????? ??? ?????????")
        self.category_box.addItem("???????????? ??? ??????")
        self.category_box.addItem("?????? ??? ??????")
        self.category_box.addItem("??????")
        self.category_box.addItem("?????? ??? ??????")
        self.category_box.addItem("?????? ??? ??????")
        self.category_box.addItem("????????? ??? 4X")
        self.category_box.addItem("??????")
        self.category_box.addItem("????????? ??????")
        self.category_box.addItem("?????? ?????????")
        self.category_box.addItem("?????? ??????")
        self.category_box.addItem("????????? ??? ?????????")
        self.category_box.addItem("?????? ?????????")
        self.category_box.addItem("?????? ??? ?????? ")
        self.category_box.addItem("?????? ?????????")
        self.category_box.addItem("?????????")
        self.category_box.addItem("????????? ???????????????")
        self.category_box.addItem("????????? ???????????????")
        self.category_box.addItem("??? ?????????")

        for i in range(1,101):
            self.startbox.addItem(str(i))

        for i in range(1,101):
            self.endbox.addItem(str(i))


QApplication.setStyle("fusion")
app = QApplication(sys.argv)
main_dialog = MainDialog()
main_dialog.show()
sys.exit(app.exec_())