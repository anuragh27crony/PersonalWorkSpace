package another;

import another.POJO.MessageType;
import com.google.gson.annotations.SerializedName;

/**
 * Created by amala on 25/11/2016.
 */
public class MyBaseTypeModel {
    @SerializedName("message")
    private MessageType msgTypeId;
}
