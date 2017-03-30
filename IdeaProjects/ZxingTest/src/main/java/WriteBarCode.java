import com.google.zxing.BarcodeFormat;
import com.google.zxing.MultiFormatWriter;
import com.google.zxing.WriterException;
import com.google.zxing.client.j2se.MatrixToImageWriter;
import com.google.zxing.common.BitMatrix;

import java.io.File;
import java.io.IOException;

/**
 * Created by amala on 30-03-2017.
 */
public class WriteBarCode {
    public void createBarCode(String contents, BarcodeFormat barcodeFormat, String filePath, String fileFormat, int height, int width)
            throws WriterException, IOException {
        String encodedContent = new String(contents.getBytes("UTF-8"), "UTF-8");
        BitMatrix matrixData = new MultiFormatWriter().encode(encodedContent, barcodeFormat, width, height, null);
        MatrixToImageWriter.writeToFile(matrixData, fileFormat, new File(filePath));
    }
}
