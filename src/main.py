import sys
import numpy as np
import pandas as pd
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QHBoxLayout, QPushButton, QLabel, QFileDialog,
                               QMessageBox)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
  def __init__(self):
    super().__init__()
    self.setWindowTitle("Watchlist Generator")
    self.titles = None

    # UI
    self.open_btn = QPushButton("Open CSV ...")
    self.gen_btn = QPushButton("Generate")
    self.gen_btn.setEnabled(False)

    self.file_label = QLabel("No file selected")
    self.file_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
    self.count_label = QLabel("0 titles")
    self.result_label = QLabel("-")
    self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    self.result_label.setStyleSheet("font-size: 22px;")

    top = QHBoxLayout()
    top.addWidget(self.open_btn)
    top.addWidget(self.gen_btn)

    layout = QVBoxLayout()
    layout.addLayout(top)
    layout.addWidget(self.file_label)
    layout.addWidget(self.count_label)
    layout.addWidget(self.result_label)

    container = QWidget()
    container.setLayout(layout)
    self.setCentralWidget(container)

    # Signals
    self.open_btn.clicked.connect(self.open_csv)
    self.gen_btn.clicked.connect(self.generate)

  def open_csv(self):
    path, _ = QFileDialog.getOpenFileName(self, "Select watchlist CSV",
                                          "", "CSV Files (*.csv)")
    if not path:
      return
    try:
      df = pd.read_csv(path)
    except Exception as e:
      self._err(f"Failed to read CSV: {e}")
      return

    col = None
    # Prefer IMDb export column name
    if "Title" in df.columns:
      col = "Title"
    else:
      for c in df.columns:
        if df[c].dtype == object:
          col = c
          break

    if not col:
      self._err("No text column found. Expected a Title column.")
      return

    vals = df[col].dropna().astype(str).str.strip()
    vals = vals[vals != ""]
    if vals.empty:
      self._err("No non-empty titles found.")
      return

    self.titles = vals.to_numpy()
    self.file_label.setText(f"Loaded: {path}")
    self.count_label.setText(f"{len(self.titles)} titles")
    self.gen_btn.setEnabled(True)

  def generate(self):
    if self.titles is None or len(self.titles) == 0:
      self._err("Load a CSV first.")
      return
    choice = np.random.default_rng().choice(self.titles)
    self.result_label.setText(choice)

  def _err(self, msg):
    QMessageBox.critical(self, "Error", msg)

def main():
  app = QApplication(sys.argv)
  window = MainWindow()
  window.resize(520, 220)
  window.show()
  sys.exit(app.exec())

if __name__ == "__main__":
  main()
