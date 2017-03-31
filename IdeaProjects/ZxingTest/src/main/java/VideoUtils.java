import com.google.zxing.BarcodeFormat;
import com.google.zxing.NotFoundException;
import com.google.zxing.WriterException;
import org.apache.log4j.Logger;

import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Created by amala on 30-03-2017.
 */
public class VideoUtils {
    private final static Logger logger = Logger.getLogger(VideoUtils.class);


    public void watchProcess(Process process) {
        Thread t = new Thread() {
            public void run() {
                BufferedReader input = new BufferedReader(new InputStreamReader(process.getInputStream()));
                String line = null;
                try {
                    while ((line = input.readLine()) != null) {
                        logger.info(line);
//                    System.out.println(line);
                    }
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        };
        t.start();
        try {
            t.join();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }


    public String extractFramesFromVideo(Path resourcesPath, String sourceVideoPath, String videoFileName) {


        String destinationFolder = Paths.get(resourcesPath.toString(), "Frames", videoFileName).toString();

        File destinationDir = new File(destinationFolder);
        if (!destinationDir.exists())
            System.out.println(destinationDir.mkdirs());

        String imgDirPath = Paths.get(destinationFolder, "img_%d.png").toString();
        String command = "cmd /c ffmpeg -i " + sourceVideoPath + " " + imgDirPath;
        ProcessBuilder builder = new ProcessBuilder("cmd", "/c", "ffmpeg", "-i", sourceVideoPath, imgDirPath);
        builder.redirectErrorStream(true);

        try {
            final Process process = builder.start();
            watchProcess(process);
        } catch (IllegalStateException e) {
            logger.fatal(e.getMessage(), e);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return destinationFolder;
    }

    public void analyzeExtractedFrames(int startSequence, int limit, String directoryPath, String imgFile, String imgExt) {
        ReadBarCode barcodeReader = new ReadBarCode();
        int previousCounter = 0, repeatedFrames = 0, skippedFrames = 0, frameDiff;
        Boolean firstIter = Boolean.TRUE;

        while (startSequence <= limit) {
            String filePath = Paths.get(directoryPath, imgFile + startSequence + imgExt).toString();
            try {
                StringBuffer output = new StringBuffer(barcodeReader.readBarCode(filePath));
                int currentCounter = Integer.parseInt(output.deleteCharAt(output.length() - 1).toString());

                if (!firstIter) {
                    firstIter = Boolean.FALSE;
                    frameDiff = currentCounter - previousCounter;

                    if (frameDiff > 1) {
                        skippedFrames += frameDiff - 1;
                        logger.info("SKIPPED FRAMES: " + currentCounter + "-" + previousCounter);
                    } else if (frameDiff < 1) {
                        repeatedFrames++;
                        logger.info("REPEATED FRAMES: " + currentCounter + "-" + previousCounter);
                    }
                }
                previousCounter = currentCounter;
            } catch (IOException | NotFoundException | NumberFormatException | ArrayIndexOutOfBoundsException e) {
                logger.fatal(e.getMessage(), e);
            }
            startSequence++;
        }

        logger.info("TOTAL REPEATED FRAMES: " + repeatedFrames);
        logger.info("TOTAL SKIPPED FRAMES: " + skippedFrames);
    }

    public void CreateBarCodeImages(int startSeqeunce, int limit, String directoryPath, String imgFile, String imgExt, int height, int width) {
        WriteBarCode barCodeWriter = new WriteBarCode();

        while (startSeqeunce <= limit) {
            String dataContents = String.format("%011d", startSeqeunce);
            String filePath = Paths.get(directoryPath, imgFile + startSeqeunce + "." + imgExt).toString();
            try {
                barCodeWriter.createBarCode(dataContents, BarcodeFormat.UPC_A, filePath, imgExt, height, width);
            } catch (WriterException | IOException e) {
                logger.fatal(e.getMessage(), e);
            }
            startSeqeunce++;
        }
    }
}
