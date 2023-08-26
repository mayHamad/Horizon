from datetime import datetime, timedelta

WIN32_EPOCH = datetime(1601, 1, 1)

def dt_from_win32_ts(timestamp):
    return WIN32_EPOCH + timedelta(microseconds=timestamp // 10)