import org.apache.log4j.RollingFileAppender;

import java.util.Random;

/**
 * Created by amala on 31-03-2017.
 */
public class LogFileAppender extends RollingFileAppender {
    @Override
    public void setFile(String fileName) {
        Random random = new Random(new Random().nextInt());
        super.setFile(fileName+random.nextInt());
    }
}
