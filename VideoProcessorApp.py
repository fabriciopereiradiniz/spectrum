from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox, QWidget, QLabel, QProgressBar
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from moviepy.editor import *
import pydub.silence as pydub_silence
from pydub import AudioSegment
from VideoProcessor import VideoProcessor
import os
import sys

class VideoProcessorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.input_video_path = None
        self.output_video_path = None
        self.OUTPUT_AUDIO_FILE = "extracted_audio.wav"

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowTitle("")
        self.setGeometry(100, 100, 1280, 720)

        background_image = QPixmap("images/background.png")

        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        background_label.setGeometry(0, 0, self.width(), self.height())

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        self.close_button = QPushButton("X", self)
        self.close_button.setStyleSheet('''
            QPushButton {
                background-image: url(images/select.png);
                background-color: transparent;
                color: #f3f1fd;
                padding: 5px 5px;
                text-align: center;
                text-decoration: none;
                display: center;
                font-size: 23px;
                margin: 0px 0px;
                cursor: pointer;
                border-radius: 15px;
            }
        ''')
        self.close_button.setGeometry(1150, 20, 100, 30)
        self.close_button.clicked.connect(self.close)

        self.select_input_button = QPushButton("", self)
        self.select_input_button.setGeometry(440, 150, 400, 100)
        self.select_input_button.setStyleSheet('''
            QPushButton {
                background-image: url(images/select.png);
                background-color: transparent;
                color: #f3f1fd;
                padding: 5px 5px;
                text-align: center;
                text-decoration: none;
                display: center;
                font-size: 23px;
                margin: 0px 0px;
                cursor: pointer;
                border-radius: 15px;
            }
        ''')
        self.select_input_button.clicked.connect(self.select_input_video)

        self.select_output_button = QPushButton("", self)
        self.select_output_button.setGeometry(440, 300, 400, 100)
        self.select_output_button.setStyleSheet('''
            QPushButton {
                background-image: url(images/save.png);
                background-color: transparent;
                color: #f3f1fd;
                padding: 5px 5px;
                text-align: center;
                text-decoration: none;
                display: center;
                font-size: 23px;
                margin: 0px 0px;
                cursor: pointer;
                border-radius: 15px;
            }
        ''')
        self.select_output_button.clicked.connect(self.select_output_location)

        self.process_button = QPushButton("", self)
        self.process_button.setGeometry(540, 450, 200, 50)
        self.process_button.setStyleSheet('''
            QPushButton {
                background-image: url(images/start.png);
                background-color: transparent;
                color: #f3f1fd;
                padding: 5px 5px;
                text-align: center;
                text-decoration: none;
                display: center;
                font-size: 23px;
                margin: 0px 0px;
                cursor: pointer;
                border-radius: 15px;
            }
        ''')
        self.process_button.clicked.connect(self.process_video)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(440, 520, 400, 30)
        self.progress_bar.setVisible(False)
        self.progress_bar.setFormat(" ")
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                background-color: #f7f7f6;
            
                border-radius: 13px;
                text-align: center; /* Centraliza o texto */
            }
            QProgressBar::chunk {
                background-color: #dfe8ec; /* Cor azul para o carregamento */
                border-radius: 15px;
            }
        ''')

        self.progress_bar.setAlignment(Qt.AlignCenter)

    def select_input_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Video Files (*.mp4 *.avi *.mov)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.input_video_path = selected_files[0]

    def select_output_location(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = QFileDialog()
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("mp4")
        file_dialog.setNameFilter("MP4 Files (*.mp4)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                self.output_video_path = selected_files[0]

    def process_video(self):
        if self.input_video_path and self.output_video_path:
            try:
                self.progress_bar.setVisible(True)
                self.progress_bar.setValue(0)  

                print(f"Vídeo de entrada: {self.input_video_path}")
                print(f"Vídeo de saída: {self.output_video_path}")

                video_processor = VideoProcessor(self.input_video_path)
                video_processor.extract_audio()
                
                self.progress_bar.setValue(50)

                video_processor.remove_silence_segments(self.output_video_path)

                self.progress_bar.setValue(100)

                QMessageBox.information(self, "Processamento Concluído", "O vídeo foi processado com sucesso!")

            except Exception as e:
                print(f"Erro durante o processamento do vídeo: {str(e)}")
            finally:
                self.progress_bar.setVisible(False)

                if os.path.exists(self.OUTPUT_AUDIO_FILE):
                    os.remove(self.OUTPUT_AUDIO_FILE)