import os, json, requests, subprocess, pkg_resources, sys, atexit
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QInputDialog, QAction, QMenu, QSystemTrayIcon
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTimer
local_app_data = os.getenv('LOCALAPPDATA')
roblox_versions_path = os.path.join(local_app_data, 'Roblox', 'Versions')
fps_options = ["10", "15", "30", "60", "100", "120", "144", "165", "240", "360", "unlimited", "custom"] // bleh rahh uwu
class FPSDialog(QWidget):
    def restart(self):
        """Restart the application."""
        self.close()
        self.showDialog()
    def __init__(self):
        super().__init__()
        self.icon_path = os.path.join(local_app_data, 'pyfpsunlocker', 'icon.ico')
        self.downloadIcon()
        self.tray_icon = None
        self.initUI()
    def downloadIcon(self):
        os.makedirs(os.path.dirname(self.icon_path), exist_ok=True)
        response = requests.get('https://raw.githubusercontent.com/hiimnotyou/pyfpsunlock/main/icon.ico')
        with open(self.icon_path, 'wb') as file:
            file.write(response.content)
    def initUI(self):
        self.setWindowTitle('FPS Unlocker')
        if self.tray_icon is None:
            self.createTrayIcon()
        else:
            self.tray_icon.show()
    def createTrayIcon(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon(self.icon_path))
        quit_action = QAction("Exit", self)
        edit_action = QAction("Edit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        edit_action.triggered.connect(self.restart)
        tray_menu = QMenu()
        tray_menu.addAction(edit_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()
        self.showDialog()
    def show(self):
        super().show()
        QTimer.singleShot(1, self.hide)
    def showDialog(self):
        fps, ok = QInputDialog.getItem(self, 'Input FPS', 'Enter the target FPS:', fps_options, 0, False)
        if ok and fps:
            if fps == "unlimited":
                fps = 10000
            elif fps == "custom":
                fps, ok = QInputDialog.getInt(self, 'Custom FPS', 'Enter a custom FPS value:')
                if not ok:
                    return
                fps = int(fps)
            else:
                fps = int(fps)
            self.updateFPS(fps)
        self.show()
    def updateFPS(self, fps):
        if os.path.exists(roblox_versions_path):
            for folder in os.listdir(roblox_versions_path):
                folder_path = os.path.join(roblox_versions_path, folder)
                if os.path.isdir(folder_path):
                    if 'RobloxPlayerBeta.dll' in os.listdir(folder_path):
                        print(f"Found RobloxPlayerBeta.dll in {folder_path}")
                        client_settings_path = os.path.join(folder_path, 'ClientSettings')
                        os.makedirs(client_settings_path, exist_ok=True)
                        client_app_settings_path = os.path.join(client_settings_path, 'ClientAppSettings.json')
                        with open(client_app_settings_path, 'w') as file:
                            json.dump({"DFIntTaskSchedulerTargetFps": fps}, file)
        else:
            print("Roblox folder does not exist.")
if __name__ == "__main__":
    app = QApplication([])
    ex = FPSDialog()
    atexit.register(ex.updateFPS, 60)
    sys.exit(app.exec_())
