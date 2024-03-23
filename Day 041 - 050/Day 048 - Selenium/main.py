from travian_manager import Travian
from ui_manager import MainWindow

if __name__ == "__main__":
    TRAVIAN = None
    TRAVIAN = Travian()
    ui = MainWindow()
    TRAVIAN.driver.quit()