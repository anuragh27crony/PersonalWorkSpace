package another;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import org.joda.time.DateTime;
import org.joda.time.DateTimeZone;
import org.joda.time.LocalDateTime;
import org.joda.time.format.ISODateTimeFormat;

/**
 * Created by amala on 25/11/2016.
 */
public class MainClass {

    public static void main1(String[] args) {
        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.registerTypeAdapter(MyBaseTypeModel.class, new MyTypeModelDeserializer());
        Gson gson = gsonBuilder.create();
        String myJsonString = "{\n" +
                "    \"inc\": {\n" +
                "        \"innername\": \"SOME_STRING\"\n" +
                "    },\n" +
                "    \"message\": {\n" +
                "        \"id\": \"dcbaedf5-3e13-4807-b8ed-5c6848f88f6d\",\n" +
                "        \"type\": \"videoUploadReply\"\n" +
                "    },\n" +
                "    \"name\": \"BLAH BLAH\"\n" +
                "}";

        MyBaseTypeModel myTypeModel = gson.fromJson(myJsonString, MyBaseTypeModel.class);

        System.out.println(Type1Model.class.isInstance(myTypeModel));
        System.out.println(myTypeModel);

    }

    public static void main(String[] args) {

//        String validDateTimeFormatString = "yyyy-MM-dd HH:mm:ss.SSS";
//        DateTimeFormatter dtf = DateTimeFormat.forPattern(validDateTimeFormatString);
//
//
        String startdt = "2016-10-09T10:40:27.500Z";
        DateTime startDateTime = ISODateTimeFormat.dateTime().parseDateTime(startdt);
//        long mills = startDateTime.toDateTime().getMillis();

        System.out.println(startDateTime.withZone(DateTimeZone.UTC));

//        String enddt = "2016-10-09T10:42:27.500Z";
//        LocalDateTime endDateTime = dtf.parseLocalDateTime(startdt);
//        System.out.println(endDateTime.toDateTime().withZone(DateTimeZone.UTC));

//        System.out.println(LocalDateTime.now().toDateTime().toString(ISODateTimeFormat.dateTime()));
//        System.out.println(ISODateTimeFormat.dateTime().parseDateTime("2016-10-09T10:40:27.500Z"));

        System.out.println(ISODateTimeFormat.dateTime().print(DateTime.now().withZone(DateTimeZone.UTC)));
        System.out.println(ISODateTimeFormat.dateTime().print(LocalDateTime.now().toDateTime().withZone(DateTimeZone.UTC)));


    }
}
