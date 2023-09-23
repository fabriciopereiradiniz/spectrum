from VideoProcessorApp import *

app = QApplication(sys.argv)
window = VideoProcessorApp()
window.setGeometry(100, 100, 1280, 720)
window.show()
sys.exit(app.exec_())   