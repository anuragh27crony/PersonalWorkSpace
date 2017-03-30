package another.POJO;

/**
 * Created by amala on 25/11/2016.
 */
public enum MessageTypeEnum {
    UNINITIALIZED("uninitialized"),
    VIDEO_PROVIDER_REGISTER_REQUEST("videoProviderRegisterRequest"),
    VIDEO_PROVIDER_REGISTER_REPLY("videoProviderRegisterReply"),
    VIDEO_UPLOAD_REQUEST("videoUploadRequest"),
    VIDEO_UPLOAD_REPLY("videoUploadReply"),
    VIDEO_TRANSFER_REQUEST("videoTransferRequest"),
    VIDEO_TRANSFER_REPLY("videoTransferReply"),
    VIDEO_RECORDING_CAPACITY_REQUEST("videoRecordingCapacityRequest"),
    VIDEO_RECORDING_CAPACITY_REPLY("videoRecordingCapacityReply"),
    DETECTOR_PRTG_REQUEST("detectorPRTGRequest"),
    DETECTOR_PRTG_REPLY("detectorPRTGReply"),
    TIME_INFO_REQUEST("timeInfoRequest"),
    TIME_INFO_REPLY("timeInfoReply");

    private final String msgTypeValue;

    public String getMsgTypeValue() {
        return this.msgTypeValue;
    }

    MessageTypeEnum(String typeString) {
        this.msgTypeValue = typeString;
    }

    public static MessageTypeEnum getMessageTypeByValue(String value) {
        for (MessageTypeEnum messageType : MessageTypeEnum.values()) {
            if (messageType.getMsgTypeValue().equals(value))
                return messageType;
        }

        return UNINITIALIZED;
    }
}
