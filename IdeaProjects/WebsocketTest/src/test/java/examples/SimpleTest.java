//import io.undertow.websockets.client.WebSocketClient;
//import org.apache.log4j.LogManager;
//import org.apache.log4j.Logger;
//import org.eclipse.jetty.websocket.WebSocket;
//import org.junit.Test;
//
//import java.io.IOException;
//import java.net.URI;
//import java.util.concurrent.Future;
//import java.util.concurrent.TimeUnit;
//
//import static org.junit.Assert.assertThat;
//
///**
// * Created by amala on 17/11/2016.
// */
//public class SimpleTest {
//    private static final Logger LOGGER = LogManager.getLogger(SimpleTest.class);
//
//    @Test
//    public void testStartAndBuild() throws Exception {
//        subject = new WebSocketServer();
//        subject.buildAndStartServer(8080, "127.0.0.1");
//        WebSocketClient client = new WebSocketClient();
//        Future connectionFuture = client.open(new URI("ws://localhost:8080/websocket"), new WebSocket() {
//            @Override
//            public void onOpen(Connection connection) {
//                LOGGER.info("onOpen");
//                try {
//                    connection.sendMessage("TestMessage");
//                } catch (IOException e) {
//                    LOGGER.error("Failed to send message: " + e.getMessage(), e);
//                }
//            }
//
//            @Override
//            public void onClose(int i, String s) {
//                LOGGER.info("onClose");
//            }
//        });
//        WebSocket.Connection connection = connectionFuture.get(2, TimeUnit.SECONDS);
//        assertThat(connection, is(notNullValue()));
//        connection.close();
//        subject.stopServer();
//        Thread.sleep(1000);
//        assertThat(subject.lastReceivedMessage, is("TestMessage"));
//    }
//
//}
