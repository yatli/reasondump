import shutil
import os

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
        try:
            section = list(section)
        except:
            section = [section]
            pass
        for s in section:
            s.doubleClick()
            sleep(3)
    searchTextbox.click()
    type(searchItem + Key.ENTER)
    sleep(3)
    # double click first entry
    Location(228, 186).doubleClick()

def go_dump(readProc, nextProc, cleanupProc, name, nr):
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
    # run the cleanup proc
    cleanupProc()
    # then, move all the dumped samples into a folder
    target_dir = "recorder/"+name
    try:
        os.mkdir(target_dir)
    except:
        print "failed to create directory: "+name
    try:
        files = [x for x in os.listdir('recorder/') if x.endswith('.wav')]
        for x in files:
            try:
                shutil.move('recorder/' + x, target_dir)
                print x + " -> " + target_dir
            except:
                print "failed to move file: "+x
    except:
        print "failed to list directory 'recorder'"


def go_rex(folder, section, name, nr):
    if userInterrupt:
        return
    go_nav(folder, section, ".rx2")
    sleep(5)
    # now, the first rex loop is loaded, and a OctoRex is created.
    go_dump(readRex, nextRex, cleanupRex, name, nr)


def go_aif(section, name, nr):
    if userInterrupt:
        return
    go_nav(folder, section, ".aif")
    sleep(2)
    # now, the first aiff is loaded, and an audio track is created.
    go_dump(readAiff, nextAiff, cleanupAiff, name, nr)

def go_wav(section, name, nr):
    if userInterrupt:
        return
    go_nav(folder, section, ".wav")
    sleep(2)
    # now, the first aiff is loaded, and an audio track is created.
    go_dump(readAiff, nextAiff, cleanupAiff, name, nr)


# done
#go_rex(factorySounds, Location(202, 374), "musicloops.txt", 45)
#go_rex(factorySounds, Location(234, 301), "percloops.txt", 258)
#go_rex(factorySounds, Location(238, 284), "instloops.txt", 734)
#go_rex(factorySounds, Location(218, 258), "drumloops.txt", 1717)
#go_aif(factorySounds, Location(201, 374), "factory_aiff.txt", 55)    


go_rex(Location(54, 484), None, "flatpack", 624)
go_rex(Location(46, 520), None, "akai", 784)
go_rex(Location(70, 556), None, "analogmonster", 77)
go_rex(Location(40, 700), None, "peff", 65)
go_rex(Location(67, 718), None, "Propellerhead", 1492)

reasonRefills=Location(65, 753)

go_rex(reasonRefills, Location(228, 230), "ACCESS_VIRUSES", 47)
go_aif(reasonRefills, Location(215, 319), "celtic_flavours", 513)
go_rex(reasonRefills, Location(225, 354), "RexDrumloops", 1200)
go_rex(reasonRefills, Location(239, 373), "drumnbassSensations", 63)
go_rex(reasonRefills, Location(206, 409), "funkmaster", 655)
go_rex(reasonRefills, Location(281, 535), "AMG_Drumnbass", 562)
go_rex(reasonRefills, Location(234, 572), "Rex_Noize_Loops", 293)
go_wav(reasonRefills, Location(244, 644), "the_dark_side_of_triphop", 246)
go_rex(reasonRefills, Location(204, 660), "VIROLOGY", 80)
go_wav(reasonRefills, Location(227, 680), "Vocals_loop_sample", 1675)
go_wav(reasonRefills, Location(241, 716), "arabian_traditions", 326)
go_rex(reasonRefills, Location(215, 733), "world_of_rex_2", 988)

go_rex(Location(48, 771), None, "Roland_rex", 78)
go_rex(Location(63, 790), None, "SonicReality_rex", 811)

zeroG = Location(49, 916)
totalRex2 = Location(218, 302)

go_rex(zeroG, [totalRex2, Location(221, 194)], "totalRex_PureBrazilieanBeats", 194)
go_rex(zeroG, [totalRex2, Location(205, 211)], "totalRex_PureHiphop", 146)
go_rex(zeroG, [totalRex2, Location(204, 229)], "totalRex_PureMayhem", 340)
go_rex(zeroG, [totalRex2, Location(196, 247)], "totalRex_PureRnB", 195)
go_rex(zeroG, [totalRex2, Location(196, 267)], "totalRex_PureTabla", 274)
go_rex(zeroG, [totalRex2, Location(203, 284)], "totalRex_PureTriphop", 147)
go_rex(zeroG, [totalRex2, Location(219, 301)], "totalRex_reggae_connection", 194)
go_rex(zeroG, [totalRex2, Location(247, 319)], "totalRex_return_to_plannet_of_the_break", 142)
go_rex(zeroG, [totalRex2, Location(228, 336)], "totalRex_rhythmGuitar_fx", 248)
go_rex(zeroG, [totalRex2, Location(206, 355)], "totalRex_species_of_india", 200)
go_rex(zeroG, [totalRex2, Location(213, 374)], "totalRex_synthbassloops", 14)
go_rex(zeroG, [totalRex2, Location(211, 393)], "totalRex_techno_prisoners", 36)
go_rex(zeroG, [totalRex2, Location(218, 409)], "totalRex_total_drumandbass", 782)
go_rex(zeroG, [totalRex2, Location(209, 427)], "totalRex_total_funk", 910)
go_rex(zeroG, [totalRex2, Location(205, 444)], "totalRex_total_hiphop", 552)
go_rex(zeroG, [totalRex2, Location(201, 464)], "totalRex_total_house", 668)
go_rex(zeroG, [totalRex2, Location(215, 482)], "totalRex_trance_formation", 15)
go_rex(zeroG, [totalRex2, Location(220, 500)], "totalRex_upfront_lead_guitar", 44)
go_rex(zeroG, [totalRex2, Location(250, 518)], "totalRex_WIRED_the_element_of_trance", 928)
go_rex(zeroG, [totalRex2, Location(220, 536)], "totalRex_world_class_breaks", 200)

#go(rexDrumLoops, "drumloops.txt", 2)
#go(rexPercLoops, "percloops.txt", 2)
#go(rexInstLoops, "instloops.txt", 2)
#go(rexMusicLoops, "musicloops.txt", 2)
