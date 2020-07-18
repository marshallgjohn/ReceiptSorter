import re, glob, os, pytesseract
from shutil import copyfile
from PIL import Image
from datetime import datetime


def dateFinder(string, dir, file, destDir,storeName):
    """Regex to find date and beg of moving file around"""
    # Regex list for dates
    re_list = [
        # Regex for dates like January 14, 2018 or Jan 14 2018 or Jan 14, 2018 or 14 Jan 2018
        r"((\b\d{1,2}\D{0,3})?\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|(?:nov|dec)(?:ember))\D?(\d{1,2}\D?)?\D?((19[7-9]\d|20\d{2})|\d{2}))",
        # Regex for dates like 1/1/2018 or 01/01/2018
        r"(\d{2}/\d+/\d+)"
    ]

    # Create blank list for potential dates
    matches = []

    # Searches text from file for any dates from corresponding regex
    for res in re_list:
        matches += re.findall(res, string)

    # If file is unreadable move to manual move folder
    if not matches:
        invalidFile(dir, file, destDir)

    # Looks at each match found from regex and determines how to move it around
    for match in matches:
        #print(file)
        index = matches[findBestDate(matches)]
        date = filenameFormat(index)

        # Determines if date picked by regex is in the future due to image-to-string error or other error
        if int(str(date[0] + date[1])) > datetime.now().month:
            invalidFile(dir, file, destDir)
            break
        updateFile(matches, dir, file, destDir, storeName, date)


def invalidFile (dir, file, destDir):
    """If file is unreadable or otherwise does not work move for manual review"""
    copyfile(dir + file, destDir + "unknown/" + file)
    os.remove(dir + file)
    print("File " + file + " need your attention!")


def updateFile(matches, dir, file, destDir,storeName, date):
    """Determines if path for file is made and copies/removes file to proper location"""
    if not os.path.exists(destDir + date[0] + date[1] + "-18"):
        os.makedirs(destDir + date[0] + date[1] + "-18")

    copyfile(dir + file, destDir + "/" + date[0] + date[1] + "-18" + "/" + date + "-18 " + storeName + ".jpg")
    os.remove(dir + file)
    print(file + " moved to: " + destDir + "/" + date[0] + date[1] + "-18" + "/" + date + "-18 " + storeName + ".jpg")



def findBestDate(matches):
    """Finds closest date incase of multiple dates on reciept"""
    value = "13"
    index = -1
    for match in matches:
        if int(str(match[0] + match[1]) < value) and not match[1] == '/':
            value = str(match[0] + match[1])
            index += 1
    if index == -1:
        index = 0
    return index


def filenameFormat (match):
    """Formats the filenames depending on what regex found in prev function"""
    #print(match)
    # Formats filename for all months from jan - dec
    if('january' in match[0] or 'jan' in match[0]):
        return str("01-" + match[2][0] + match[2][1])
    elif ('febuary' in match[0] or 'feb' in match[0]):
        return str("02-" + match[2][0] + match[2][1])
    elif ('march' in match[0] or 'march' in match[0]):
        return str("03-" + match[2][0] + match[2][1])
    elif ('april' in match[0] or 'apr' in match[0]):
        return str("04-" + match[2][0] + match[2][1])
    elif ('may' in match[0] or 'may' in match[0]):
        return str("05-" + match[2][0] + match[2][1])
    elif ('june' in match[0] or 'jun' in match[0]):
        return str("06-" + match[2][0] + match[2][1])
    elif ('july' in match[0] or 'jul' in match[0]):
        return str("07-" + match[2][0] + match[2][1])
    elif ('august' in match[0] or 'aug' in match[0]):
        return str("08-" + match[2][0] + match[2][1])
    elif ('sept' in match[0] or 'sept' in match[0]):
        return str("09-" + match[2][0] + match[2][1])
    elif ('october' in match[0] or 'oct' in match[0]):
        return str("10-" + match[2][0] + match[2][1])
    elif ('november' in match[0] or 'nov' in match[0]):
        return str("11-" + match[2][0] + match[2][1])
    elif ('december' in match[0] or 'dec' in match[0]):
        return str("12-" + match[2][0] + match[2][1])


    # Format file name for 01/01/2018 and 1/1/2018 dates
    if (match[1] != '/'):
        return str(match[0] + match[1] + "-" + match[3] + match[4])
    elif(match[1] == '/'):
        return str("0" + match[0] + "-" + "0" + match[2])
    return " "


def fileRunner(dir, destDir):
    """Runs thru all .jpg files in dir folder"""
    os.chdir(dir)
    for file in glob.glob("*.jpg"):
        fileReader(dir, file, destDir)


def fileReader(dir, file, destDir):
    """Finds and creates readable image and finds store name to find date and move file from scanning to approriate date of creation"""
    image = Image.open(dir + file)
    string = pytesseract.image_to_string(image, lang='eng')
    storeName = findStore(string)
    dateFinder(string, dir, file, destDir, storeName)
    #print(pytesseract.image_to_string(image, lang='eng'))

    # OLD PDF WAY TO FIND FILES WHEN USING EPSON PDF TEXT SEARCH NOW USING OWN VERSION
    #pdfFileObj = open(dir + file, 'rb')
    #pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    #pageObj = pdfReader.getPage(0)


def findStore(string):
    """Simple funct to find a store name in read text to add to end of file name"""

    if "target" in string.lower():
        return "target"
    elif "chipotle" in string.lower():
        return "chipotle"
    elif "ross" in string.lower():
        return "ross"
    elif "cvs" in string.lower():
        return "cvs"
    elif "panda" in string.lower():
        return "panda express"
    elif "shell" in string.lower():
        return "shell"

    return ""


fileRunner("F:\\My Documents\\Personal\\Scanning\\", "F:/My Documents/Personal/Reciepts/")
