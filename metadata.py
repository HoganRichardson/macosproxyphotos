import sys
import os
import sqlite3

exif_value = [
    {id: 618, "str": "exifGPSAltitude"},
    {id: 619, "str": "exifGPSAltitudeRef"},
    {id: 620, "str": "exifApertureValue"},
    {id: 621, "str": "exifArtist"},
    {id: 622, "str": "exifBrightnessValue"},
    {id: 623, "str": "exifCameraSerialNumber"},
    {id: 624, "str": "exifCaptureYear"},
    {id: 625, "str": "exifCaptureMonthOfYear"},
    {id: 626, "str": "exifCaptureDayOfMonth"},
    {id: 627, "str": "exifCaptureDayOfWeek"},
    {id: 628, "str": "exifCaptureHourOfDay"},
    {id: 629, "str": "exifCaptureMinuteOfHour"},
    {id: 630, "str": "exifCaptureSecondOfMinute"},
    {id: 633, "str": "exifColorSpace"},
    {id: 634, "str": "exifContrast"},
    {id: 635, "str": "exifCustomRendered"},
    {id: 636, "str": "exifDataRate"},#
    {id: 637, "str": "exifDNGBackwardVersion"},
    {id: 638, "str": "exifDNGVersion"},
    {id: 639, "str": "exifDepth"},#
    {id: 641, "str": "exifExposureCompensation"},  #"exifExposureBiasValue"},
    {id: 642, "str": "exifExposureMode"},
    {id: 643, "str": "exifExposureProgram"},
    {id: 645, "str": "exifFlash"},
    {id: 646, "str": "exifFlashExposureComp"},#
    {id: 648, "str": "exifFocalLenIn35mmFilm"},
    {id: 649, "str": "exifFocalLength"},
    {id: 650, "str": "exifFocusMode"},#
    {id: 651, "str": "exifFocusDistance"},#
    {id: 652, "str": "exifFPS"},#
    {id: 653, "str": "exifDelayTime"},#
    {id: 654, "str": "exifGPSHPositioningError"},
    {id: 655, "str": "exifGPSLatitudeRef"},
    {id: 656, "str": "exifGPSLongitudeRef"},
    {id: 657, "str": "exifGPSSpeed"},
    {id: 659, "str": "exifGPSTimestamp"},
    {id: 661, "str": "exifImageDate"}, #
    {id: 662, "str": "exifImageDescription"},
    {id: 663, "str": "exifGPSImgDirection"},
    {id: 665, "str": "exifISO"},#SpeedRating"},
    {id: 666, "str": "exifRecommendedExposureIndex"},
    {id: 667, "str": "exifSensitivityType"},
    {id: 668, "str": "exifLensMaxMM"}, #
    {id: 669, "str": "exifLensMinMM"}, #
    {id: 671, "str": "exifLightSource"},
    {id: 674, "str": "exifMaxApertureValue"},
    {id: 675, "str": "exifMeasuredEV"}, #
    {id: 676, "str": "exifMeteringMode"},
    {id: 678, "str": "exifMovieDuration"},
    {id: 679, "str": "exifNikonFlashSet"},
    {id: 682, "str": "exifNikonImageSharpening"},
    {id: 690, "str": "exifSaturation"},
    {id: 691, "str": "exifSceneCaptureType"},
    {id: 692, "str": "exifSharpness"},
    {id: 693, "str": "exifShootingMode"},
    {id: 694, "str": "exifShutterSpeed"},
    {id: 696, "str": "exifSubjectDistance"},
    {id: 697, "str": "exifSubsecondTime"},
    {id: 698, "str": "exifUserComment"},
    {id: 699, "str": "exifWhiteBalance"},
    {id: 700, "str": "exifWhiteBalanceIndex"},
]

exif_str= [
    {id: 631, "str": "exifColorModel"},#
    {id: 632, "str": "exifCopyright"},
    #{id: 640, "str": "exifExifVersion"}, # not needed
    {id: 644, "str": "exifFirmware"},#
    {id: 647, "str": "exifFlashPixVersion"},
    {id: 658, "str": "exifGPSSpeedRef"},
    {id: 660, "str": "exifGPSVersion"},#
    {id: 664, "str": "exifGPSImgDirectionRef"},
    {id: 670, "str": "exifLensModel"},
    {id: 672, "str": "exifMake"},
    {id: 673, "str": "exifGPSMapDatum"},
    {id: 677, "str": "exifModel"},
    {id: 680, "str": "exifNikonFlashSetting"},
    {id: 681, "str": "exifNikonFocusMode"},
    {id: 683, "str": "exifNikonQuality"},
    {id: 684, "str": "exifNikonSharpenMode"},
    {id: 685, "str": "exifNikonWhiteBalanceMode"},
    {id: 686, "str": "exifOwnerName"},
    #{id: 687, "str": "exifPixelHeight"}, # don't want these because they're for orig
    #{id: 688, "str": "exifPixelWidth"},
    {id: 689, "str": "exifProfileName"},
    {id: 695, "str": "exifSoftware"},
]

def TAG_NAME(meta):
    return meta["str"][4:]

def addTag(string, newtag, value):
    string += " -" + str(newtag) + "=" + str(value)
    return string

def getMetadata (db, filename):
    db = sqlite3.connect(db)

    image = (db.execute("SELECT uuid FROM RKMaster where originalFileName is (?)", 
                        [filename]).fetchone())[0]
    version_modelId = (db.execute("SELECT modelId FROM RKVersion where masterUuid is (?)",
                                [image]).fetchone())[0]

    tagstring = ""

    print("Looking up EXIF data for image: {}, id: {}, modelId: {}".format(filename, image, version_modelId))
    tables = db.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%RKVersion_%Note'").fetchall()

    for meta in exif_value: 
        value = None
        for t in tables:
            value = db.execute("SELECT value FROM {} WHERE attachedToId is (?) AND keyPath is (?)".format(t[0]),[version_modelId, meta[id]]).fetchone()

            if value != None:
                value = value[0]
                tagstring = addTag(tagstring, TAG_NAME(meta), value)
                break
    
    for meta in exif_str: 
        value = None
        value = db.execute("SELECT value FROM RKVersion_stringAtomNote WHERE attachedToId is (?) AND keyPath is (?)".format(t[0]),[version_modelId, meta[id]]).fetchone()

        if value != None:
            string = db.execute("SELECT string FROM LiStringAtom WHERE modelId is (?)", 
                    [value[0]]).fetchone()
           
            string = "'" + string[0] + "'"
            tagstring = addTag(tagstring, TAG_NAME(meta), string)

    return tagstring

if __name__ == "__main__":
    database = sys.argv[1]
    filename = sys.argv[2]

    tagstr = getMetadata(database, filename)
    print(tagstr)
