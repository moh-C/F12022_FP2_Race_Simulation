from datetime import timedelta
from statistics import mode


def get_race_sim(df, name, stint_tyre=False):
    temp_df = df[df["Driver"] == name]
    idx1 = temp_df["LapTime"] > timedelta(minutes=1, seconds=34, milliseconds=500)
    idx2 = temp_df["LapTime"] < timedelta(minutes=1, seconds=42)
    idx = idx1 & idx2
    time_filtered_df = temp_df[idx]
    stint_target = mode(time_filtered_df["Stint"])
    stint_filtered_data = time_filtered_df[time_filtered_df["Stint"] == stint_target]
    tyre = mode(stint_filtered_data["Compound"])

    if tyre == "MEDIUM":
        tyre = "M"
    elif tyre == "SOFT":
        tyre = "S"
    elif tyre == "HARD":
        tyre = "H"
        
    times = list(stint_filtered_data["LapTime"])
    times = [time.total_seconds() for time in times]
    if stint_tyre:
        return times, tyre
    return times

class DriverRacePaceInfo():
    def __init__(self, _name, df):
        self.name = _name
        self.stintTyre = 'SOFT'
        self.times = []
        self.stintLength = None
        self.team = None
        self.get_pace(df)
        
    def get_pace(self, df):
        self.times, self.stintTyre = get_race_sim(df, self.name, True)
        
        temp = df[df["Driver"] == self.name]
        self.team = temp.iloc[0].Team
        
        self.calc_len()
        
    def calc_len(self):
        self.stintLength = len(self.times)
        
    def __repr__(self):
        resp = f"Driver Name: {self.name}\n"
        resp += f"Tyre Compound: {self.stintTyre}\n"
        resp += f"Times: {self.times}\n"
        resp += f"Stint Length: {self.stintLength}\n"
        resp += f"Team is: {self.team}"
        return resp