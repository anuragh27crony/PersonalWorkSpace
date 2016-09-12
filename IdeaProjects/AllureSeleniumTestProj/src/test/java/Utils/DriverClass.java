package Utils;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.remote.DesiredCapabilities;
import org.openqa.selenium.support.events.AbstractWebDriverEventListener;
import org.openqa.selenium.support.events.EventFiringWebDriver;
import org.openqa.selenium.support.events.WebDriverEventListener;
import ru.yandex.qatools.allure.annotations.Attachment;
import ru.yandex.qatools.allure.annotations.Step;


/**
 * Created by AnuragM on 11/09/16.
 */
public class DriverClass {

    private WebDriver driverInstance;

    public DriverClass(){
        System.setProperty("webdriver.gecko.driver","/Applications/Firefox.app/Contents/MacOS/firefox");
        DesiredCapabilities capabilities=DesiredCapabilities.firefox();
        capabilities.setCapability("marionette",true);

        EventFiringWebDriver eventDriver = new EventFiringWebDriver(new FirefoxDriver(capabilities));
        WebDriverEventListener errorListener = new AbstractWebDriverEventListener() {
            @Override
            public void onException(Throwable throwable, WebDriver driver) {
                takeScreenshot();
            }
        };
        eventDriver.register(errorListener);
        driverInstance=eventDriver;

    }

    @Step("Navigate to Homepage")
    public void openHomepage(){
        driverInstance.get("http://WWW.Google.com");
    }

    @Step("Search  \\\"{0}\\\" in Homepage")
    public void searchKeyword(String searchText){
        WebElement searchElement=driverInstance.findElement(By.id("q"));
        searchElement.sendKeys(searchText);
        searchElement.sendKeys(Keys.ENTER);
    }

    @Step("Verify the search Results")
    public void validateResults(){
        driverInstance.findElement(By.id("NONEXISTING ELEMENT"));
    }


//    This Annotation does all the work from saving screenshot
//    till attaching it to report
    @Attachment
    public byte[] takeScreenshot(){
        return ((TakesScreenshot)driverInstance).getScreenshotAs(OutputType.BYTES);
    }
}
