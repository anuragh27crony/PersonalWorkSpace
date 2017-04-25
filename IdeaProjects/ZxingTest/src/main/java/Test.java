import POJO.ShowFrames;
import POJO.ShowPackets;
import com.google.gson.Gson;

/**
 * Created by amala on 05-04-2017.
 */
public class Test {
    public static void main(String[] args) {

        Gson gson = new Gson();
        String frame_data = "{ \"frames\": [ { \"media_type\": \"video\", \"stream_index\": 0, \"key_frame\": 1, \"pkt_pts\": 0, \"pkt_pts_time\": \"0.000000\", \"pkt_dts\": 0, \"pkt_dts_time\": \"0.000000\", \"best_effort_timestamp\": 0, \"best_effort_timestamp_time\": \"0.000000\", \"pkt_duration\": 512, \"pkt_duration_time\": \"0.033333\", \"pkt_pos\": \"48\", \"pkt_size\": \"6764\", \"width\": 360, \"height\": 240, \"pix_fmt\": \"yuv420p\", \"pict_type\": \"I\", \"coded_picture_number\": 0, \"display_picture_number\": 0, \"interlaced_frame\": 0, \"top_field_first\": 0, \"repeat_pict\": 0 }, { \"media_type\": \"video\", \"stream_index\": 0, \"key_frame\": 0, \"pkt_pts\": 512, \"pkt_pts_time\": \"0.033333\", \"pkt_dts\": 512, \"pkt_dts_time\": \"0.033333\", \"best_effort_timestamp\": 512, \"best_effort_timestamp_time\": \"0.033333\", \"pkt_duration\": 512, \"pkt_duration_time\": \"0.033333\", \"pkt_pos\": \"6812\", \"pkt_size\": \"1453\", \"width\": 360, \"height\": 240, \"pix_fmt\": \"yuv420p\", \"pict_type\": \"P\", \"coded_picture_number\": 1, \"display_picture_number\": 0, \"interlaced_frame\": 0, \"top_field_first\": 0, \"repeat_pict\": 0 }],\"format\": { \"filename\": \"D:\\\\GitRepos\\\\PersonalWorkSpace\\\\IdeaProjects\\\\ZxingTest\\\\resources\\\\RecordedVideos\\\\WCTOSPREY08W170404124700_04.MP4\", \"nb_streams\": 1, \"nb_programs\": 0, \"format_name\": \"mov,mp4,m4a,3gp,3g2,mj2\", \"format_long_name\": \"QuickTime / MOV\", \"start_time\": \"0.000000\", \"duration\": \"60.000000\", \"size\": \"5521465\", \"bit_rate\": \"736195\", \"probe_score\": 100, \"tags\": { \"major_brand\": \"isom\", \"minor_version\": \"512\", \"compatible_brands\": \"isomiso2avc1mp41\", \"encoder\": \"Lavf57.56.100\" }} }";

        ShowFrames datasets = gson.fromJson(frame_data, ShowFrames.class);

        for (ShowFrames.Frame frame : datasets.frames) {
            System.out.println(frame.coded_picture_number);
        }


        String packet_data = "{ \"packets\": [ { \"codec_type\": \"video\", \"stream_index\": 0, \"pts\": 0, \"pts_time\": \"0.000000\", \"dts\": 0, \"dts_time\": \"0.000000\", \"duration\": 512, \"duration_time\": \"0.033333\", \"size\": \"6764\", \"pos\": \"48\", \"flags\": \"K\" }, { \"codec_type\": \"video\", \"stream_index\": 0, \"pts\": 512, \"pts_time\": \"0.033333\", \"dts\": 512, \"dts_time\": \"0.033333\", \"duration\": 512, \"duration_time\": \"0.033333\", \"size\": \"1453\", \"pos\": \"6812\", \"flags\": \"_\" }] }";


        ShowPackets packetDataset = gson.fromJson(packet_data, ShowPackets.class);
        System.out.println("Total Packets:" + packetDataset.getTotalPackets());
    }
}
