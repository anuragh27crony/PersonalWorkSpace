//import basic.WebSocketServer;
//import org.apache.log4j.LogManager;
//import org.apache.log4j.Logger;
//import org.junit.After;
//import org.junit.Before;
//import org.junit.Test;
//
//import static org.hamcrest.core.Is.is;
//import static org.junit.Assert.assertThat;
//
//public class WebSocketServerTest {
//    private static final Logger LOGGER = LogManager.getLogger(WebSocketServerTest.class);
//    private WebSocketServer subject;
//
//    @Before
//    public void before() {
//        subject = new WebSocketServer();
//    }
//
//    @Test
//    public void testStartAndBuild() throws Exception {
//        long startTime = System.currentTimeMillis();
//
//
//        subject.buildAndStartServer(9000, "localhost");
////        WebSocketClient client = new WebSocketClient();
////        WebSocketClient client = WebSocketClient.toSocketAddress(new URI("ws://localhost:8080/websocket"))
////        Future<WebSocket.Connection> connectionFuture = client.open(new URI("ws://localhost:8080/websocket"), new WebSocket() {
////            @Override
////            public void onOpen(Connection connection) {
////                LOGGER.info("onOpen");
////                try {
////                    connection.sendMessage("TestMessage");
////                } catch (IOException e) {
////                    LOGGER.error("Failed to send message: " + e.getMessage(), e);
////                }
////            }
////
////            @Override
////            public void onClose(int i, String s) {
////                LOGGER.info("onClose");
////            }
////        });
////        WebSocket.Connection connection = connectionFuture.get(2, TimeUnit.SECONDS);
////        assertThat(connection, is(notNullValue()));
////        connection.close();
//        long after_start = System.currentTimeMillis();
//        long timeOutinMillis = 10000;
//        long pollinMillis = 100;
//        while (subject.getLastReceivedMessage() == null && timeOutinMillis > 0) {
//            Thread.sleep(pollinMillis);
//            timeOutinMillis -= pollinMillis;
//        }
//
//        long stopTime = System.currentTimeMillis();
//        System.out.println(stopTime - startTime);
//        System.out.println(stopTime - after_start);
//        System.out.println("Total Wait time is -> " + (10000 - timeOutinMillis));
//
//        assertThat(subject.getLastReceivedMessage(), is("TestMessage"));
//    }
//
//    @After
//    public void after() {
//        subject.stopServer();
//        System.out.println("Successfully stoped the server");
//    }
//}