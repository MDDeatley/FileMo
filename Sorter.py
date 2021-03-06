import os, re, eyed3  # pip install eyed3
from datetime import datetime, timedelta
from pathlib import Path

class sorter:
    ifstack = []  # stores
    opfeed = []  # oplist storage
    files = []  # file list storage
    sortedFiles = [] # list of already sorted files
    dest = ''  # dest directory storage

    def __init__(self, oplist, dest, filelist):
        self.opfeed = oplist  # get oplist
        self.files = filelist  # get filelist
        self.dest = dest  # set file dest directory
        self.sortif()  #do sort if

    def stackif(self, file, ops):
        boolstack = True
        state = True
        for x in ops:  # if there is no ops returns true
            if x[1][0] == 'filename':
                reg = x[3][1][1:-1]  # strip quotes
                try:
                    name = os.path.splitext(os.path.basename(file))
                    if x[1][1] == 'type':
                        name = name[1][1:]
                    elif x[1][1] == 'name':
                        name = name[0]
                    if x[2] != '':
                        if reg == '':
                            state = True
                        else:
                            state = (reg in name)
                    else:
                        state = (reg == name.lower())
                    if x[0] == 6:
                        state = not state
                except:
                    #file already sorted
                    state = False


            elif x[1][0] == 'medianame':
                try:
                    if not (file in self.sortedFiles): # if file not sorted
                        reg = x[3][1][1:-1]  # strip quotes
                        name = ''
                        if x[1][1] == "title":
                            mp3 = eyed3.load(file)
                            name = mp3.tag.getTitle().lower()
                        elif x[1][1] == "artist":
                            mp3 = eyed3.load(file)
                            name = mp3.tag.getArtist().lower()
                        elif x[1][1] == "author":
                            name = os.stat(file).st_uid.lower()
                        if x[2] != '':
                            if reg == '':
                                state = True
                            else:
                                state = (reg in name)
                        else:
                            state = (reg == name)
                        if x[0] == 6:
                            state = not state
                    else:
                        state = False #file is already sorted
                except:
                    state = False

            elif x[1][0] == 'filetime':
                if x[3][0] == 'time':
                    try:
                        # extract int from user date
                        usertime = int(re.search(r'\d+', x[3][1]).group())
                        if 's' in x[3][1]:
                            usertime = timedelta(seconds=usertime)
                        elif 'mn' in x[3][1]:
                            usertime = timedelta(minutes=usertime)
                        elif 'h' in x[3][1]:
                            usertime = timedelta(hours=usertime)
                        elif 'd' in x[3][1]:
                            usertime = timedelta(days=usertime)
                        elif 'm' in x[3][1]:
                            usertime = timedelta(days=usertime*30.44)  # timedelta does not use months
                        elif 'y' in x[3][1]:
                            usertime = timedelta(days=usertime*365.25)  # timedelta does not use years
                        # get files time
                        try:
                            if x[1][1] == 'modifydate':
                                filetime = datetime.fromtimestamp(os.path.getmtime(file))
                            elif x[1][1] == 'createdate':
                                filetime = datetime.fromtimestamp(os.path.getctime(file))
                            elif x[1][1] == 'accessdate':
                                filetime = datetime.fromtimestamp(os.path.getatime(file))
                            else:
                                x[0] = 0
                            # do compare
                            if x[0] == 1:
                                state = filetime.date() == (datetime.today() - usertime).date()
                            elif x[0] == 2:
                                state = filetime >= datetime.today() - usertime
                            elif x[0] == 3:
                                state = filetime < datetime.today() - usertime
                            elif x[0] == 4:
                                state = filetime <= datetime.today() - usertime
                            elif x[0] == 5:
                                state = filetime > datetime.today() - usertime
                            elif x[0] == 6:
                                state = filetime.date() != (datetime.today() - usertime).date()
                            else:
                                state = False
                        except:
                            #file already sorted
                            state = False
                    except:
                        print('invalid date')
                        state = False
                elif x[3][0] == 'date':
                    try:
                        usertime = datetime.strptime(x[3][1], '%d-%m-%Y')
                        try:
                            if x[1][1] == 'modifydate':
                                filetime = datetime.fromtimestamp(os.path.getmtime(file))
                            elif x[1][1] == 'createdate':
                                filetime = datetime.fromtimestamp(os.path.getctime(file))
                            elif x[1][1] == 'accessdate':
                                filetime = datetime.fromtimestamp(os.path.getatime(file))
                            # do compare
                            if x[0] == 1:
                                state = filetime.date() == usertime.date()
                            elif x[0] == 2:
                                state = filetime.date() >= usertime.date()
                            elif x[0] == 3:
                                state = filetime.date() < usertime.date()
                            elif x[0] == 4:
                                state = filetime.date() <= usertime.date()
                            elif x[0] == 5:
                                state = filetime.date() > usertime.date()
                            elif x[0] == 6:
                                state = filetime.date() != usertime.date()
                        except:
                            #file has already been sorted
                            state = False
                    except:
                        print('invalid date')
                        state = False

            elif x[1][0] == 'filesize':
                try:
                    filesize = os.path.getsize(file)
                    usersize = int(re.search(r'\d+', x[3][1]).group())
                    mult = 1
                    if 'kb' in x[3][1]:
                        mult = 1024
                    elif 'mb' in x[3][1]:
                        mult = 1048576
                    elif 'gb' in x[3][1]:
                        mult = 1073741824
                    elif 'tb' in x[3][1]:
                        mult = 1099511627776
                    if x[0] == 1:
                        filesize = filesize // mult
                        state = filesize == usersize
                    elif x[0] == 2:
                        state = filesize >= usersize * mult
                    elif x[0] == 3:
                        state = filesize < usersize * mult
                    elif x[0] == 4:
                        state = filesize <= usersize * mult
                    elif x[0] == 5:
                        state = filesize > usersize * mult
                    elif x[0] == 6:
                        filesize = filesize // mult
                        state = filesize != usersize
                except:
                    # file already sorted
                    state = False

            boolstack = boolstack and state

        return boolstack

    def sortif(self):
        opstack = []
        for x in self.opfeed:
            if x[0] == 0:
                if x[1][0] == 'clear':  # clear if stack
                    i = 0
                    while len(opstack) > 0:
                        opstack.pop()
                elif x[1][0] == 'path':
                    for y in self.files:
                        if self.stackif(y, opstack):  # do if stack on file
                            try:
                                ################################################################
                                
                                new_name = x[1][1]
                                
                                fileC = datetime.fromtimestamp(os.path.getctime(y))
                                fileM = datetime.fromtimestamp(os.path.getmtime(y))
                                fileA = datetime.fromtimestamp(os.path.getatime(y))
                                
                                new_name = new_name.replace('(cyear)', str(fileC.year) + ' c')
                                new_name = new_name.replace('(myear)', str(fileM.year) + ' m')
                                new_name = new_name.replace('(ayear)', str(fileA.year) + ' a')

                                new_name = new_name.replace('(cmonth)', str(fileC.month) + ' c')
                                new_name = new_name.replace('(mmonth)', str(fileM.month) + ' m')
                                new_name = new_name.replace('(amonth)', str(fileA.month) + ' a')

                                new_name = new_name.replace('(cday)', str(fileC.day) + ' c')
                                new_name = new_name.replace('(mday)', str(fileM.day) + ' m')
                                new_name = new_name.replace('(aday)', str(fileA.day) + ' a')

                                #for x in ['<', '>', ':', '"', '/', '\\', '|', '?', '*']:
                                #    print(x)
                                
                                #################################################################
                                Path(self.dest + new_name).mkdir(parents=True, exist_ok=True)  # make directory
                            except:
                                pass
                            try:
                                if not (y in self.sortedFiles):
                                    os.rename(y, (self.dest + new_name + os.path.basename(y)))
                                    self.sortedFiles.append(y)
                            except:
                                pass
                    if len(opstack) != 0:
                        opstack.pop()
            else:
                opstack.append(x)

        self.sortedFiles.clear()
