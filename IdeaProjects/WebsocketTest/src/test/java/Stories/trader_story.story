Meta:

Narrative:
As a user
I want to perform an action
So that I can achieve a business goal


Scenario:  trader is not alerted below threshold

Given a stock of symbol STK1 and a threshold of 10.0
When the stock is traded at 5.0
Then the alert status should be OFF

Scenario:  trader is alerted above threshold

Given a stock of symbol STK1 and a threshold of 10.0
When the stock is traded at 11.0
Then the alert status should be ON