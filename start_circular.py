from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QMainWindow

from circular.circular import Ui_CircularBar
import sys

# GLOBAL

progress_count = 0


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_CircularBar()
        self.ui.setupUi(self)
        # suppression de la barre des titres
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # effet ombrage

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(10)
        self.shadow.setXOffset(2)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor(0, 0, 0, 220))
        self.ui.frame.setGraphicsEffect(self.shadow)

        # QTIMER => START
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_progressbar)
        self.timer.start(100)
        self.angle = 90
        self.color = "rgba(85, 170, 255, 255)"  # bleu
        # self.color = "rgba(255, 70, 255, 255)"  # magenta
        # self.color = "rgba(15, 255, 21, 255)"  # vert
        # self.color = "rgba(245, 12, 5, 255)"  # rouge

        self.progress_value(0)
        self.progress_title()

    def progress_title(self, title="CPU", subtitle="USAGE"):
        self.title = title
        self.subtitle = subtitle

        style = """<span style=" font-size:11pt; font-weight:600; color:#aaaaff;">{MAIN}</span><span style=" font-size:11pt;"> {SUB}</span>"""
        text = style.replace("{MAIN}", self.title).replace("{SUB}", self.subtitle)
        self.ui.label_name.setText(text)

    def progress_color(self, color):
        self.color = color
        self.newstyle = self.newstyle.replace("{color}", self.color)
        self.ui.circularProgress.setStyleSheet(self.newstyle)

    def progress_angle(self, angle):
        self.angle = angle

    def progress_value(self, value):

        stylesheet = """
        QFrame{
        border-radius:150px;
        background-color: qconicalgradient(cx:0.5, cy:0.5, angle:{angle},stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} {color});
        }
        """

        text_value = """<span style=" font-size:56pt;color:#ffffff;">{VALUE}</span><span style=" font-size:48pt;vertical-align:super;">%</span> """
        if value > 100:
            value = 100

        progress = (100 - value) / 100.0
        stop1 = progress - 0.001
        stop2 = progress

        self.newstyle = stylesheet.replace("{STOP_1}", str(stop1)).replace("{STOP_2}", str(stop2)).replace("{angle}",
                                                                                                           str(self.angle))
        self.newstyle = self.newstyle.replace("{color}", self.color)
        self.ui.circularProgress.setStyleSheet(self.newstyle)

        newtextstyle = text_value.replace("{VALUE}", str(value))
        self.ui.label_value.setText(newtextstyle)

    def update_progressbar(self):
        global progress_count

        self.progress_value(progress_count)
        if progress_count == 20:
            self.ui.label_description.setText("modules ...")

        if progress_count == 30:
            self.ui.label_description.setText("en cours ...")

        if progress_count > 100:
            self.timer.stop()
            self.close()

        progress_count += 1


def main():
    app = QtWidgets.QApplication(sys.argv)
    application = SplashScreen()
    application.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
