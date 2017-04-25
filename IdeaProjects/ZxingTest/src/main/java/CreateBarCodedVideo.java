import POJO.FilePathConstants;
import org.apache.log4j.Logger;

import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Created by amala on 05-04-2017.
 */
public class CreateBarCodedVideo {
    private final static Logger logger = Logger.getLogger(CreateBarCodedVideo.class);

    public static void main(String[] args) {
        logger.info("=====================================================================================");
        VideoUtils videoUtils = new VideoUtils();
        Path resourcesPath = Paths.get(System.getProperty("user.dir"), "resources");
        int frameRate = 25, durationInSec = 1800;
        String imgFilePrefix = "img_";
        String imgFileExt = "png";

        createBarCodedVideo(videoUtils, resourcesPath, frameRate, durationInSec, imgFilePrefix, imgFileExt);
    }

    public static void createBarCodedVideo(VideoUtils videoUtils, Path resourcesPath, int frameRate, int duration, String imgFilePrefix, String imgFileExt) {
        String barCodeDirPath = Paths.get(resourcesPath.toString(), "Barcodes").toString();
        int height = 700, width = 750;
        int totalBarCodes = frameRate * duration;
        System.out.println(totalBarCodes);

        FilePathConstants.checkAndCreateDir(barCodeDirPath);

//        videoUtils.CreateBarCodeImages(1, totalBarCodes, barCodeDirPath, imgFilePrefix, imgFileExt, height, width);
        videoUtils.stitchFramesToVideo(imgFilePrefix, "." + imgFileExt);
    }
}
