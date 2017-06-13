Feature: This feature verifies the status of Channel Worker.


  Scenario Outline: Verify State of channel worker
    Given Channel is <Channel>
    And   Channel <HTTPMethod>  <Activity>
    When Get status "v1/admin/status"
    Then Status code should be 200
    And  Channel state should be <State>

    Examples: states mapping
      | Channel | Activity       | HTTPMethod | State       |
      | worker1 | v1/admin/start | POST       | Operational |
      | worker2 | v1/admin/stop  | POST       | Idle        |