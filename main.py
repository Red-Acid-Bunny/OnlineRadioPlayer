import sys
from PyQt5.Qt import QUrl, Qt
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QPushButton, QGridLayout, QLabel, QListWidget, QInputDialog, QFileDialog
import time
import requests

class Demo(QWidget):
    def __init__(self):
        super(Demo, self).__init__()
        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)        
        self.player.playlist().setPlaybackMode(QMediaPlaylist.Loop)

        self.Name = []
        self.listUrl = QListWidget()

        self.getUrlFromFile()
        
        self.volumeslider = QSlider(Qt.Horizontal)
        self.volumeslider.setFocusPolicy(Qt.NoFocus)
        self.volumeslider.valueChanged[int].connect(self.change_volume)
        self.volumeslider.setValue(30)
        self.volume = self.volumeslider.value()

        play_btn  = QPushButton('Play')   
        play_btn.clicked.connect(self.playMedia)
        pause_btn = QPushButton('Pause')  
        pause_btn.clicked.connect(self.pauseMedia)
        stop_btn  = QPushButton('Stop')   
        stop_btn.clicked.connect(self.stopMedia)
        next_btn  = QPushButton('Next')   
        next_btn.clicked.connect(self.nextMedia)
        prev_btn  = QPushButton('Prev')   
        prev_btn.clicked.connect(self.prevMedia)
        add_btn  = QPushButton('Add')   
        add_btn.clicked.connect(self.addMedia)
        save_btn  = QPushButton('Save')   
        save_btn.clicked.connect(self.saveMedia)
        load_btn  = QPushButton('Load')   
        load_btn.clicked.connect(self.loadMedia)
        
        self.label = QLabel(self)

        maxSize = 3
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 0, 1, maxSize)
        layout.addWidget(play_btn, 1, 0)
        layout.addWidget(pause_btn, 1, 1)
        layout.addWidget(stop_btn, 1, 2)
        layout.addWidget(prev_btn, 2, 0)
        layout.addWidget(next_btn, 2, 1)
        layout.addWidget(add_btn, 5, 0)
        layout.addWidget(load_btn, 5, 1)
        layout.addWidget(save_btn, 5, 2)
        layout.addWidget(self.volumeslider, 3, 0, 1, maxSize)
        
        self.updateListUrl()
        self.listUrl.itemClicked.connect(self.setTrack)
        layout.addWidget(self.listUrl, 4,0,1,maxSize)

        self.player.setVolume(self.volume)
        self.updateCurrenInfo()

    def change_volume(self, value):
        self.player.setVolume(value)

    def saveMedia(self):
        fname = QFileDialog.getOpenFileName(self, 'Save file', './')[0]
        f = open(fname, 'w')
        with f:
            playlist = self.playlist
            for i in range(len(self.Name)):
                f.write(self.Name[i]+'\n')
                t = playlist.media(i).canonicalUrl().toString()
                f.write(t+'\n')
        f.close()

    def loadMedia(self,fname):
        if fname==False:
            fname = QFileDialog.getOpenFileName(self, 'Open file', './')[0]
        temp = []
        f = open(fname, 'r')
        with f:
            for i in f:
                t = i 
                t = self.clearStr(t)
                if t!='':
                    temp.append(i[0:-1])
        f.close()
        self.stopMedia()
        self.Name = []
        self.listUrl.clear()
        self.playlist.clear()
        for i in range(0,len(temp),2):
            self.Name.append(temp[i])
            self.playlist.addMedia(
                    QMediaContent(QUrl(self.clearStr(temp[i+1]))))    
        self.updateListUrl()

    def addMedia(self):
        name, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter name:')
        print(name,ok)
        if ok==False:
            return 0
        link, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter link:')
        link = self.clearStr(link)
        print(link,ok)
        if ok==False:
            return 0
        self.Name.append(name)
        self.playlist.addMedia(QMediaContent(QUrl(link)))    
        self.updateListUrl()

    def playMedia(self):
        self.player.play()  
        self.updateCurrenInfo()

    def pauseMedia(self):
        self.player.pause()        
    
    def nextMedia(self):
        self.player.playlist().next()
        self.updateCurrenInfo()

    def prevMedia(self):
        self.player.playlist().previous()    
        self.updateCurrenInfo()

    def stopMedia(self):
        self.player.stop()  

    def updateCurrenInfo(self):
        Index = int(self.playlist.currentIndex())
        if Index < self.playlist.mediaCount():
            if Index > -1:
                self.label.setText(self.Name[Index])

    def clearStr(self,s :str):
        return s.replace(' ','').replace('\t','').replace('\n','')

    def getUrlFromFile(self):
        self.loadMedia("url.txt")

    def updateListUrl(self):
        self.listUrl.clear()
        for i in range(len(self.Name)):
            self.listUrl.addItem(self.Name[i])
            

    def setTrack(self, item):
        name = item.text()
        for i in range(len(self.Name)):
            if name == self.Name[i]:
                self.player.playlist().setCurrentIndex(i)
                break
        self.updateCurrenInfo()
        self.player.play()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo()
    demo.show()
    sys.exit(app.exec_())
