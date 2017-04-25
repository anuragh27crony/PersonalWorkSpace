package POJO;

import java.util.List;

/**
 * Created by amala on 05-04-2017.
 */
public class ShowPackets {
    private List<Packets> packets;

    public int getTotalPackets() {
        return packets.size();
    }

    public class Packets {
        public int duration;
        public String duration_time;
        public String pts_time;
        public String dts_time;
    }
}

