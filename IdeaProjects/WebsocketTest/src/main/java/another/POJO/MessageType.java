package another.POJO;

import com.google.gson.annotations.SerializedName;

public class MessageType {
    @SerializedName("msgType")
    private MessageTypeEnum msgType = MessageTypeEnum.UNINITIALIZED;
    private String id;

    public MessageType(String messageType, String id) {
        this.msgType = MessageTypeEnum.getMessageTypeByValue(messageType);
        this.id = id;
    }

    public String getMsgId() {
        return id;
    }

    public MessageTypeEnum getMsgType() {
        return msgType;
    }
}