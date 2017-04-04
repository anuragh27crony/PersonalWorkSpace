import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by amala on 27-03-2017.
 */
public class BarCode {
    private final static Logger logger = LoggerFactory.getLogger(BarCode.class);

    public static void main(String[] args) {
        logger.info("=====================================================================================");
        VideoUtils videoUtils = new VideoUtils();
        Path resourcesPath = Paths.get(System.getProperty("user.dir"), "resources");
        int frameRate = 24, durationInSec = 60;

        analyzeRecordedVideos(videoUtils, resourcesPath, frameRate, durationInSec);

        //        createBarCodes(videoUtils,resourcesPath);
    }


    public static void analyzeRecordedVideos(VideoUtils videoUtils, Path resourcesPath, int frameRate, int duration) {
        String imgFileExt = ".png";
        String imgFilePrefix = "img_";
        int totalExpectedFrames = frameRate * duration;

        String recorderVideosPath = Paths.get(resourcesPath.toString(), "RecordedVideos").toString();
        File f = new File(recorderVideosPath);
        ArrayList<String> videoFiles = new ArrayList<String>(Arrays.asList(f.list()));

        if (videoFiles.isEmpty())
            logger.error("No Video Files to Analyze");
        else {
            for (String videoFile : videoFiles) {
                logger.info(">>>>>>>>>>>>>>>>>>>>>\t" + videoFile.toUpperCase() + "\t>>>>>>>>>>>>>>>>>>>>>");

                String videoFilePath = Paths.get(recorderVideosPath, videoFile).toString();
                String videoFileName = videoFile.substring(0, videoFile.length() - 4);

                //Extract Frames from a Video File
                String extractedFramesDir = videoUtils.extractFramesFromVideo(resourcesPath, videoFileName, videoFilePath, imgFilePrefix, imgFileExt);

                //Analyze Barcodes in Extracted Frames
                videoUtils.analyzeExtractedFrames(1, totalExpectedFrames, extractedFramesDir, imgFilePrefix, imgFileExt);

                logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<");
            }
        }
    }

    public static void createBarCodes(VideoUtils videoUtils, Path resourcesPath, int frameRate, int duration, String imgFilePrefix, String imgFileExt) {
        String barCodeDirPath = Paths.get(resourcesPath.toString(), "Barcodes").toString();
        int height = 300, width = 350;
        int totalBarCodes = frameRate * duration;

        File barCodesDir = new File(barCodeDirPath);
        if (!barCodesDir.exists())
            logger.info(barCodesDir.getAbsolutePath() + " Directory Creation :" + barCodesDir.mkdirs());

        videoUtils.CreateBarCodeImages(1, totalBarCodes, barCodeDirPath, imgFilePrefix, imgFileExt, height, width);
    }
}
