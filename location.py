#!/usr/local/python

import re
import subprocess
import sys

def main():
  latlon = subprocess.check_output(["exiftool", "-GPSLatitude", "-GPSLongitude", sys.argv[1]])

  latitude = get_latitude(latlon)
  longitude = get_longitude(latlon)

  print "[%f, %f]" % (longitude, latitude)

def get_latitude(latlon):
  lat_regex_results = re.search('GPS Latitude.*: (\d+) deg (\d+)\' ([\d.]+)\" ([NSEW])', latlon)

  degrees = int(lat_regex_results.group(1))
  minutes = int(lat_regex_results.group(2))
  seconds = float(lat_regex_results.group(3))
  direction = lat_regex_results.group(4)

  return convert_dms_to_decimal(degrees, minutes, seconds, direction)

def get_longitude(latlon):
  lon_regex_results = re.search('GPS Longitude.*: (\d+) deg (\d+)\' ([\d.]+)\" ([NSEW])', latlon)

  degrees = int(lon_regex_results.group(1))
  minutes = int(lon_regex_results.group(2))
  seconds = float(lon_regex_results.group(3))
  direction = lon_regex_results.group(4)

  return convert_dms_to_decimal(degrees, minutes, seconds, direction)

def convert_dms_to_decimal(degrees, minutes, seconds, direction):
  value = (minutes * 60 + seconds) / 3600 + degrees

  if direction == 'W' or direction == 'S':
    value *= -1

  return value

if __name__ == '__main__':
  main()