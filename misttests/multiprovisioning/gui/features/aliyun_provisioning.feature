@aliyun-provisioning
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear
    Given key "Keyrandom" has been generated and added via API request

  @aliyun-machine-create-cloud-init
  Scenario: Create a machine in aliyun provider, creating a file using cloud init
    Given "Alibaba Cloud" cloud has been added
    And I wait for 120 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Alibaba Cloud" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "aliyun-mp-test-random" to field "Machine Name" in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "us-west-1a" button in the "Location" dropdown in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "ubuntu_18_04_x64_20G_alibase_20200618.vhd" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "ecs.e4.small (1 cpus/ 8.0Gb RAM )" button in the "Size" dropdown in the "machine" add form
    And I open the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
    And I wait for 1 seconds
    Then I set the "cloud init" script "#!/bin/bash\ntouch ~/new_file"
    Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
    When I focus on the button "Launch" in the "machine" add form
    And I click the button "Launch" in the "machine" add form
    When I visit the Home page
    And I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "aliyun-mp-test-random"
    Then "aliyun-mp-test-random" machine should be present within 60 seconds
    And "aliyun-mp-test-random" machine state has to be "running" within 120 seconds
    When I click the "aliyun-mp-test-random" "machine"
    Then I expect the "machine" page to be visible within max 5 seconds
    When I wait for 90 seconds
    And I click the "Shell" action button in the "machine" page
    Then I expect terminal to open within 3 seconds
    And shell input should be available after 30 seconds
    When I type in the terminal "sudo su"
    And I wait for 2 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output
