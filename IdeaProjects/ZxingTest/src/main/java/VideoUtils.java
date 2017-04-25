import POJO.FilePathConstants;
import POJO.VideoFrame;
import com.google.gson.Gson;
import com.google.zxing.BarcodeFormat;
import com.google.zxing.NotFoundException;
import com.google.zxing.WriterException;
import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.file.Paths;
import java.util.StringJoiner;

/**
 * Created by amala on 30-03-2017.
 */
public class VideoUtils {
    private final static Logger logger = Logger.getLogger(VideoUtils.class);
    private final Gson gsonInstance = new Gson();


    public void probeVideoFrames(String videoFilePath) {
        String jsonFilePath = "";
        ProcessBuilder builder = new ProcessBuilder("cmd", "/c", "ffprobe", "-print_format", "json", "-show_format", "-show_frames", videoFilePath, ">", jsonFilePath);
        builder.redirectErrorStream(true);

        try {
            final Process process = builder.start();
            watchProcess(process);
            gsonInstance.fromJson(jsonFilePath, VideoFrame.class);
        } catch (IllegalStateException | IOException e) {
            logger.error(e.getMessage(), e);
        }
    }

    public void watchProcess(Process process) {
        Thread t = new Thread() {
            public void run() {
                InputStream stderr = process.getErrorStream();
                InputStreamReader isr = new InputStreamReader(stderr);
                BufferedReader error = new BufferedReader(isr);
                BufferedReader input = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line = null;

                try {
                    while ((line = error.readLine()) != null)
                        logger.error(line);

                    int exitVal = process.waitFor();
                    logger.error("Process exitValue: " + exitVal);

                    while ((line = input.readLine()) != null) {
                        logger.info(line);
                    }
                } catch (IOException | InterruptedException e) {
                    logger.error(e.getMessage(), e);
                }
            }
        };
        t.start();
        try {
            t.join();
        } catch (InterruptedException e) {
            logger.error(e.getMessage(), e);
        }
    }


    public String extractFramesFromVideo(String sourceVideoPath, String videoFileName, String frameFilePrefix, String frameFileExt) {

        String videoSpecificFramesDir = Paths.get(FilePathConstants.framesDirPath.toString(), videoFileName).toString();
        FilePathConstants.checkAndCreateDir(videoSpecificFramesDir);

        String framesFilePath = Paths.get(videoSpecificFramesDir, frameFilePrefix + "%d" + frameFileExt).toString();
        ProcessBuilder builder = new ProcessBuilder("cmd", "/c", "ffmpeg", "-i", sourceVideoPath, framesFilePath);
        builder.redirectErrorStream(true);

        try {
            final Process process = builder.start();
            watchProcess(process);
        } catch (IllegalStateException | IOException e) {
            logger.error(e.getMessage(), e);
        }
        return videoSpecificFramesDir;
    }

    public boolean analyzeExtractedFrames(int startSequence, int limit, String directoryPath, String imgFile, String imgExt) {
        Boolean errorFlag = Boolean.FALSE;

        BarCodeReader barcodeReader = new BarCodeReader();
        int previousCounter = 0, frameDiff = 0;
        int repeatedFrames = 0, skippedFrames = 0;
        Boolean firstIter = Boolean.TRUE;


        while (startSequence <= limit) {
            String filePath = Paths.get(directoryPath, imgFile + startSequence + imgExt).toString();
            try {
                StringBuffer output = new StringBuffer(barcodeReader.readBarCode(filePath));
                int currentCounter = Integer.parseInt(output.deleteCharAt(output.length() - 1).toString());

                if (!firstIter) {
                    frameDiff = currentCounter - previousCounter;
                    logger.trace(currentCounter + "-" + previousCounter + ":" + frameDiff);
                    if (frameDiff > 1) {
                        skippedFrames += frameDiff - 1;
                        logger.info("SKIPPED FRAME SEQUENCE: " + currentCounter + "-" + previousCounter);
                        errorFlag = Boolean.TRUE;
                    } else if (frameDiff < 1) {
                        repeatedFrames++;
                        logger.info("REPEATED FRAME SEQUENCE: " + currentCounter + "-" + previousCounter);
                        errorFlag = Boolean.TRUE;
                    }
                }
                previousCounter = currentCounter;
                if (firstIter)
                    firstIter = Boolean.FALSE;
            } catch (IOException | NotFoundException | NumberFormatException | ArrayIndexOutOfBoundsException e) {
                logger.error("startSequence :" + startSequence);
                logger.error(e.getMessage(), e);
                errorFlag = Boolean.TRUE;
            }
            startSequence++;
        }

        logger.info("TOTAL REPEATED FRAMES: " + repeatedFrames);
        logger.info("TOTAL SKIPPED FRAMES: " + skippedFrames);
        return errorFlag;
    }

    public void CreateBarCodeImages(int startSeqeunce, int limit, String directoryPath, String imgFile, String imgExt, int height, int width) {
        BarCodeWriter barCodeWriter = new BarCodeWriter();

        while (startSeqeunce <= limit) {
            String dataContents = String.format("%011d", startSeqeunce);
            String filePath = Paths.get(directoryPath, imgFile + startSeqeunce + "." + imgExt).toString();
            try {
                barCodeWriter.createBarCode(dataContents, BarcodeFormat.UPC_A, filePath, imgExt, height, width);
            } catch (WriterException | IOException e) {
                logger.error(e.getMessage(), e);
            }
            startSeqeunce++;
        }
    }

    public void stitchFramesToVideo(String barCodeImgFilePrefix, String barCodeImgFileExt) {

        String barCodeImagesPath = Paths.get(FilePathConstants.barCodeImagesDirPath.toString(), barCodeImgFilePrefix + "%d" + barCodeImgFileExt).toString();

        String filterGraphOptions = "\"[0:0]drawtext=fontfile=/Windows/Fonts/arial.ttf:timecode=\'00\\:00\\:00\\:00\':rate=1000::fontcolor=white:fontsize=40:x=w-tw-20:y=th+50:box=1:boxcolor=black@0.5:boxborderw=10,format=yuv420p[a];[a][1:0]overlay=0:H/3\"";

        String testSourceOptions = "testsrc=duration=1800:size=1280x720:rate=25";
        String BarcodedVideoFile = Paths.get(FilePathConstants.resourcesDirPath.toString(), "PAL_25_Big_Barcodes.mp4").toString();

        //Create YUV File from BAR CODE FILES (ffmpeg -i %03d.jpg -pix_fmt yuv420p -r 29.97 output.yuv)
        ProcessBuilder builder = new ProcessBuilder("cmd", "ffmpeg", "-f", "lavfi", "-i", testSourceOptions, "-i", barCodeImagesPath, "-filter_complex", filterGraphOptions, "-c:v", "libx264", BarcodedVideoFile);
        StringJoiner command = new StringJoiner(" ");
        for (String arg : builder.command())
            command.add(arg);
        logger.info("Final Command is:" + command.toString());
        builder.redirectErrorStream(true);

        try {
//            final Process process = builder.start();
            Runtime rt = Runtime.getRuntime();
            final Process process = rt.exec(command.toString());
//            rt.
//            process.waitFor();
            watchProcess(process);
        } catch (IllegalStateException | IOException e) {
            logger.error(e.getMessage(), e);
        }
    }
}
