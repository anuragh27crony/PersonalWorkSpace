import com.google.zxing.BarcodeFormat;
import com.google.zxing.NotFoundException;
import com.google.zxing.WriterException;

import java.io.File;
import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

/**
 * Created by amala on 30-03-2017.
 */
public class VideoUtils {

    public String extractFramesFromVideo(Path resourcesPath, String sourceVideoPath, String videoFileName) {

        Runtime rt = Runtime.getRuntime();

        String destinationFolder = Paths.get(resourcesPath.toString(), "Frames", videoFileName).toString();

        File destinationDir = new File(destinationFolder);
        if (!destinationDir.exists())
            System.out.println(destinationDir.mkdirs());

        String imgDirPath = Paths.get(destinationFolder, "img_%d.jpg").toString();

        String command = "ffmpeg -i " + sourceVideoPath + " " + imgDirPath;

        try {
            Process ffmpegProcess = rt.exec(command);
            int retVal = ffmpegProcess.waitFor();

            System.out.println(videoFileName + ":" + retVal);
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
        }
        return destinationFolder;
    }

    public void analyzeExtractedFrames(int startSequence, int limit, String directoryPath, String imgFile, String imgExt) {
        ReadBarCode barcodeReader = new ReadBarCode();
        int previousCounter = 0, repeatedFrames = 0, skippedFrames = 0;

        while (startSequence <= limit) {
            String filePath = Paths.get(directoryPath, imgFile + startSequence + imgExt).toString();
            try {

                StringBuffer output = new StringBuffer(barcodeReader.readBarCode(filePath));
                int currentCounter = Integer.parseInt(output.deleteCharAt(output.length() - 1).toString());

                int frameDiff = currentCounter - previousCounter;

                if (frameDiff > 1) {
                    skippedFrames += frameDiff - 1;
                    System.out.println(currentCounter + "-" + previousCounter);
                } else if (frameDiff < 1) {
                    repeatedFrames++;
                    System.out.println(currentCounter);
                }
                previousCounter = currentCounter;
            } catch (IOException | NotFoundException e) {
                e.printStackTrace();
            }
            startSequence++;
        }

        System.out.println("Repeated Frames:- " + repeatedFrames);
        System.out.println("Skipped Frames:- " + skippedFrames);
    }

    public void CreateBarCodeImages(int startSeqeunce, int limit, String directoryPath, String imgFile, String imgExt, int height, int width) {
        WriteBarCode barCodeWriter = new WriteBarCode();

        while (startSeqeunce <= limit) {
            String dataContents = String.format("%011d", startSeqeunce);
            String filePath = Paths.get(directoryPath, imgFile + startSeqeunce + "."+imgExt).toString();
            try {
                barCodeWriter.createBarCode(dataContents, BarcodeFormat.UPC_A, filePath, imgExt, height, width);
            } catch (WriterException | IOException e) {
                e.printStackTrace();
            }
            startSeqeunce++;
        }
    }
}
