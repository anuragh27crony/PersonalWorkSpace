package undertow1;

import io.undertow.Undertow;
import io.undertow.server.handlers.PathHandler;
import io.undertow.server.handlers.resource.ClassPathResourceManager;
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
 * Created by amala on 20-01-2017.
 */
public class WebSocketServer {
//    private static final Logger LOGGER = LogManager.getLogger(basic.WebSocketServer.class);
    private Undertow server;
    private String lastReceivedMessage;

    public static void main(final String[] args) {
        basic.WebSocketServer webSocketServer = new basic.WebSocketServer();
        webSocketServer.buildAndStartServer(8080, "localhost");
    }

    public void buildAndStartServer(int port, String host) {
        server = Undertow.builder()
                .addListener(port, host)
                .setHandler(getWebSocketHandler())
                .build();
        server.start();
    }

    public void stopServer() {
        if (server != null) {
            server.stop();
        }
    }

    private PathHandler getWebSocketHandler() {
        return path().addPath("/websocket", websocket(new WebSocketConnectionCallback() {
            @Override
            public void onConnect(WebSocketHttpExchange exchange, WebSocketChannel channel) {
                channel.getReceiveSetter().set(new AbstractReceiveListener() {
                    @Override
                    protected void onFullTextMessage(WebSocketChannel channel, BufferedTextMessage message) {
                        String data = message.getData();
                        lastReceivedMessage = data;
                        System.out.println("Recieved Data is "+lastReceivedMessage);
//                        LOGGER.info("Received data: " + data);
                        WebSockets.sendText(data, channel, null);
                    }
                });
                channel.resumeReceives();
            }
        }));
    }

    public String getLastReceivedMessage() {
        return lastReceivedMessage;
    }

    public void setLastReceivedMessage(String lastReceivedMessage) {
        this.lastReceivedMessage = lastReceivedMessage;
    }
}
