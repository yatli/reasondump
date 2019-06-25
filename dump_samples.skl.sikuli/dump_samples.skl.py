# make sure reason is opened, and sample auto play is OFF, and the rack is EMPTY.

reason = App("Reason")
#setShowActions(True)
reason.focus()


#factorySounds = find("1561267759716.png")
factorySounds = Location(64, 304)

searchButton = find("1561279881629.png")
searchTextbox = searchButton.left(600)

#playButton = find("1561292665476.png")
playButton = Location(583, 956)

#nextButton = find("1561292683253.png")
nextButton = Location(699, 932)

#label = find("1561292817890.png")
rexLabel = Location(879, 375)
track = rexLabel.above(30)
trackLabel = Location(834, 344)

#importButton = find("1561428913029.png")
importButton = Location(673, 932)
scrollbar = Location(719, 452)
# ------------------ Interruption -------------------
userInterrupt = False

def onUserInterrupt(event):
    global userInterrupt 
    userInterrupt = True

Env.addHotkey(Key.F1, KeyModifier.ALT+KeyModifier.CTRL, onUserInterrupt)
# ---------------------------------------------------


def readRex():
    rexLabel.doubleClick()
    sleep(0.5)
    type("c", Key.CTRL)
    type(Key.ESC)
    fname=reason.getClipboard()
    playButton.click()
    return fname

def nextRex():
    nextButton.click()
    sleep(4)

def cleanupRex():
    # then, delete the rex machine
    track.click()
    type(Key.DELETE)
    sleep(1)
    type(Key.ENTER)

def readAiff():
    trackLabel.doubleClick()
    sleep(0.5)
    type("c", Key.CTRL)
    type(Key.ESC)
    fname=reason.getClipboard()
    playButton.click()
    return fname

def nextAiff():
    # delete the audio track
    track.click()
    type(Key.DELETE)
    sleep(0.5)
    type(Key.ENTER)
    sleep(1) 
    # focus back to sample explorer, down, then import
    scrollbar.click()
    type(Key.DOWN)
    importButton.click()
    sleep(1)

def cleanupAiff():
    pass
    
def go_nav(folder, section, searchItem):
    if folder:
        folder.click()
        sleep(1)
    if section:
        section.doubleClick()
    searchTextbox.click()
    type(searchItem + Key.ENTER)
    sleep(3)
    # double click first entry
    Location(228, 186).doubleClick()

def go_dump(readProc, nextProc, cleanupProc, name):
    # iterate through all the samples
    with open("recorder/"+name+".txt", "w") as f:
        for i in range(0, nr):
            if userInterrupt:
                break
            fname = readProc()
            f.write(fname)
            f.write("\n")
            f.flush()
            sleep(3)
            while not exists("1561294114006.png"):
                pass
            nextProc()
    # then, move all the dumped samples into a folder


def go_rex(folder, section, name, nr):
    if userInterrupt:
        return
    go_nav(folder, section, ".rx2")
    sleep(5)
    # now, the first rex loop is loaded, and a OctoRex is created.
    go_dump(readRex, nextRex, cleanupRex, name)


def go_aiff(section, name, nr):
    if userInterrupt:
        return
    go_nav(folder, section, ".aif")
    sleep(2)
    # now, the first aiff is loaded, and an audio track is created.
    go_dump(readAiff, nextAiff, cleanupAiff, name)

def go_wav(section, name, nr):
    if userInterrupt:
        return
    go_nav(folder, section, ".wav")
    sleep(2)
    # now, the first aiff is loaded, and an audio track is created.
    go_dump(readAiff, nextAiff, cleanupAiff, name)


# done
#go_rex(factorySounds, Location(202, 374), "musicloops.txt", 45)
#go_rex(factorySounds, Location(234, 301), "percloops.txt", 258)
#go_rex(factorySounds, Location(238, 284), "instloops.txt", 734)
#go_rex(factorySounds, Location(218, 258), "drumloops.txt", 1717)
#go_aiff(factorySounds, Location(201, 374), "factory_aiff.txt", 55)    


go_rex(Location(54, 484), None, "flatpack", 624)
go_rex(Location(46, 520), None, "akai", 784)
go_rex(Location(70, 556), None, "analogmonster", 77)
go_rex(Location(40, 700), None, "peff", 65)
go_rex(Location(67, 718), None, "Propellerhead", 1492)

reasonRefills=Location(65, 753)

go_rex(reasonRefills, Location(228, 213), "ACCESS_VIRUSES", 47)
go_aif(reasonRefills, Location(215, 302), "celtic_flavours", 513)
go_rex(reasonRefills, Location(225, 337), "RexDrumloops", 1200)
go_rex(reasonRefills, Location(239, 355), "drumnbassSensations", 63)
go_rex(reasonRefills, Location(206, 392), "funkmaster", 655)
go_rex(reasonRefills, Location(281, 518), "AMG_Drumnbass", 562)
go_rex(reasonRefills, Location(234, 572), "Rex_Noize_Loops", 293)
go_wav(reasonRefills, Location(244, 644), "the_dark_side_of_triphop", 246)
go_rex(reasonRefills, Location(204, 660), "VIROLOGY", 80)
go_wav(reasonRefills, Location(227, 680), "Vocals_loop_sample", 1675)
go_wav(reasonRefills, Location(241, 716), "arabian_traditions", 326)
go_rex(reasonRefills, Location(215, 733), "world_of_rex_2", 988)

go_rex(Location(48, 771), None, "Roland_rex", 78)
go_rex(Location(63, 790), None, "SonicReality_rex", 811)
# go_wav(Location(71, 755), None, "Symphony_of_voices", 811)


#go(rexDrumLoops, "drumloops.txt", 2)
#go(rexPercLoops, "percloops.txt", 2)
#go(rexInstLoops, "instloops.txt", 2)
#go(rexMusicLoops, "musicloops.txt", 2)
