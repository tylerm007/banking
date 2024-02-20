#this is the api_test.feature
Feature: API GET Testing

  Scenario: GET Customer Endpoint
    Given GET Customer endpoint
    When GET Customer API
    Then Customer retrieved

  Scenario: GET Branch Endpoint
    Given GET Branch endpoint
    When GET Branch API
    Then Branch retrieved

  Scenario: GET AccountType Endpoint
    Given GET AccountType endpoint
    When GET AccountType API
    Then AccountType retrieved

  Scenario: GET Account Endpoint
    Given GET Account endpoint
    When GET Account API
    Then Account retrieved

  Scenario: GET Transfer Endpoint
    Given GET Transfer endpoint
    When GET Transfer API
    Then Transfer retrieved

  Scenario: GET Employee Endpoint
    Given GET Employee endpoint
    When GET Employee API
    Then Employee retrieved

  Scenario: GET Transaction Endpoint
    Given GET Transaction endpoint
    When GET Transaction API
    Then Transaction retrieved

