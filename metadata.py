import sys
import os
import sqlite3
import datetime

exif_value = [
    {id: 618, "str": "exifGPSAltitude", "PrintConv": True},
    {id: 619, "str": "exifGPSAltitudeRef", "PrintConv": True},
    {id: 620, "str": "exifApertureValue", "PrintConv": True},
    {id: 621, "str": "exifArtist", "PrintConv": True},
    {id: 622, "str": "exifBrightnessValue", "PrintConv": True},
    {id: 623, "str": "exifCameraSerialNumber", "PrintConv": True},
    {id: 624, "str": "exifCaptureYear", "PrintConv": True},
    {id: 625, "str": "exifCaptureMonthOfYear", "PrintConv": True},
    {id: 626, "str": "exifCaptureDayOfMonth", "PrintConv": True},
    {id: 627, "str": "exifCaptureDayOfWeek", "PrintConv": True},
    {id: 628, "str": "exifCaptureHourOfDay", "PrintConv": True},
    {id: 629, "str": "exifCaptureMinuteOfHour", "PrintConv": True},
    {id: 630, "str": "exifCaptureSecondOfMinute", "PrintConv": True},
    {id: 633, "str": "exifColorSpace", "PrintConv": False},
    {id: 634, "str": "exifContrast", "PrintConv": True},
    {id: 635, "str": "exifCustomRendered", "PrintConv": True},
    {id: 636, "str": "exifDataRate", "PrintConv": True},#
    {id: 637, "str": "exifDNGBackwardVersion", "PrintConv": True},
    {id: 638, "str": "exifDNGVersion", "PrintConv": True},
    #{id: 639, "str": "exifDepth", "PrintConv": True},# not writeable
    {id: 641, "str": "exifExposureCompensation", "PrintConv": True},  #"exifExposureBiasValue"},
    {id: 642, "str": "exifExposureMode", "PrintConv": False},
    {id: 643, "str": "exifExposureProgram", "PrintConv": False},
    {id: 645, "str": "exifFlash", "PrintConv": False},
    {id: 646, "str": "exifFlashExposureComp", "PrintConv": True},#
    #{id: 648, "str": "exifFocalLenIn35mmFilm", "PrintConv": True}, # not defined
    {id: 649, "str": "exifFocalLength", "PrintConv": True},
    {id: 650, "str": "exifFocusMode", "PrintConv": True},#
    {id: 651, "str": "exifFocusDistance", "PrintConv": True},#
    {id: 652, "str": "exifFPS", "PrintConv": True},#
    {id: 653, "str": "exifDelayTime", "PrintConv": True},#
    {id: 654, "str": "exifGPSHPositioningError", "PrintConv": True},
    {id: 655, "str": "exifGPSLatitudeRef", "PrintConv": True},
    {id: 656, "str": "exifGPSLongitudeRef", "PrintConv": True},
    {id: 657, "str": "exifGPSSpeed", "PrintConv": True},
    {id: 659, "str": "exifGPSTimestamp", "PrintConv": True},
    {id: 661, "str": "exifImageDate", "PrintConv": True}, #
    {id: 662, "str": "exifImageDescription", "PrintConv": True},
    {id: 663, "str": "exifGPSImgDirection", "PrintConv": True},
    {id: 665, "str": "exifISO", "PrintConv": True},#SpeedRating"},
    {id: 666, "str": "exifRecommendedExposureIndex", "PrintConv": True},
    {id: 667, "str": "exifSensitivityType", "PrintConv": True},
    {id: 668, "str": "exifLensMaxMM", "PrintConv": True}, #
    {id: 669, "str": "exifLensMinMM", "PrintConv": True}, #
    {id: 671, "str": "exifLightSource", "PrintConv": True},
    {id: 674, "str": "exifMaxApertureValue", "PrintConv": True},
    {id: 675, "str": "exifMeasuredEV", "PrintConv": True}, #
    {id: 676, "str": "exifMeteringMode", "PrintConv": False},
    {id: 678, "str": "exifMovieDuration", "PrintConv": True},
    {id: 679, "str": "exifNikonFlashSet", "PrintConv": True},
    {id: 682, "str": "exifNikonImageSharpening", "PrintConv": True},
    {id: 690, "str": "exifSaturation", "PrintConv": True},
    {id: 691, "str": "exifSceneCaptureType", "PrintConv": False},
    {id: 692, "str": "exifSharpness", "PrintConv": True},
    {id: 693, "str": "exifShootingMode", "PrintConv": True},
    #{id: 694, "str": "exifShutterSpeed", "PrintConv": True}, # Not Writeable
    {id: 696, "str": "exifSubjectDistance", "PrintConv": True},
    {id: 697, "str": "exifSubsecondTime", "PrintConv": True},
    {id: 698, "str": "exifUserComment", "PrintConv": True},
    {id: 699, "str": "exifWhiteBalance", "PrintConv": False},
    {id: 700, "str": "exifWhiteBalanceIndex", "PrintConv": True},
]

exif_str= [
    #{id: 631, "str": "exifColorModel", "PrintConv": True}, # not defined
    {id: 632, "str": "exifCopyright", "PrintConv": True},
    #{id: 640, "str": "exifExifVersion"}, # not needed
    {id: 644, "str": "exifFirmware", "PrintConv": True},#
    {id: 647, "str": "exifFlashPixVersion", "PrintConv": False},
    {id: 658, "str": "exifGPSSpeedRef", "PrintConv": True},
    {id: 660, "str": "exifGPSVersion", "PrintConv": True},#
    {id: 664, "str": "exifGPSImgDirectionRef", "PrintConv": True},
    {id: 670, "str": "exifLensModel", "PrintConv": True},
    {id: 672, "str": "exifMake", "PrintConv": True},
    {id: 673, "str": "exifGPSMapDatum", "PrintConv": True},
    {id: 677, "str": "exifModel", "PrintConv": True},
    {id: 680, "str": "exifNikonFlashSetting", "PrintConv": True},
    {id: 681, "str": "exifNikonFocusMode", "PrintConv": True},
    {id: 683, "str": "exifNikonQuality", "PrintConv": True},
    {id: 684, "str": "exifNikonSharpenMode", "PrintConv": True},
    {id: 685, "str": "exifNikonWhiteBalanceMode", "PrintConv": True},
    {id: 686, "str": "exifOwnerName", "PrintConv": True},
    #{id: 687, "str": "exifPixelHeight", "PrintConv": True}, # don't want these because they're for orig
    #{id: 688, "str": "exifPixelWidth"},
    {id: 689, "str": "exifProfileName", "PrintConv": True},
    {id: 695, "str": "exifSoftware", "PrintConv": True},
]

def TAG_NAME(meta):
    return meta["str"][4:]

def addTag(string, newtag, value):
    string += " -" + str(newtag) + "=" + str(value)
    return string
def parseDate(tags):
    # Extract date
    new_tags = []
    year = ''
    month = ''
    date = ''
    hour = ''
    minute = '' 
    sec = ''
    tz = ''
    for t in tags:
        if t['name'] == 'ImageDate':
            #imageDate = t['value']
            pass
        elif t['name'] == 'CaptureYear':
            year = str(t['value'])
        elif t['name'] == 'CaptureMonthOfYear':
            month = str(t['value'])
        elif t['name'] == 'CaptureDayOfMonth':
            date = str(t['value'])
        elif t['name'] == 'CaptureDayOfWeek':
            pass
        elif t['name'] == 'CaptureHourOfDay':
            hour = str(t['value'])
        elif t['name'] == 'CaptureMinuteOfHour':
            minute = str(t['value'])
        elif t['name'] == 'CaptureSecondOfMinute':
            sec = str(t['value'])
        elif t['name'] == 'TimeZone':
            tz = str(t['value'])
        else:
            new_tags.append(t)
  
    new_tags.append({
        'name': 'xmp:dateTimeOriginal',
        'value': '"' + year + ":" + month + ":" + date + " " + hour + ":" + minute + ":" + sec + tz + '"',
        'PrintConv': True
        })
    
    return new_tags

def generateTagArgs(tags):
    print("Generating tag set...")
    tag_set = ""
    for t in tags:
        if t['PrintConv']:
            tag_set = addTag(tag_set, t['name'], t['value'])
        else:
            tag_set = addTag(tag_set, t['name'] + "#", t['value'])
    print(tag_set)
    
def getMetadata (db, filename):
    db = sqlite3.connect(db)

    #image = (db.execute("SELECT uuid FROM RKMaster where originalFileName is (?)", 
                        #[filename]).fetchone())[0]
    image = (db.execute("SELECT uuid FROM RKMaster where originalFileName is (?)", 
                        [filename]).fetchall())
    if len(image) == 1:
        image = image[0][0]
    else: 
        print("More than one image matches this name:") 
        for i in range(len(image)):
            print(f"   {i}: {image[i]}")
        selection = int(input("Which one do you want? "))
        image = image[selection][0]

    print(f"Selected {image}...")
    
    version_modelId = (db.execute("SELECT modelId FROM RKVersion where masterUuid is (?)",
                                [image]).fetchone())[0]

    tags = []

    print("Looking up EXIF data for image: {}, id: {}, modelId: {}".format(filename, image, version_modelId))
    tables = db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%RKVersion_%Note'").fetchall()

    for meta in exif_value: 
        value = None
        for t in tables:
            value = db.execute("SELECT value FROM {} WHERE attachedToId is (?) AND keyPath is (?)".format(t[0]),[version_modelId, meta[id]]).fetchone()

            if value != None:
                value = value[0]
                #tagstring = addTag(tagstring, TAG_NAME(meta), value)
                tags.append({"name": TAG_NAME(meta), "value": value, "PrintConv": meta['PrintConv']})
                break
    
    for meta in exif_str: 
        value = None
        value = db.execute("SELECT value FROM RKVersion_stringAtomNote WHERE attachedToId is (?) AND keyPath is (?)".format(t[0]),[version_modelId, meta[id]]).fetchone()

        if value != None:
            string = db.execute("SELECT string FROM LiStringAtom WHERE modelId is (?)", 
                    [value[0]]).fetchone()
           
            string = "'" + string[0] + "'"
            #tagstring = addTag(tagstring, TAG_NAME(meta), string)
            tags.append({"name": TAG_NAME(meta), "value": string, "PrintConv": meta['PrintConv']})

    # GPS Data
    #place_id = db.execute("SELECT placeId FROM RKPlaceForVersion WHERE modelId is (?)", [version_modelId]).fetchone()[0]
    #gps_list = gps_data[1:len(gps_data) -1].split(',')
    if (db.execute("SELECT longitude FROM RKVersion WHERE modelId is (?)", [version_modelId]).fetchone()[0]) is not None:
        gps_long = float(db.execute("SELECT longitude FROM RKVersion WHERE modelId is (?)", [version_modelId]).fetchone()[0])
        gps_lat = float(db.execute("SELECT latitude FROM RKVersion WHERE modelId is (?)", [version_modelId]).fetchone()[0])
        #tagstring = addTag(tagstring, "GPSLongitude", gps_long)
        #tagstring = addTag(tagstring, "GPSLongitudeRef", gps_long) # Setting to neg/pos value auto sets via exiftool
        #tagstring = addTag(tagstring, "GPSLatitude", gps_lat)
        #tagstring = addTag(tagstring, "GPSLatitudeRef", gps_lat) # Setting to neg/pos value auto sets via exiftool
        tags.append({"name": "GPSLongitude", "value": gps_long, "PrintConv": True})
        tags.append({"name": "GPSLongitudeRef", "value": gps_long, "PrintConv": True})
        tags.append({"name": "GPSLatitude", "value": gps_lat, "PrintConv": True})
        tags.append({"name": "GPSLatitudeRef", "value": gps_lat, "PrintConv": True})

    # Timezone
    timezone = db.execute("SELECT imageTimeZoneName FROM RKVersion WHERE modelId is (?)", [version_modelId]).fetchone()[0]
    tags.append({"name": "TimeZone", "value": timezone[3:], "PrintConv": True})

    return tags 

if __name__ == "__main__":
    database = sys.argv[1]
    filename = sys.argv[2]

    tags = getMetadata(database, filename)
    tags = parseDate(tags)
    generateTagArgs(tags)
