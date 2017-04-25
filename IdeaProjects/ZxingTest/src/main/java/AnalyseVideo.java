import POJO.FilePathConstants;
import org.apache.commons.io.FileUtils;
import org.apache.log4j.Logger;

import java.io.File;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by amala on 27-03-2017.
 */
public class AnalyseVideo {
    private final static Logger logger = Logger.getLogger(AnalyseVideo.class);

    public static void main(String[] args) {
        logger.info("=====================================================================================");
        VideoUtils videoUtils = new VideoUtils();
        int frameRate = 25, durationInSec = 60;

        analyzeRecordedVideos(videoUtils, frameRate, durationInSec);
    }


    public static void analyzeRecordedVideos(VideoUtils videoUtils, int frameRate, int duration) {
        String imgFileExt = ".png";
        String imgFilePrefix = "img_";
        int totalExpectedFrames = frameRate * duration;

        String recorderVideosPath = FilePathConstants.recordedVideosDirPath.toString();
        File f = new File(recorderVideosPath);
        ArrayList<String> videoFiles = new ArrayList<>(Arrays.asList(f.list()));

        if (videoFiles.isEmpty())
            logger.error("No Video Files to Analyze");
        else {
            for (String videoFile : videoFiles) {
                logger.info(">>>>>>>>>>>>>>>>>>>>>\t" + videoFile.toUpperCase() + "\t>>>>>>>>>>>>>>>>>>>>>");

                String videoFilePath = Paths.get(recorderVideosPath, videoFile).toString();
                String videoFileName = videoFile.substring(0, videoFile.length() - 4);

                //Extract Frames from a Video File
                String extractedFramesDir = videoUtils.extractFramesFromVideo(videoFilePath, videoFileName, imgFilePrefix, imgFileExt);

                //Analyze Barcodes in Extracted Frames
                Boolean errorFlag = videoUtils.analyzeExtractedFrames(1, totalExpectedFrames, extractedFramesDir, imgFilePrefix, imgFileExt);

                if (!errorFlag) {
                    try {
                        File deleteDir = new File(extractedFramesDir);
                        deleteDir.setWritable(Boolean.TRUE);
                        System.gc();
                        FileUtils.forceDeleteOnExit(deleteDir);
                    } catch (IOException e) {
                        logger.error(e.getMessage(), e);
                    }
                }
                logger.info("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<");
            }
        }
    }
}