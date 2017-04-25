package POJO;


import org.apache.log4j.Logger;

import java.io.File;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Created by amala on 06-04-2017.
 */
public class FilePathConstants {
    public static final Path resourcesDirPath = Paths.get(System.getProperty("user.dir"), "resources");
    public static final Path framesDirPath = Paths.get(resourcesDirPath.toString(), "Frames");
    public static final Path recordedVideosDirPath = Paths.get(resourcesDirPath.toString(), "RecordedVideos");
    public static final Path barCodeImagesDirPath = Paths.get(resourcesDirPath.toString(), "Barcodes");

    private static final Logger logger = Logger.getLogger(FilePathConstants.class);

    public static boolean checkAndCreateDir(String DirPath) {
        boolean result = Boolean.FALSE;

        File destinationDir = new File(DirPath);
        try {
            if (!destinationDir.exists()) {
                result = destinationDir.mkdirs();
                logger.trace(destinationDir.getAbsolutePath() + " Directory Creation :" + destinationDir.mkdirs());
            } else {
                result = Boolean.TRUE;
            }
        } catch (Exception e) {
            logger.error(e.getMessage(), e);

        }
        return result;

    }
}

