import json

#import obspy.core.event.base.CreationInfo
#import obspy.core.event.origin.Pick
#import obspy.core.event.origin.Origin
#import obspy.core.event.magnitude.Magnitude
#import obspy.core.event.event.EventDescription
#import obspy.core.event.source.FocalMechanism
#import obspy.core.event.magnitude.Amplitude
#import obspy.core.event.base.Comment
#obspy.core.event.origin.Arrival
#obspy.core.event.base.WaveformStreamID

import obspy
from obspy.core import read
from obspy.io.nordic.core import read_nordic
from obspy.io.nordic.core import write_select
from obspy.io.nordic.core import nordpick
#from quakenet.data_io import load_catalog
from obspy.core.utcdatetime import UTCDateTime
import argparse
import os
import fnmatch
from . import seisobs #https://github.com/d-chambers/seisobs
import sys 
import csv
import traceback

#from sklearn.neighbors.nearest_centroid import NearestCentroid

class Catalog():

    def __init__(self):
        self.events = []
   
    def import_sfiles(self, input_metadata_dir):
        #This imports a nordic format sfile into our own catalog object
        print ("[preprocessing metadata] \033[94m INFO:\033[0m Remember that sfiles need to have names such as 01-1259-00M.S201804")
        metadata_files = [file for file in os.listdir(input_metadata_dir) if
            fnmatch.fnmatch(file, "*")]
        print ("[preprocessing metadata] List of metadata files to anlayze: ", metadata_files)

        #centroids = np.array([[10.33908571, -68.01505714], [8.246, -72.21366667], [10.352, -62.472]]) #centroids
        #centroid_numbers = np.array([0, 1, 2])
        #nearest_centroid_model = NearestCentroid()
        #nearest_centroid_model.fit(centroids, centroid_numbers)

        for metadata_file in metadata_files:
            #WARNING: Nordic Format lines start with a whitespace and have 80 characters
            #NORDIC FORMAT: http://seis.geus.net/software/seisan/node240.html
            #See fields here: https://docs.obspy.org/packages/autogen/obspy.core.event.event.Event.html#obspy.core.event.event.Event
            #1. Process metadata
            print("[preprocessing metadata] Reading metadata file "+os.path.join(input_metadata_dir, metadata_file))
            

            #obspyCatalogMeta = seisobs.seis2cat(os.path.join(input_metadata_dir, metadata_file)) 
            try:
                obspyCatalogMeta = read_nordic(os.path.join(input_metadata_dir, metadata_file))
            except Exception as e:
                print(e)
                track = traceback.format_exc()
                print(track)
                sys.exit()

            print("done")
            print(str(obspyCatalogMeta))

            if len(obspyCatalogMeta.events) == 0 :
                print ("[preprocessing metadata] \033[91m ERROR!!\033[0m Cannot process metadata sfile "+os.path.join(input_metadata_dir, metadata_file))
                sys.exit(0)

            obspyCatalogMeta.events.append(full_test_event())
            write_select (obspyCatalogMeta, os.path.join(input_metadata_dir, "select.out"))

            for event in obspyCatalogMeta.events:
                print("fake event")
                #event = full_test_event()
                print(event)
                eventOriginTime = obspyCatalogMeta.events[0].origins[0].time
                lat = event.origins[0].latitude
                lon = event.origins[0].longitude
                depth = event.origins[0].depth
                if len(event.magnitudes) > 0:
                    mag = event.magnitudes[0].mag
                else:
                    mag = -1 #TODO
                #cluster = nearest_centroid_model.predict([[lat, lon]])[0]
                #e = Event(eventOriginTime, lat, lon, depth, mag, cluster)
                eventid = event.resource_id.id
                e = Event(eventOriginTime, lat, lon, depth, mag, eventid)
                self.events.append(e)
                print("APPEND")
                print(event.origins[0])
                print(nordpick(event))
                

                print("picks:")
                print(event.picks)
                for pick in event.picks:
                    print(pick)

                
                print("arrivals:")
                print(event.origins[0].arrivals)
                for arrival in event.origins[0].arrivals:
                    print(arrival)
                    #station_code = pick.waveform_id.station_code


                #    if pick.phase_hint == 'P':
                #        station_code = pick.waveform_id.station_code
                #        d = Detection(station_code, pick.time)
                #        e.detections.append(d)
                #        print(pick.waveform_id.get_seed_string())
                





                #for comment in sobspyCatalogMeta.events[0].comment:
                #    print("COMMENT:"+comment)

                #print("ID:")
                #print obspyCatalogMeta.events[0].resource_id.id
                #print obspyCatalogMeta.events[0].event_descriptions
                #for desc in obspyCatalogMeta.events[0].event_descriptions:
                #    print("DESC:"+str(desc.text))
                #print("CATALOG:"+obspyCatalogMeta.description)
                #print("COMMENTS:")
                #for ccomment in obspyCatalogMeta.comments:
                #    print("ccomment:"+ccomment)
                #print("CATALOG:"+obspyCatalogMeta.description)
                #print obspyCatalogMeta.resource_id.get_referred_object()
                #print obspyCatalogMeta.creation_info.agency_uri



    def import_txt(self, input_txtfile_path):
        #This imports a summary containing only locations and origin times for events in txt with tab delimiters
        print("[preprocessing metadata] Reading metadata file "+input_txtfile_path)
        with open(input_txtfile_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter="\t", skipinitialspace=True)
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    line_count += 1
                    year = int(row[0].strip())
                    month = int(row[1])
                    day = int(row[2])
                    hour = int(row[3])
                    minute = int(row[4])
                    sec = int(float(row[5]))
                    lat = float(row[6])
                    lon = float(row[7])
                    depth = float(row[8])
                    print(str(year)+","+str(month)+","+str(day)+","+str(hour)+","+str(minute)+","+str(sec)+","+str(lat)+","+str(lon)+","+str(depth))
                    eventOriginTime = UTCDateTime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)
                    e = Event(eventOriginTime, lat, lon, depth)
                    self.events.append(e)
                    

    #def export_json(self, path):
    #    with open(path, 'w') as f:
    #        s = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    #        json.dump(s, f)

    def export_json(self, path):
        with open(path, 'w') as f:
            jevents = {"events":[]}  
            for e in self.events:
                print("FOUND EVENT")
                jevent = {"detections":[]}
                jevent["eventOriginTime"] = str(e.eventOriginTime)
                jevent["lat"] = e.lat
                jevent["lon"] = e.lon
                jevent["depth"] = e.depth
                jevent["mag"] = e.mag
                jevent["eventid"] = e.eventid

                #jevent["cluster"] = e.cluster
                for d in e.detections:
                    jevent["detections"].append({"station":d.station, "ptime":str(d.ptime)})
                jevents["events"].append(jevent)
            json.dump(jevents, f, indent=4)

    def export_javascript(self, path):
        with open(path, 'w') as f:
            i = 0
            for e in self.events:
                f.write("t"+str(i)+": {\n")
                f.write("center: {lat: "+str(e.lat)+", lng:"+str(e.lon)+"},\n")
                f.write("population: "+str(e.mag)+"\n")
                f.write("},\n")
                i = i + 1

    def import_json(self, path):
        with open(path) as f:  
            jdata = json.load(f)
            for jevent in jdata['events']:
                #e = Event(UTCDateTime(jevent['eventOriginTime']), jevent['lat'], jevent['lon'], jevent['depth'], jevent['mag'], jevent['cluster'])
                e = Event(UTCDateTime(jevent['eventOriginTime']), jevent['lat'], jevent['lon'], jevent['depth'], jevent['mag'], jevent['eventid'])
                self.events.append(e)
                for jdetection in jevent['detections']:
                    d = Detection(jdetection['station'], UTCDateTime(jdetection['ptime']))
                    e.detections.append(d)

    def getPtime(self, window_start, window_end, station):
        event, detection = self.getDetection(window_start, window_end, station)
        if detection is not None:
            return detection.ptime
        else:
            return None

    def getLatLongDepth(self, window_start, window_end, station):
        event, detection = self.getDetection(window_start, window_end, station)
        return event.lat, event.lon, event.depth

    def getDetection(self, window_start, window_end, station):
        res = None
        for e in self.events:
            for d in e.detections:
                if ((d.station == station) and (d.ptime >= window_start) and (d.ptime <= window_end)):
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
    def __init__(self, eventOriginTime, lat, lon, depth, mag, eventid):
        self.eventOriginTime = eventOriginTime
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.detections = [] 
        self.mag = mag
        self.eventid = eventid

        #self.cluster = cluster

class Detection():
    def __init__(self, station, ptime):
        self.station = station
        self.ptime = ptime

def full_test_event():
    """
    Function to generate a basic, full test event
    """
    test_event = obspy.core.event.event.Event()
    test_event.origins.append(obspy.core.event.origin.Origin(
        time=UTCDateTime("2012-03-26") + 1.2, latitude=45.0, longitude=25.0,
        depth=15000))
    test_event.event_descriptions.append(obspy.core.event.event.EventDescription())
    test_event.event_descriptions[0].text = 'LE'
    test_event.creation_info = obspy.core.event.base.CreationInfo(agency_id='TES')
    test_event.magnitudes.append(obspy.core.event.magnitude.Magnitude(
        mag=0.1, magnitude_type='ML', creation_info=obspy.core.event.base.CreationInfo('TES'),
        origin_id=test_event.origins[0].resource_id))
    test_event.magnitudes.append(obspy.core.event.magnitude.Magnitude(
        mag=0.5, magnitude_type='Mc', creation_info=obspy.core.event.base.CreationInfo('TES'),
        origin_id=test_event.origins[0].resource_id))
    test_event.magnitudes.append(obspy.core.event.magnitude.Magnitude(
        mag=1.3, magnitude_type='Ms', creation_info=obspy.core.event.base.CreationInfo('TES'),
        origin_id=test_event.origins[0].resource_id))

    # Define the test pick
    _waveform_id_1 = obspy.core.event.base.WaveformStreamID(station_code='FOZ', channel_code='SHZ',
                                      network_code='NZ')
    _waveform_id_2 = obspy.core.event.base.WaveformStreamID(station_code='WTSZ', channel_code='BH1',
                                      network_code=' ')
    # Pick to associate with amplitude - 0
    test_event.picks = [
        obspy.core.event.origin.Pick(waveform_id=_waveform_id_1, phase_hint='IAML',
             polarity='undecidable', time=UTCDateTime("2012-03-26") + 1.68,
             evaluation_mode="manual"),
        obspy.core.event.origin.Pick(waveform_id=_waveform_id_1, onset='impulsive', phase_hint='PN',
             polarity='positive', time=UTCDateTime("2012-03-26") + 1.68,
             evaluation_mode="manual"),
        obspy.core.event.origin.Pick(waveform_id=_waveform_id_1, phase_hint='IAML',
             polarity='undecidable', time=UTCDateTime("2012-03-26") + 1.68,
             evaluation_mode="manual"),
        obspy.core.event.origin.Pick(waveform_id=_waveform_id_2, onset='impulsive', phase_hint='SG',
             polarity='undecidable', time=UTCDateTime("2012-03-26") + 1.72,
             evaluation_mode="manual"),
        obspy.core.event.origin.Pick(waveform_id=_waveform_id_2, onset='impulsive', phase_hint='PN',
             polarity='undecidable', time=UTCDateTime("2012-03-26") + 1.62,
             evaluation_mode="automatic")]
    # Test a generic local magnitude amplitude pick
    test_event.amplitudes = [
        obspy.core.event.magnitude.Amplitude(generic_amplitude=2.0, period=0.4,
                  pick_id=test_event.picks[0].resource_id,
                  waveform_id=test_event.picks[0].waveform_id, unit='m',
                  magnitude_hint='ML', category='point', type='AML'),
        obspy.core.event.magnitude.Amplitude(generic_amplitude=10,
                  pick_id=test_event.picks[1].resource_id,
                  waveform_id=test_event.picks[1].waveform_id, type='END',
                  category='duration', unit='s', magnitude_hint='Mc',
                  snr=2.3),
        obspy.core.event.magnitude.Amplitude(generic_amplitude=5.0, period=0.6,
                  pick_id=test_event.picks[2].resource_id,
                  waveform_id=test_event.picks[0].waveform_id, unit='m',
                  category='point', type='AML')]
    test_event.origins[0].arrivals = [
        obspy.core.event.origin.Arrival(time_weight=0, phase=test_event.picks[1].phase_hint,
                pick_id=test_event.picks[1].resource_id),
        obspy.core.event.origin.Arrival(time_weight=2, phase=test_event.picks[3].phase_hint,
                pick_id=test_event.picks[3].resource_id,
                backazimuth_residual=5, time_residual=0.2, distance=15,
                azimuth=25, takeoff_angle=10),
        obspy.core.event.origin.Arrival(time_weight=2, phase=test_event.picks[4].phase_hint,
                pick_id=test_event.picks[4].resource_id,
                backazimuth_residual=5, time_residual=0.2, distance=15,
                azimuth=25, takeoff_angle=170)]

    return test_event


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


    

        