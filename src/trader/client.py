import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyStock")
        self.setGeometry(300, 300, 600, 300)

        self.kiwoom = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")

        btn1 = QPushButton("Login", self)
        btn1.move(20, 20)
        btn1.clicked.connect(self.btn1_clicked)

        btn2 = QPushButton("Check state", self)
        btn2.move(20, 70)
        btn2.clicked.connect(self.btn2_clicked)

        btn3 = QPushButton("Run", self)
        btn3.move(180, 45)
        btn3.clicked.connect(self.btn3_clicked)

        self.text_edit = QTextEdit(self)
        self.text_edit.setGeometry(20, 120, 560, 160)
        self.text_edit.setEnabled(False)

        self.kiwoom.OnReceiveChejanData.connect(self.OnReceiveChejanData)
        self.kiwoom.OnReceiveMsg.connect(self.OnReceiveMsg)

    def btn1_clicked(self):
        ret = self.kiwoom.dynamicCall("CommConnect()")
        self.kiwoom.OnEventConnect.connect(self.OnEventConnect)
        self.log("CommConnect() returns: " + str(ret))

    def btn2_clicked(self):
        ret = self.kiwoom.dynamicCall("GetConnectState()")
        self.log("GetConnectStates() return: " + str(ret) + " (0 means NOT CONNECTED)")

        account_num = int(self.kiwoom.dynamicCall("GetLoginInfo(QString)", ["ACCNO"]).rstrip(";"))
        self.log("계좌번호: " + str(account_num))

    def btn3_clicked(self):
        #self.kiwoom.dynamicCall("CommRqData()")

        try:
            result = self.kiwoom.SendOrder("RQ1", "0220", "8085069711", 2, "122630", 123, 11000, "00", "")
            #result = self.kiwoom.dynamicCall("SendOrderFO(QString, QString, QString, int, QString, int, int, QString, QString)",
            #                             ["abc", "0220", "8085069711", 1, "122630", 123, 11000, "7", ""])
            self.log(str(result))
        except Exception as e:
            self.log(str(e))


        # SendOrder(
        #   BSTR sRQName, // 사용자 구분명
        #   BSTR sScreenNo, // 화면번호
        #   BSTR sAccNo,  // 계좌번호 10자리
        #   LONG nOrderType,  // 주문유형 1:신규매수, 2:신규매도 3:매수취소, 4:매도취소, 5:매수정정, 6:매도정정
        #   BSTR sCode, // 종목코드 // 122630
        #   LONG nQty,  // 주문수량 // 123
        #   LONG nPrice, // 주문가격 // 11000
        #   BSTR sHogaGb,   // 거래구분(혹은 호가구분)은 아래 참고 // 1
        #   BSTR sOrgOrderNo  // 원주문번호입니다. 신규주문에는 공백, 정정(취소)주문할 원주문번호를 입력합니다.
        #   )

    def log(self, str):
        self.text_edit.append(str)


    def OnEventConnect(self, ErrCode):
        self.log("OnEventConnect() called back with ErrCode: " + str(ErrCode))

    def OnReceiveChejanData(self, sGubun, nItemCnt, sFIDList):
        print("OnReceiveChejanData()")
        order_num = self.kiwoom.GetChejanData(302)
        order_vol = self.kiwoom.GetChejanData(900)
        order_price = self.kiwoom.GetChejanData(901)
        print("주문번호 : {}, 주문수량 : {}, 주문가격 : {}".format(order_num.strip(), order_vol, order_price))

    def OnReceiveMsg(self, sScrNo, sRQName, sTrCode, sMsg):
        print("OnReceiveMsg::sMsg:{}".format(sMsg))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
