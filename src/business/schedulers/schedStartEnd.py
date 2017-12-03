from src.business.schedulers.qthreadStartEnd import QThreadStartEnd
from src.utils.Singleton import Singleton
import datetime


class SchedStartEnd(metaclass=Singleton):
    def __init__(self, start_obs_info, end_obs_info, total_obs_info):
        self.start_obs_info = start_obs_info
        self.end_obs_info = end_obs_info
        self.total_obs_info = total_obs_info

        self.threadStartEnd = QThreadStartEnd()

        self.threadStartEnd.values_start_end.connect(self.refresh)
        self.c = 0

    def start_scheduler(self):
        self.threadStartEnd.start()

    # Refreshing Start End Observation
    def refresh(self, value):
        the_date = datetime.datetime.utcnow()
        if the_date.hour == 12 and the_date.minute == 0 or self.c == 0:
            info_start_end = value
            start_time = str(info_start_end[0])
            start_field = start_time[:-10] + " UTC"
            end_time = str(info_start_end[1])
            end_field = end_time[:-10] + " UTC"
            time_obs_time = str(info_start_end[2])
            time_obs_field = time_obs_time[:-3] + " Hours"
            try:
                self.start_obs_info.setText(start_field)
                self.end_obs_info.setText(end_field)
                self.total_obs_info.setText(time_obs_field)
            except Exception as e:
                print("refresh SchedStartEnd -> {}".format(e))
            self.c = 1
