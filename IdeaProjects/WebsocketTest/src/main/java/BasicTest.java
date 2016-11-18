import io.undertow.Undertow;
import io.undertow.server.handlers.PathHandler;
import io.undertow.websockets.WebSocketConnectionCallback;
import io.undertow.websockets.core.AbstractReceiveListener;
import io.undertow.websockets.core.BufferedTextMessage;
import io.undertow.websockets.core.WebSocketChannel;
import io.undertow.websockets.core.WebSockets;
import io.undertow.websockets.spi.WebSocketHttpExchange;
import org.apache.log4j.LogManager;
import org.apache.log4j.Logger;


import static io.undertow.Handlers.path;
import static io.undertow.Handlers.websocket;

/**
 * Created by amala on 17/11/2016.
 */
public class BasicTest {
    private static final Logger LOGGER = LogManager.getLogger(BasicTest.class);

    public void buildAndStartServer(int port, String host) {
        Undertow server = Undertow.builder()
                .addListener(port, host)
                .setHandler(getWebSocketHandler())
                .build();
        server.start();
    }

    private PathHandler getWebSocketHandler() {
        return path().addPath("/websocket", websocket(new WebSocketConnectionCallback() {
            @Override
            public void onConnect(WebSocketHttpExchange exchange, WebSocketChannel channel) {
                channel.getReceiveSetter().set(new AbstractReceiveListener() {
                    @Override
                    protected void onFullTextMessage(WebSocketChannel channel, BufferedTextMessage message) {
                        String data = message.getData();
                        String lastReceivedMessage = data;
                        LOGGER.info("Received data: " + data);
                        WebSockets.sendText(data, channel, null);
                    }
                });
                channel.resumeReceives();
            }
        }));
    }


}
