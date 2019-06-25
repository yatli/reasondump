open System
open System.IO
open NAudio.Wave
open NAudio.Wave.Asio

type DirectoryInfo =
    {
        files: string list
        // sorted, full name
        recordings: string list
        // sorted
        recordingIds: int list
        // defaults to 1
        lastRecordingId: int
        // requires both directory "indexname" and the index file "indexname.txt"
        indexes: string list
    }

let getDirectoryInfo dir =
    let currentDirectoryFiles = 
        Directory.GetFiles(dir)
        |> Seq.map Path.GetFullPath
        |> List.ofSeq
    let existingRecordings =
        currentDirectoryFiles
        |> List.filter (fun x -> x.EndsWith(".wav"))
        |> List.sort
    let existingRecordingIds = 
        existingRecordings
        |> List.map Path.GetFileName
        |> List.map(fun x -> x.Substring(10, x.Length - 14) |> Int32.Parse)
        |> List.sort
    let lastRecordingId = List.max (1::existingRecordingIds)
    let recordingIndexes =
        currentDirectoryFiles
        |> List.filter (fun x -> x.EndsWith(".txt"))
        |> List.map (fun x -> x.Substring(0, x.Length - 4))

    {
        files = currentDirectoryFiles
        recordings = existingRecordings
        recordingIds = existingRecordingIds
        lastRecordingId = lastRecordingId
        indexes = recordingIndexes
    }

let mutable notSilentTime = DateTime.Now
let mutable rmsReportTime = DateTime.Now
let silentPeriod = TimeSpan.FromSeconds(1.0)
let fileMinPeriod = TimeSpan.FromSeconds(3.0)
let rmsReportPeriod = TimeSpan.FromSeconds(3.0)

let splLevelThreshold = -80.0f
let mutable filePeakLevel = -90.0f
let mutable fileId = 1
let mutable (fileWriter: WaveFileWriter) = null
let mutable showSilentClip = false
let mutable continuousSilentClips = 0

let bufSize = 1024 * 1024
let buf = Array.zeroCreate (1024 * 16)
let mutable fileBuf: single[] = Array.zeroCreate bufSize
let mutable fileBufIndex = 0
let mutable fileStartTime = DateTime.Now
let mutable nch = 1
let pow2 x = x * x

type WriteAction = 
| Write of WaveFileWriter * single[] * int * int
| Close of WaveFileWriter
| Discard of WaveFileWriter

let actionQueue = System.Collections.Concurrent.ConcurrentQueue<WriteAction>()
let getRecordingName = sprintf "recording_%06d.wav"

let newWaveFile() =
    if fileWriter = null then ()
    elif filePeakLevel < splLevelThreshold then
        continuousSilentClips <- continuousSilentClips + 1
        if continuousSilentClips > 100 then
            Environment.Exit(0)
        Console.Clear()
        showSilentClip <- true
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "================================================="
        printfn "Dropping silent clip (peak = %A)..." filePeakLevel
        actionQueue.Enqueue(Discard fileWriter)
    else
        printfn "Finishing clip (peak = %A)." filePeakLevel
        continuousSilentClips <- 0
        actionQueue.Enqueue(Close fileWriter)

    fileId <- fileId + 1
    let filename = getRecordingName fileId
    fileWriter <- new WaveFileWriter(filename, WaveFormat.CreateIeeeFloatWaveFormat(44100, nch))
    notSilentTime <- DateTime.Now
    fileStartTime <- DateTime.Now
    filePeakLevel <- -90.0f

let calcAudioLevel (buf: single[]) cnt nch =
    let mutable i = 0
    let mutable rms = 0.0f
    while i < cnt do
        rms <- rms + pow2 buf.[i]
        i <- i + nch
    let n = single(cnt / nch)
    20.0f * log10(sqrt(rms / n))

let onAudio (e: AsioAudioAvailableEventArgs) =
    let cnt = e.GetAsInterleavedSamples(buf)
    let now = DateTime.Now
    let level = calcAudioLevel buf cnt nch

    // copy sample to file buffer
    if fileBuf.Length - fileBufIndex <= cnt then
        fileBuf <- Array.zeroCreate bufSize
        fileBufIndex <- 0
    Array.Copy(buf, 0, fileBuf, fileBufIndex, cnt)
    // submit the write action
    actionQueue.Enqueue(Write(fileWriter, fileBuf, fileBufIndex, cnt))
    fileBufIndex <- fileBufIndex + cnt
    // update peak level
    filePeakLevel <- max filePeakLevel level

    if (now - rmsReportTime) > rmsReportPeriod then
        (*printfn "Current level = %A" level*)
        rmsReportTime <- now

    if level < splLevelThreshold then
        if (now - notSilentTime) > silentPeriod && (now - fileStartTime) > fileMinPeriod then
            newWaveFile()
    else
        notSilentTime <- now
        if showSilentClip then
            showSilentClip <- false
            Console.Clear()
            printfn "================================================="
            printfn "=================             ==================="
            printfn "========                               =========="
            printfn "====                                       ======"
            printfn "==                                           ===="
            printfn "=                                             ==="
            printfn "=                                             ==="
            printfn "==                                           ===="
            printfn "====                                       ======"
            printfn "=======                                =========="
            printfn "=================            ===================="
            printfn "================================================="
    ()

let scan index =
    printfn "scan: %s" index
    let info = getDirectoryInfo index
    let existingFileIds = List.sort info.recordingIds
    let mutable start = 0
    let mutable last = -1
    for x in existingFileIds do
        if x <> last + 1 then
            if last - start > 0 then
                printfn "conseq: %d - %d" start last
                for i = start + 1 to last do
                    let f = Path.Combine(index, getRecordingName i)
                    printfn "deleting %s" f
                    try File.Delete(f)
                    with _ -> ()
            start <- x
        last <- x

let join index =
    printfn "join: %s" index
    let info = getDirectoryInfo index
    let sampleNames = File.ReadAllLines (index+".txt") |> List.ofSeq
    let namelistLen, filelistLen =
        List.length sampleNames, List.length info.recordings 
    if  namelistLen <> filelistLen then
        printfn "join: %s sampleNames length (%d) mismatch with recordings (%d)!" index namelistLen filelistLen
    else
    for (recording,name) in List.zip info.recordings sampleNames do
        let target = Path.Combine(index, name + ".wav")
        if File.Exists(target) then
            printfn "!! file already exists: %s" target
        else
            printfn "%-30s -> %s.wav" (Path.GetFileName recording) name
            File.Move(recording, Path.Combine(index, target))

let waveWriteProc() =
    while true do
        match actionQueue.TryDequeue() with
        | true, Write(writer, buf, idx, cnt) ->
            writer.WriteSamples(buf, idx, cnt)
        | true, Close(writer) -> 
            writer.Dispose()
        | true, Discard(writer) ->
            writer.Dispose()
            try File.Delete(writer.Filename)
            with _ -> ()
        | _ -> ()

let sample() =
    newWaveFile()
    let writeThread = Threading.Thread(waveWriteProc)
    writeThread.Start()

    use asio = new AsioOut("Focusrite USB ASIO")
    asio.InputChannelOffset <- 4
    asio.InitRecordAndPlayback(null, nch, 44100)
    asio.AudioAvailable.Add onAudio
    printfn "Listening to %d channels" nch
    printfn "Buffer size = %d" asio.FramesPerBuffer 
    asio.Play()
    ignore <| Console.ReadLine()

[<EntryPoint>]
[<STAThread>]
let main argv =
    let info = getDirectoryInfo "."

    printfn "Last file id is: %d" info.lastRecordingId
    fileId <- info.lastRecordingId + 1

    match argv with
    | [| "--sample" |] ->
        nch <- 2
        sample()
    | [|"--scan"|] ->
        info.indexes |> List.iter scan
    | [|"--join"|] ->
        info.indexes |> List.iter join
    | _ -> ()

    0

