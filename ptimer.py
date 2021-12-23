"""Performace Timer

Use to measure seconds between points in code.
"""
from time import time
timers = {}


def start(name=None):
    """Starts timer
    """
    global timers
    if name is None:
        print("PTIMER: Need a name for this timer.")
    else:
        timers[name] = {
            'stime': round(time(), 3),
            'etime': 0,
            'dtime': 0,
            'stopped': False
        }
        print("PTIMER: Timer started for [{0}]".format(name))


def stop(name=None):
    try:
        global timers
        if name is None:
            for t in timers:
                if timers[t]['stopped']:
                    print("PTIMER: [{0}] is already stopped!".format(t))
                else:
                    t = timers[t]
                    t['etime'] = round(time(), 3)
                    t['dtime'] = round(t['etime'] - t['stime'], 3)
                    t['stopped'] = True
        else:
            t = timers[name]
            if not t['stopped']:
                t['etime'] = round(time(), 3)
                t['dtime'] = round(t['etime'] - t['stime'], 3)
                t['stopped'] = True
            else:
                print("PTIMER: [{0}] is already stopped!".format(name))
    except KeyError:
        print("PTIMER: [{0}] isn not a timer I tracked!".format(name))


def display(name=None):
    if not timers:
        print("PTIMER: I didn't track any timers!")
    else:
        try:
            print("\n=====Performance Timer=====")
            if name is None:
                for t in timers:
                    a = timers[t]
                    if a['stopped'] is False:
                        a['dtime'] = round(round(time(), 3) - a['stime'], 3)
                    print("\n{0} (Stopped: {1})\n\tElapsed: {2}\n\tStart: {3}\n\tStop: {4}"
                          .format(t, a['stopped'], a['dtime'], a['stime'], a['etime']))
                    print("\n--------------------")
                print("\n============END============")
            else:
                a = timers[name]
                print("\n{0} (Stopped: {1})\n\tElapsed: {2}\n\tStart: {3}\n\tStop: {4}"
                      .format(name, a['stopped'], a['dtime'], a['stime'], a['etime']))
                print("\n============END============")                    
        except KeyError:
            print("PTIMER: [{0}] isn not a timer I tracked!".format(name))


def stop_display(name=None):
    if name is None:
        stop()
        display()
    else:
        stop(name)
        display(name)
