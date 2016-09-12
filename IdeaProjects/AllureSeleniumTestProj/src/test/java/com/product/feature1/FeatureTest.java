package com.product.feature1;

import Utils.DriverClass;
import org.testng.Assert;
import org.testng.annotations.BeforeClass;
import org.testng.annotations.Test;

/**
 * Created by AnuragM on 11/09/16.
 */
public class FeatureTest {

    public DriverClass driver;

    @BeforeClass
    public void Setup(){
        this.driver= new DriverClass();
    }

    @Test
    public void testSearchResults(){
        driver.openHomepage();
        driver.searchKeyword("Testing is fun");

        //This step fails since we are searching non exisiting element
        driver.validateResults();

    }

}
