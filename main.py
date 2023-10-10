"""A module that provides functions for accessing command line arguments"""
import sys

import PyQt5
import PyQt5.Qt
import PyQt5.QtMultimedia
import PyQt5.QtWidgets


DEFAULT_DATA_PATH = "./url.txt"

class OnlineRadioPlayer(PyQt5.QtWidgets.QWidget):
    """Main class"""
    def __init__(self):
        super().__init__()
        self.player = PyQt5.QtMultimedia.QMediaPlayer(self)
        self.playlist = PyQt5.QtMultimedia.QMediaPlaylist()
        self.player.setPlaylist(self.playlist)
        self.player.playlist().setPlaybackMode(
                PyQt5.QtMultimedia.QMediaPlaylist.Loop
                )

        self.names_of_radio_stations = []
        self.links_to_radio_stations = PyQt5.QtWidgets.QListWidget()

        self.load_media(DEFAULT_DATA_PATH)
        self.update_links_to_radio_stantions()
        self.update_name_of_the_current_station()

        # Volume
        self.volume_slider = PyQt5.QtWidgets.QSlider(PyQt5.Qt.Qt.Horizontal)
        self.volume_slider.setFocusPolicy(PyQt5.Qt.Qt.NoFocus)
        self.volume_slider.valueChanged.connect(self.change_volume)
        self.volume_slider.setValue(30)
        self.volume = self.volume_slider.value()
        self.player.setVolume(self.volume)

        # Buttons
        play_btn = PyQt5.QtWidgets.QPushButton('Play')
        play_btn.clicked.connect(self.play_media)

        pause_btn = PyQt5.QtWidgets.QPushButton('Pause')
        pause_btn.clicked.connect(self.pause_media)

        stop_btn = PyQt5.QtWidgets.QPushButton('Stop')
        stop_btn.clicked.connect(self.stop_media)

        next_btn = PyQt5.QtWidgets.QPushButton('Next')
        next_btn.clicked.connect(self.next_media)

        prev_btn = PyQt5.QtWidgets.QPushButton('Prev')
        prev_btn.clicked.connect(self.prev_media)

        add_btn = PyQt5.QtWidgets.QPushButton('Add')
        add_btn.clicked.connect(self.add_media)

        save_btn = PyQt5.QtWidgets.QPushButton('Save')
        save_btn.clicked.connect(self.save_media)

        load_btn  = PyQt5.QtWidgets.QPushButton('Load')
        load_btn.clicked.connect(self.load_media)

        # List names of radio station
        self.links_to_radio_stations.itemClicked.connect(self.set_track)

        # Labels
        self.name_of_the_current_station = PyQt5.QtWidgets.QLabel(self)

        # Ui
        max_size = 3

        layout = PyQt5.QtWidgets.QGridLayout(self)

        layout.addWidget(self.name_of_the_current_station, 0, 0, 1, max_size)

        layout.addWidget(play_btn, 1, 0)
        layout.addWidget(pause_btn, 1, 1)
        layout.addWidget(stop_btn, 1, 2)

        layout.addWidget(prev_btn, 2, 0)
        layout.addWidget(next_btn, 2, 1)

        layout.addWidget(self.volume_slider, 3, 0, 1, max_size)

        layout.addWidget(self.links_to_radio_stations, 4,0,1,max_size)

        layout.addWidget(add_btn, 5, 0)
        layout.addWidget(load_btn, 5, 1)
        layout.addWidget(save_btn, 5, 2)

    def change_volume(self, value):
        """ change volume """
        self.player.setVolume(value)

    def save_media(self):
        """ Save """
        file_path = PyQt5.QtWidgets.QFileDialog.getOpenFileName(
                self, 'Save file', './'
                )[0]
        with open(file_path, encoding="utf-8") as file:
            playlist = self.playlist
            for i, name in enumerate(self.names_of_radio_stations):
                file.write(name + '\n')
                temp = playlist.media(i).canonicalUrl().toString()
                file.write(temp + '\n')
        file.close()

    def load_media(self,file_path):
        """ Load """
        if not file_path:
            file_path = PyQt5.QtWidgets.QFileDialog.getOpenFileName(
                    self, 'Open file', './'
                    )[0]

        temp_names_of_radio_stations = []

        data = []
        with open(file_path, encoding="utf-8") as file:
            for line in file:
                temp = line
                temp = self.clear_str(temp)
                if temp!='':
                    data.append(line)
        file.close()
        p = 0
        for i, string in enumerate(data):
            if (i+p)%2 == 0:
                temp_names_of_radio_stations.append(["No name","No url"])
                if (string.find("https://", 0, 8) == -1 and
                        string.find("http://", 0, 7) == -1):
                    temp_names_of_radio_stations[-1][0] = string[0:-1]
                else:
                    temp_names_of_radio_stations[-1][1] = string[0:-1]
                    if p == 0:
                        p = 1
                    else:
                        p = 0
            else:
                if (string.find("https://", 0, 8) == -1 and
                        string.find("http://", 0, 7) == -1):
                    temp_names_of_radio_stations[-1][0] = string[0:-1]
                    if p == 0:
                        p = 1
                    else:
                        p = 0
                else:
                    temp_names_of_radio_stations[-1][1] = string[0:-1]


        for i, obj in enumerate(temp_names_of_radio_stations):
            if obj[1] == "No url":
                temp_names_of_radio_stations.pop(i)


        self.stop_media()

        # Clear
        self.names_of_radio_stations = []
        self.links_to_radio_stations.clear()
        self.playlist.clear()

        for i in temp_names_of_radio_stations:
            self.names_of_radio_stations.append(i[0])
            self.playlist.addMedia(
                    PyQt5.QtMultimedia.QMediaContent(
                        PyQt5.Qt.QUrl(self.clear_str(i[1]))
                        )
                    )
        self.update_links_to_radio_stantions()

    def add_media(self):
        """ Add radio station """
        radio_station_name, status = PyQt5.QtWidgets.QInputDialog.getText(
                self, 'Input Dialog', 'Enter the name of the radio station:'
                )

        if not status:
            return False

        link_to_the_radio_station, status = PyQt5.QtWidgets.QInputDialog.getText(
                self, 'Input Dialog', 'Enter the link to the radio station:'
                )

        link_to_the_radio_station = self.clear_str(link_to_the_radio_station)

        if not status:
            return False

        self.names_of_radio_stations.append(radio_station_name)
        self.playlist.add_media(
                PyQt5.QtMultimedia.QMediaContent(
                    PyQt5.Qt.QUrl(link_to_the_radio_station)
                    )
                )
        self.update_links_to_radio_stantions()
        return True

    def play_media(self):
        """ Play """
        self.player.play()
        self.update_name_of_the_current_station()

    def pause_media(self):
        """ Pause """
        self.player.pause()

    def stop_media(self):
        """ Stop """
        self.player.stop()
        self.update_name_of_the_current_station(True)

    def next_media(self):
        """ Next station """

        self.player.playlist().next()
        self.update_name_of_the_current_station()

    def prev_media(self):
        """ Previous station """
        self.player.playlist().previous()
        self.update_name_of_the_current_station()

    def update_name_of_the_current_station(self, clean = False):
        """ Update names of radio stations """
        index = int(self.playlist.currentIndex())
        if index < self.playlist.mediaCount():
            if index > -1:
                if clean:
                    self.name_of_the_current_station.setText(
                            ""
                            )
                else:
                    self.name_of_the_current_station.setText(
                            self.names_of_radio_stations[index]
                            )

    def clear_str(self,s :str):
        """ Remove insignificant characters """
        return s.replace(' ','').replace('\t','').replace('\n','')

    def update_links_to_radio_stantions(self):
        """ Update links to radio stantions """
        self.links_to_radio_stations.clear()
        for name in self.names_of_radio_stations:
            self.links_to_radio_stations.addItem(name)

    def set_track(self, radio_station_name):
        """ Set track """
        for i, name in enumerate(self.names_of_radio_stations):
            if radio_station_name.text() == name:
                self.player.playlist().setCurrentIndex(i)
                break
        self.update_name_of_the_current_station()
        self.player.play()


if __name__ == '__main__':
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    demo = OnlineRadioPlayer()
    demo.show()
    sys.exit(app.exec_())
