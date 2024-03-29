import json

import obspy
from obspy.core import read
from obspy.io.nordic.core import read_nordic
from obspy.io.nordic.core import write_select
from obspy.io.nordic.core import readwavename
from obspy.io.nordic.core import nordpick
from obspy.core.utcdatetime import UTCDateTime
import argparse
import os
import fnmatch
import sys 
import csv
import traceback

class Catalog():

    def __init__(self):
        self.events = []

    def import_sfile(self, input_path):
        try:
            obspyCatalogMeta = read_nordic(input_path, return_wavnames=True)
            #If return_wavnames not specified it returns directly the events, otherwise:
            #obspyCatalogMeta[0] contains the events
            #obspyCatalogMeta[1] contains the waveform files
        except Exception as e:
            print ("[preprocessing metadata] \033[91m ERROR!!\033[0m Error reading Nordic Format file: "+str(e))
            track = traceback.format_exc()
            print(track)
            sys.exit()

        if len(obspyCatalogMeta[0].events) == 0 :
            print ("[preprocessing metadata] \033[91m ERROR!!\033[0m No events found in "+input_path)
            sys.exit(0)

        #For testing we can add an event generated by code
        #using the function full_test_event
        #https://github.com/obspy/obspy/blob/master/obspy/io/nordic/tests/test_nordic.py
        #obspyCatalogMeta.events.append(full_test_event())
        #write_select (obspyCatalogMeta[0], "select_debug.out")

        #wave files can be read alone with:
        #print(readwavename(input_path))

        eventsCatalog = obspyCatalogMeta[0]
        waveform_files = obspyCatalogMeta[1]

        for i, event in enumerate(eventsCatalog.events):
            print("Processing event "+str(i))
            eventOriginTime = event.origins[0].time
            lat = event.origins[0].latitude
            lon = event.origins[0].longitude
            depth = event.origins[0].depth
            if len(event.magnitudes) > 0:
                mag = event.magnitudes[0].mag
            else:
                print ("[preprocessing metadata] \033[91m WARNING!!\033[0m Magnitude not found in event number"+str(i))
                mag = 0
                #sys.exit()
            
            eventid = event.resource_id.id
            e = Event(eventOriginTime, lat, lon, depth, mag, eventid, waveform_files[i])
            self.events.append(e)

            for pick in event.picks:
                station_code = pick.waveform_id.station_code
                d = Pick(station_code, pick.time, pick.phase_hint)
                e.picks.append(d)

    def export_json(self, path):
        with open(path, 'w') as f:
            jevents = {"events":[]}  
            for e in self.events:
                jevent = {"picks":[]}
                jevent["eventOriginTime"] = str(e.eventOriginTime)
                jevent["lat"] = e.lat
                jevent["lon"] = e.lon
                jevent["depth"] = e.depth
                jevent["mag"] = e.mag
                jevent["eventid"] = e.eventid
                jevent["waveform_file"] = e.waveform_file
                for d in e.picks:
                    jevent["picks"].append({"station":d.station, "ptime":str(d.ptime), "phase_hint":str(d.phase_hint)})
                jevents["events"].append(jevent)
            json.dump(jevents, f, indent=4)

    def import_json(self, path):
        with open(path) as f:  
            jdata = json.load(f)
            for jevent in jdata['events']:
                e = Event(UTCDateTime(jevent['eventOriginTime']), jevent['lat'], jevent['lon'], jevent['depth'], jevent['mag'], jevent['eventid'], jevent['waveform_file'])
                self.events.append(e)
                for jpick in jevent['picks']:
                    d = Pick(jpick['station'], UTCDateTime(jpick['ptime']), jpick['phase_hint'])
                    e.picks.append(d)

    def getPtime(self, window_start, window_end, station):
        event, pick = self.getPick(window_start, window_end, station, "P")
        if pick is not None:
            return pick.ptime
        else:
            return None

    def getPick(self, window_start, window_end, station, phase_hint):
        res = None
        for e in self.events:
            for d in e.picks:
                if ((d.station == station) and (d.phase_hint == phase_hint) and (d.ptime >= window_start) and (d.ptime <= window_end)):
                    return e, d
        return None, None

    def getLocations(self, depth=True):
        locations = []
        for e in self.events:
            locations.append([e.lat, e.lon, e.depth])
            if depth:
                print(str(e.lat)+","+str(e.lon)+","+str(e.depth))
            else:
                print(str(e.lat)+","+str(e.lon))
        return locations

class Event():
    #def __init__(self, eventOriginTime, lat, lon, depth, mag, cluster):
    def __init__(self, eventOriginTime, lat, lon, depth, mag, eventid, waveform_file):
        self.eventOriginTime = eventOriginTime
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.picks = [] 
        self.mag = mag
        self.eventid = eventid
        self.waveform_file = waveform_file

        #self.cluster = cluster

class Pick():
    def __init__(self, station, ptime, phase_hint):
        self.station = station
        self.ptime = ptime
        self.phase_hint = phase_hint

if __name__ == "__main__":
    print ("\033[92m******************** CATALOG TOOL *******************\033[0m ")
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", type=str)
    parser.add_argument("--output_path", type=str)
    args = parser.parse_args()
    if not os.path.exists(os.path.dirname(args.output_path)):
        os.makedirs(os.path.dirname(args.output_path))
    c = Catalog()
    #c.import_sfiles(args.input_path)
    #c.export_json(args.output_path)
    c.import_json(args.input_path)
    c.export_javascript(args.output_path)


    

        