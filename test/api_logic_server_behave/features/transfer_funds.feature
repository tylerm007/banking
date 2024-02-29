Feature: Transfer Funds

  Scenario: Transfer From Savings to Checking
    Given Transfer Transaction
      When Transfer submitted
      Then Rules Fire and Transaction Success