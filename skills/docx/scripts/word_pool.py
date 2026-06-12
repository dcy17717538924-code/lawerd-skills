import win32com.client
import threading


class WordPool:
    """常驻 Word.Application 实例 + 死了自动重启。极简版。"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._word = None
        return cls._instance

    def get(self):
        if self._word is None or not self._is_alive():
            self._word = win32com.client.DispatchEx("Word.Application")
            self._word.Visible = False
            self._word.DisplayAlerts = 0  # wdAlertsNone
        return self._word

    def _is_alive(self):
        try:
            _ = self._word.Name
            return True
        except Exception:
            return False


WORD_POOL = WordPool()
