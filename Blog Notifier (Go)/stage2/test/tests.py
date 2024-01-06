# TODO -- WE NEED TO ADD THE CORRECT TESTS FOR STAGE 2

import os

from hstest import StageTest, TestedProgram, CheckResult, dynamic_test


class TestBlogNotifierCLI(StageTest):

    @staticmethod
    def create_yaml_file(file_name, content):
        with open(file_name, 'w') as file:
            file.write(content)

    @staticmethod
    def remove_yaml_file(file_name):
        if os.path.exists(file_name):
            os.remove(file_name)

    @dynamic_test
    def test1_valid_credentials_yaml(self):
        # Create the first YAML file
        yaml_content_1 = ("mode: mail\n"
                          "server:\n"
                          "  host: smtp.gmail.com\n"
                          "  port: 465\n"
                          "client:\n"
                          "  email: sender@example.com\n"
                          "  password: 123456\n"
                          "  send_to: recipient@example.net\n"
                          "telegram:\n"
                          "  bot_token: abcdef123456\n"
                          "  channel: mychannel")
        self.create_yaml_file('credentials.yaml', yaml_content_1)

        program = TestedProgram()
        output = program.start('--config', 'credentials.yaml').strip()

        # Remove the created YAML file
        self.remove_yaml_file('credentials.yaml')

        expected_output = ("mode: mail\n"
                           "email_server: smtp.gmail.com:465\n"
                           "client: sender@example.com 123456 recipient@example.net\n"
                           "telegram: abcdef123456@mychannel")

        if output != expected_output:
            return CheckResult.wrong(
                f"The output of the program does not match the expected output for the first YAML file."
                f"\nYour program output: {output}"
                f"\nExpected output: {expected_output}")

        return CheckResult.correct()

    @dynamic_test
    def test2_valid_credentials_yaml(self):
        # Create the second YAML file
        yaml_content_2 = ("mode: telegram\n"
                          "server:\n"
                          "  host: 127.0.0.1\n"
                          "  port: 2500\n"
                          "client:\n"
                          "  email: sender@example.com\n"
                          "  password: secret\n"
                          "  send_to: recipient@example.net\n"
                          "telegram:\n"
                          "  bot_token: abcd1234\n"
                          "  channel: mychannel")
        self.create_yaml_file('credentials.yaml', yaml_content_2)

        program = TestedProgram()
        output = program.start('--config', 'credentials.yaml').strip()

        # Remove the created YAML file
        self.remove_yaml_file('credentials.yaml')

        expected_output = ("mode: telegram\n"
                           "email_server: 127.0.0.1:2500\n"
                           "client: sender@example.com secret recipient@example.net\n"
                           "telegram: abcd1234@mychannel")

        if output != expected_output:
            return CheckResult.wrong(
                f"The output of the program does not match the expected output for the second YAML file."
                f"\nYour program output: {output}"
                f"\nExpected output: {expected_output}")

        return CheckResult.correct()

    @dynamic_test
    def test3_invalid_yaml_file(self):
        program = TestedProgram()
        output = program.start('--config', 'nonexistent.yaml').lower().strip()
        expected_error = "file 'nonexistent.yaml' not found"
        if 'not found' not in output or not program.is_finished():
            return CheckResult.wrong(
                f"The program should print a message mentioning YAML file was not found. "
                f"\nYour program output: {output}"
                f"\nExpected output: {expected_error}")
        return CheckResult.correct()

    @dynamic_test
    def test4_no_command_input(self):
        program = TestedProgram()
        output = program.start().lower().strip()
        expected_error = "no command input specified"

        if ('no command' not in output and 'specified' not in output) and not program.is_finished():
            return CheckResult.wrong(
                f"The program should print a message mentioning no command input was specified. "
                f"\nYour program output: {output}"
                f"\nExpected output: {expected_error}")
        return CheckResult.correct()

    # Additional edge case tests can be added here ...


# Run the test cases
if __name__ == '__main__':
    TestBlogNotifierCLI().run_tests()
