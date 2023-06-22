import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
import os

class DnsChanger(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Create labels and text fields for DNS IP input
        self.ip1_label = QLabel('DNS IP 1:', self)
        self.ip1_edit = QLineEdit(self)
        self.ip2_label = QLabel('DNS IP 2:', self)
        self.ip2_edit = QLineEdit(self)

        # Create preset buttons
        self.shecan_btn = QPushButton('Shecan', self)
        self.shecan_btn.clicked.connect(self.shecan_preset)

        # Create button to save and apply changes
        self.save_btn = QPushButton('Save', self)
        self.save_btn.clicked.connect(self.save_dns)

        # Create button to restore backup file
        self.restore_btn = QPushButton('Restore', self)
        self.restore_btn.clicked.connect(self.restore_dns)

        # Create vertical layout
        vbox = QVBoxLayout()
        vbox.addWidget(self.ip1_label)
        vbox.addWidget(self.ip1_edit)
        vbox.addWidget(self.ip2_label)
        vbox.addWidget(self.ip2_edit)
        vbox.addWidget(self.shecan_btn)
        vbox.addWidget(self.save_btn)
        vbox.addWidget(self.restore_btn)
        self.setLayout(vbox)

        self.setWindowTitle('BSS DNS Changer')
        self.show()

    def shecan_preset(self):
        # Pre-fill Shecan DNS servers
        self.ip1_edit.setText('178.22.122.100')
        self.ip2_edit.setText('185.51.200.2')

    def save_dns(self):
        # Check root privileges
        if os.geteuid() != 0:
            self.show_error('This operation requires root privileges.')
            return

        # Get DNS IP inputs from user
        ip1 = self.ip1_edit.text()
        ip2 = self.ip2_edit.text()

        # Write to resolv.conf file
        with open('resolv.conf', 'w') as f:
            f.write(f'nameserver {ip1}\n')
            f.write(f'nameserver {ip2}\n')

        # Backup existing resolv.conf file
        os.rename('/etc/resolv.conf', '/etc/resolv.conf.bak')

        # Replace existing resolv.conf with new file
        os.rename('resolv.conf', '/etc/resolv.conf')

    def restore_dns(self):
        # Check root privileges
        if os.geteuid() != 0:
            self.show_error('This operation requires root privileges.')
            return

        # Restore backup file
        os.rename('/etc/resolv.conf.bak', '/etc/resolv.conf')

    def show_error(self, message):
        # Show error message in a dialog box
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Warning)
        error_dialog.setText(message)
        error_dialog.setWindowTitle('Error')
        error_dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DnsChanger()
    sys.exit(app.exec_())

