package Steps;

import org.jbehave.core.annotations.Given;
import org.jbehave.core.annotations.Then;
import org.jbehave.core.annotations.When;

import static org.junit.Assert.assertFalse;

/**
 * Created by amala on 22/11/2016.
 */
public class RadioSteps {

    private Radio radio;

    @Given("a digital radio")
    public void aDigitalRadio(){
        radio = new Radio();
    }

    @When("I turn on the radio")
    public void iTurnOnTheRadio(){
        radio.switchOnOff();
    }

    @Then("the radio should be turned on")
    public void theRadioShouldBeTurnedOn(){
        assertFalse(radio.isTurnedOn());
    }
}
