from PyQt5 import QtCore, QtGui, QtWidgets
from main_back import Instagram
import sys
import os
import time


class Ui_MainWindow(object):
    def __init__(self, instagram_object:Instagram):
        self.insta = instagram_object

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(781, 598)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 761, 551))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_ID = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_ID.setObjectName("lbl_ID")
        self.verticalLayout.addWidget(self.lbl_ID)
        self.lbl_profilePic = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_profilePic.setObjectName("lbl_profilePic")
        self.verticalLayout.addWidget(self.lbl_profilePic)
        self.lbl_followers = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_followers.setObjectName("lbl_followers")
        self.verticalLayout.addWidget(self.lbl_followers)
        self.lbl_followings = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_followings.setObjectName("lbl_followings")
        self.verticalLayout.addWidget(self.lbl_followings)
        self.lbl_post_count = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_post_count.setObjectName("lbl_post_count")
        self.verticalLayout.addWidget(self.lbl_post_count)
        self.lbl_bio = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_bio.setObjectName("lbl_bio")
        self.verticalLayout.addWidget(self.lbl_bio)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.lbl_directTo = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_directTo.setObjectName("lbl_directTo")
        self.verticalLayout_2.addWidget(self.lbl_directTo)
        self.le_directTo = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.le_directTo.setObjectName("le_directTo")
        self.le_directTo.setPlaceholderText('To ...')
        self.verticalLayout_2.addWidget(self.le_directTo)
        self.te_directText = QtWidgets.QTextEdit(self.horizontalLayoutWidget)
        self.te_directText.setObjectName("te_directText")
        self.te_directText.setPlaceholderText('Message ...')
        self.verticalLayout_2.addWidget(self.te_directText)
        self.btn_sendDirect = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_sendDirect.setObjectName("btn_sendDirect")
        self.btn_sendDirect.clicked.connect(self.send_direct)
        self.verticalLayout_2.addWidget(self.btn_sendDirect)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.lbl_name = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_name.setObjectName("lbl_name")
        self.verticalLayout_12.addWidget(self.lbl_name)
        self.lbl_studentID = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_studentID.setObjectName("lbl_studentID")
        self.verticalLayout_12.addWidget(self.lbl_studentID)
        self.verticalLayout_5.addLayout(self.verticalLayout_12)
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.lbl_downloadStories = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.lbl_downloadStories.setObjectName("lbl_downloadStories")
        self.verticalLayout_11.addWidget(self.lbl_downloadStories)
        self.le_download_stories_from = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.le_download_stories_from.setObjectName("le_download_stories_from")
        self.le_download_stories_from.setPlaceholderText("Enter the id ...")
        self.verticalLayout_11.addWidget(self.le_download_stories_from)
        self.le_directoryToSaveStory = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.le_directoryToSaveStory.setObjectName("le_directoryToSaveStory")
        self.le_directoryToSaveStory.setPlaceholderText('Save to ...')
        self.verticalLayout_11.addWidget(self.le_directoryToSaveStory)
        self.btn_download = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.btn_download.setObjectName("btn_download")
        self.btn_download.clicked.connect(self.download_stories)
        self.verticalLayout_11.addWidget(self.btn_download)
        self.verticalLayout_5.addLayout(self.verticalLayout_11)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def download_stories(self):
        save_to = self.le_directoryToSaveStory.text()
        if os.path.exists(save_to):
            target_page_id = self.le_download_stories_from.text()
            if target_page_id:
                images = self.insta.get_stories(target_page_id)
                for i, image in enumerate(images):
                    if image:
                        with open(save_to + f'\\story-{i}.jpg', "wb") as f:
                            f.write(image)
                        print(f'story-{i} Saved')

    def send_direct(self):
        to = self.le_directTo.text()
        message = self.te_directText.toPlainText()
        if to != '' and message != '':
            self.insta.send_direct(message, to)

    def setup_init_information(self):
        """Sets up the initial information of the main page."""
        self.set_profile(self.insta.get_profile_pic())
        self.set_id(self.insta.ID)

        info = self.insta.get_info()
        bio = self.insta.get_bio()

        # [posts, followers, followings]
        self.set_post_count(info[0])
        self.set_followers(info[1])
        self.set_followings(info[2])

        self.set_bio(bio)

    def set_id(self, id:str):
        """Set the id label"""
        self.lbl_ID.setText(id)

    def set_profile(self, profile_binary:bytes):
        """Set the profile picture"""
        if not profile_binary:
            return
        profile_pic = QtGui.QPixmap()
        profile_pic.loadFromData(profile_binary)
        self.lbl_profilePic.setPixmap(profile_pic)
    
    def set_followers(self, followers:str):
        """Set the followers label"""
        self.lbl_followers.setText("Followers: " + followers)

    def set_followings(self, followings:str):
        """Set the followings label"""
        self.lbl_followings.setText("Followings: " + followings)

    def set_post_count(self, post_count:str):
        """Set the post count label"""
        self.lbl_post_count.setText("Posts: " + post_count)

    def set_bio(self, bio:str):
        """Set the bio label"""
        self.lbl_bio.setText(bio)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_ID.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_profilePic.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_followers.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_followings.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_post_count.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_bio.setText(_translate("MainWindow", "TextLabel"))
        self.lbl_directTo.setText(_translate("MainWindow", "Direct Message"))
        self.btn_sendDirect.setText(_translate("MainWindow", "Send"))
        self.lbl_name.setText(_translate("MainWindow", "Full Name: Mohsen Rahimi"))
        self.lbl_studentID.setText(_translate("MainWindow", "Student ID: 99412042"))
        self.lbl_downloadStories.setText(_translate("MainWindow", "Download Stories"))
        self.btn_download.setText(_translate("MainWindow", "Download"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")

    insta = Instagram(username, username, password)
    insta.get_instagram()
    insta.login()
    insta.not_now_button()
    insta.another_not_now_button()
    time.sleep(3)
    insta.go_to_our_page()

    ui = Ui_MainWindow(insta)
    ui.setupUi(MainWindow)
    ui.setup_init_information()

    MainWindow.show()
    sys.exit(app.exec_())
