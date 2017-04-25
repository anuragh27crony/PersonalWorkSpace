package POJO;

import java.util.List;

/**
 * Created by amala on 05-04-2017.
 */
public class ShowFrames {
    public List<Frame> frames;

    public class Frame {
        public int coded_picture_number;
        public int pkt_duration;
        public String pkt_duration_time;
    }
}

