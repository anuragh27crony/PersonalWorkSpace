import org.apache.log4j.Logger;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Arrays;

/**
 * Created by amala on 27-03-2017.
 */
public class BarCode {
    private final static Logger logger = Logger.getLogger(BarCode.class);
    public static String logFileName = "";

    public static void main(String[] args) {


        VideoUtils videoUtils = new VideoUtils();
        Path resourcesPath = Paths.get(System.getProperty("user.dir"), "resources");
        AnalyzeVideos(videoUtils, resourcesPath);
//        String path = "D:\\GitRepos\\PersonalWorkSpace\\IdeaProjects\\ZxingTest\\resources\\Frames\\";
//        videoUtils.analyzeExtractedFrames(100, 1800, path, "out", ".png");


//        createBarCodes(videoUtils,resourcesPath);

    }


    public static void createBarCodes(VideoUtils videoUtils, Path resourcesPath) {
        String barCodeDirPath = Paths.get(resourcesPath.toString(), "Barcodes").toString();

        File barCodesDir = new File(barCodeDirPath);
        if (!barCodesDir.exists())
            System.out.println(barCodesDir.mkdirs());

        videoUtils.CreateBarCodeImages(1, 9000, barCodeDirPath, "img_", "png", 300, 350);
    }

    public static void AnalyzeVideos(VideoUtils videoUtils, Path resourcesPath) {
        String recorderVideosPath = Paths.get(resourcesPath.toString(), "RecordedVideos").toString();
        File f = new File(recorderVideosPath);
        ArrayList<String> videoFiles = new ArrayList<String>(Arrays.asList(f.list()));

        for (String videoFile : videoFiles) {
            logFileName = videoFile;
            logger.info(">>>>>>>>>>>>>>>>>>>>> " + videoFile.toUpperCase() + " >>>>>>>>>>>>>>>>>>>>>");
            String videoFilePath = Paths.get(recorderVideosPath, videoFile).toString();
            String extractedFramesDir = videoUtils.extractFramesFromVideo(resourcesPath, videoFilePath, videoFile.substring(0, videoFile.length() - 4));
            videoUtils.analyzeExtractedFrames(1, 1800, extractedFramesDir, "img_", ".png");
        }
    }

}
