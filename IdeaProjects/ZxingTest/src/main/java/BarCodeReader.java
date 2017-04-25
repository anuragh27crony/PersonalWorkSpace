import com.google.zxing.*;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.HybridBinarizer;

import javax.imageio.ImageIO;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.EnumMap;
import java.util.EnumSet;
import java.util.Map;

/**
 * Created by amala on 30-03-2017.
 */
public class BarCodeReader {
    public String readBarCode(String filePath) throws IOException, NotFoundException, ArrayIndexOutOfBoundsException {

        Map<DecodeHintType, Object> hintsMap = new EnumMap<DecodeHintType, Object>(DecodeHintType.class);
        hintsMap.put(DecodeHintType.TRY_HARDER, Boolean.TRUE);
        hintsMap.put(DecodeHintType.POSSIBLE_FORMATS, EnumSet.allOf(BarcodeFormat.class));
        hintsMap.put(DecodeHintType.PURE_BARCODE, Boolean.FALSE);

        BinaryBitmap binaryBitmap = new BinaryBitmap(new HybridBinarizer(new BufferedImageLuminanceSource(ImageIO.read(new FileInputStream(filePath)))));
        Result barCode = new MultiFormatReader().decode(binaryBitmap, hintsMap);
        return barCode.getText();
    }
}
