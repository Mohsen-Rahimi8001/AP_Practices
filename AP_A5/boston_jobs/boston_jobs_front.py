from PyQt5 import QtCore, QtGui, QtWidgets
import boston_jobs_back as fns


class Ui_MainWindow(object):
    def __init__(self):
        self.result_links = []

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 560)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 761, 521))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.main_layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setObjectName("main_layout")
        self.le_search = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.le_search.setObjectName("le_search")
        self.main_layout.addWidget(self.le_search)

        self.btn_layout = QtWidgets.QHBoxLayout()
        self.btn_layout.setObjectName("btn_layout")

        self.btn_search = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_search.setObjectName("btn_search")
        self.btn_layout.addWidget(self.btn_search)
        self.btn_search.clicked.connect(self.search)

        self.btn_clear = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_clear.setObjectName("btn_clear")
        self.btn_clear.clicked.connect(self.clear_page)

        self.btn_layout.addWidget(self.btn_clear)
        self.main_layout.addLayout(self.btn_layout)
        self.lstw_jobs = QtWidgets.QListWidget(self.verticalLayoutWidget)
        self.lstw_jobs.setObjectName("lstw_jobs")
        self.lstw_jobs.itemClicked.connect(lambda job:self.show_information_of_job(job))

        self.main_layout.addWidget(self.lstw_jobs)
        MainWindow.setCentralWidget(self.centralwidget)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_information_of_job(self, job):
        """Gets the information of the selected job"""
        index = int(job.text()[0])
        info = fns.get_description(self.result_links[index-1])
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'Job Info', "\n\n".join(info)).exec()


    def clear_page(self):
        """Clears the page"""
        self.lstw_jobs.clear()
        self.le_search.clear()

    def search(self):
        """Search for what is in le_search"""
        query = self.le_search.text()
        query = "+".join(query.strip().split())
        self.lstw_jobs.clear()
        results = fns.get_search_results(query)

        for i, result in enumerate(results):
            QtWidgets.QListWidgetItem(f"{i+1}-{result[0]}", self.lstw_jobs)
            self.result_links.append(result[1])
        # Show success message
        QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information, 'Success', 'Search is done.').exec()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Boston Jobs"))
        self.btn_search.setText(_translate("MainWindow", "Click to Search"))
        self.btn_clear.setText(_translate("MainWindow", "Clear Results"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
