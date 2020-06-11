@multiprovisioning-1
Feature: Multiprovisioning

# TODO: Remove hardcoded waits when sizes, images and locations
# are returned immediately after adding cloud

  Background:
    Given I am logged in to mist
    When I visit the Home page
    And I wait for the navigation menu to appear

  @add-key
  Scenario: Add key needed for tests
    Given key "Keyrandom" has been generated and added via API request

  # FIXME: When reenabling below, switch packet's specs in scenario outline below as:
  # | Packet        | x1.small.x86 - 32GB RAM                                 | Marseille, France| Ubuntu 19.04                                   | packet-mp-test-random  |


  # @packet-set-private-ipv4
  # Scenario: Create a machine in Packet provider setting private ipv4
  #   Given "Packet" cloud has been added
  #   And I wait for 40 seconds
  #   When I visit the Machines page
  #   And I click the button "+"
  #   Then I expect the "Machine" add form to be visible within max 10 seconds
  #   When I open the "Select Cloud" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Packet" button in the "Select Cloud" dropdown in the "machine" add form
  #   Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
  #   Then I set the value "packet-mp-test0-random" to field "Machine Name" in the "machine" add form
  #   When I open the "Image" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Ubuntu 19.04" button in the "Image" dropdown in the "machine" add form
  #   When I open the "Size" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "t1.small.x86 - 8GB RAM" button in the "Size" dropdown in the "machine" add form
  #   And I open the "Key" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Keyrandom" button in the "Key" dropdown in the "machine" add form
  #   And I open the "Private IPv4 Subnet Size" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "/30" button in the "Private IPv4 Subnet Size" dropdown in the "machine" add form
  #   When I open the "Location" dropdown in the "machine" add form
  #   And I wait for 1 seconds
  #   And I click the "Amsterdam, NL" button in the "Location" dropdown in the "machine" add form
  #   Then I expect for the button "Launch" in the "machine" add form to be clickable within 10 seconds
  #   When I focus on the button "Launch" in the "machine" add form
  #   And I click the button "Launch" in the "machine" add form
  #   When I visit the Home page
  #   And I visit the Machines page
  #   And I wait for 1 seconds
  #   And I clear the search bar
  #   And I search for "packet-mp-test0-random"
  #   Then "packet-mp-test0-random" machine should be present within 60 seconds

  @mp-test-with-cloud-init
  Scenario Outline: Create a machine in various providers, creating a file using cloud init
    Given "<cloud>" cloud has been added
    And I wait for 40 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<cloud>" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "<machine-name>" to field "Machine Name" in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<location>" button in the "Location" dropdown in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<image>" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<size>" button in the "Size" dropdown in the "machine" add form
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
    And I search for "<machine-name>"
    Then "<machine-name>" machine should be present within 60 seconds

    Examples: Providers to be tested
    | cloud         | size                                                    | location         | image                                          | machine-name           |
    | Packet        | t1.small.x86 - 8192 RAM                                 | Amsterdam, NL    | Ubuntu 19.10                                   | packet-mp-test-random  |
    | Google Cloud  | f1-micro (1 vCPU (shared physical core) and 0.6 GB RAM) | europe-west1-c   | ubuntu-1804-bionic-v20200317                   | gce-mp-test-random     |

  @mp-test-with-cloud-init
  Scenario Outline: Create a machine in various providers, creating a file using cloud init
    Given "<cloud>" cloud has been added
    And I wait for 40 seconds
    When I visit the Machines page
    And I click the button "+"
    Then I expect the "Machine" add form to be visible within max 10 seconds
    When I open the "Select Cloud" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<cloud>" button in the "Select Cloud" dropdown in the "machine" add form
    Then I expect the field "Machine name" in the machine add form to be visible within max 4 seconds
    Then I set the value "<machine-name>" to field "Machine Name" in the "machine" add form
    When I open the "Location" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<location>" button in the "Location" dropdown in the "machine" add form
    When I open the "Image" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<image>" button in the "Image" dropdown in the "machine" add form
    When I open the "Size" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "<size>" button in the "Size" dropdown in the "machine" add form
    When I open the "Security group" dropdown in the "machine" add form
    And I wait for 1 seconds
    And I click the "mistio" button in the "Security group" dropdown in the "machine" add form
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
    And I search for "<machine-name>"
    Then "<machine-name>" machine should be present within 60 seconds

    Examples: Providers to be tested
    | cloud         | size                                                    | location         | image                                          | machine-name           |
    | AWS Advantis  | t2.nano - t2.nano                                       | us-west-2a       | Ubuntu Server 16.04 LTS (HVM), SSD Volume Type | ec2-mp-test-random     |

    @verify-cloud-init
    Scenario Outline: Verify that file created with cloud-init exists
      When I visit the Machines page
      And I wait for 1 seconds
      And I clear the search bar
      And I search for "<machine>"
      Then "<machine>" machine state has to be "running" within 60 seconds
      And I click the "<machine>" "machine"
      And I expect the "machine" page to be visible within max 5 seconds
      And I wait for 2 seconds
      Then I click the "Shell" action button in the "machine" page
      And I expect terminal to open within 3 seconds
      And shell input should be available after 30 seconds
      And I type in the terminal "sudo su"
      And I wait for 1 seconds
      And I type in the terminal "ls -la ~"
      And I wait for 1 seconds
      Then new_file should be included in the output
      And I close the terminal

    Examples: Providers to be tested
    | machine                |
    | ec2-mp-test-random     |
    | gce-mp-test-random     |

  @packet-verify-cloud-init
  Scenario: Verify that file created with cloud-init exists
    When I visit the Machines page
    And I wait for 1 seconds
    And I clear the search bar
    And I search for "packet-mp-test-random"
    Then "packet-mp-test-random" machine state has to be "running" within 2700 seconds
    # wait for probe
    And I wait for 300 seconds
    And I click the "packet-mp-test-random" "machine"
    And I expect the "machine" page to be visible within max 5 seconds
    And I wait for 2 seconds
    Then I click the "Shell" action button in the "machine" page
    And I expect terminal to open within 3 seconds
    And shell input should be available after 30 seconds
    And I type in the terminal "sudo su"
    And I wait for 1 seconds
    And I type in the terminal "ls -la ~"
    And I wait for 1 seconds
    Then new_file should be included in the output
    And I close the terminal
