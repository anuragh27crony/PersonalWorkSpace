package another;

import com.google.gson.*;

import java.lang.reflect.Type;

/**
 * Created by amala on 25/11/2016.
 */
public class MyTypeModelDeserializer implements JsonDeserializer<MyBaseTypeModel> {

    @Override
    public MyBaseTypeModel deserialize(final JsonElement json, final Type typeOfT, final JsonDeserializationContext context)
            throws JsonParseException {
        JsonObject jsonObject = json.getAsJsonObject();

        JsonElement jsonType = jsonObject.get("message").getAsJsonObject().get("type");
        String type = jsonType.getAsString();

        MyBaseTypeModel typeModel = null;

        if("videoUploadReply".equals(type)) {
            typeModel = new Type1Model();
        } else if("videoUploadRequest".equals(type)) {
            typeModel = new Type2Model();
        }
        // TODO : set properties of type model

        return typeModel;
    }
}