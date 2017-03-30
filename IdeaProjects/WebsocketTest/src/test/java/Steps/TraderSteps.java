package Steps;

import basic.WebSocketServer;
import org.jbehave.core.annotations.Given;
import org.jbehave.core.annotations.Then;
import org.jbehave.core.annotations.When;

import static org.hamcrest.CoreMatchers.nullValue;
import static org.hamcrest.MatcherAssert.assertThat;

/**
 * Created by amala on 21/11/2016.
 */

public class TraderSteps {

    private WebSocketServer subject;

    @Given("a stock of symbol $symbol and a threshold of $threshold")
    public void aStock(String symbol, double threshold) {
//        stock = new Stock(symbol, threshold);
    }

    @When("the stock is traded at $price")
    public void theStockIsTradedAt(double price) {
//        stock.tradeAt(price);
    }

    @Then("the alert status should be $status")
    public void theAlertStatusShouldBe(String status) {
        subject = new WebSocketServer();

        subject.buildAndStartServer(9000, "localhost");
        long timeOutinMillis = 5000;
        long pollinMillis = 100;

        while (subject.getLastReceivedMessage() == null && timeOutinMillis > 0) {
            try {
                Thread.sleep(pollinMillis);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            timeOutinMillis -= pollinMillis;
        }
        subject.stopServer();


        assertThat(subject.getLastReceivedMessage(),nullValue());

    }
}