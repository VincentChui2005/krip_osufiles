from pynput.keyboard import Listener, Key
from threading import Thread
import time

keys = "zx"  # keys that can trigger reporting, let's say they are the keys that you hit when playing osu!
report_rate = 0  # in times per second, 0 for instant report
round_base = 5  # make reports in a multiple of something, 0 to disable
holding_reports = 5  # no. of reports to be taken avg to avoid too much fluctuations, 0 / 1 to disable
quit_key = Key.delete


last = 0
report = 0
recent_reports = []
def on_press(key):
    try:
        key = key.char  # convert keystroke to key character name
    except AttributeError:
        if key == quit_key: quit()
    else:
        if key in keys:
            global last, report
            t = time.time()
            if t - report > (1 / report_rate if report_rate != 0 else 0):
                recent_reports.append(15 / (t - last))  # nps:bpm = 1:(60/4) = 1:15 for normal streaming

                raw_bpm = sum(recent_reports)/len(recent_reports)  # avg of {holding_reports} reports
                rounded_bpm = round(raw_bpm/round_base)*round_base if round_base != 0 else raw_bpm  # round {raw_bpm} to multiple of {round base}
                print(rounded_bpm)
                if len(recent_reports) >= holding_reports: recent_reports.pop(0)  # keep only the nearest {holding_reports} reports
                report = t
            last = t


with Listener(on_press=on_press) as li: li.join()
