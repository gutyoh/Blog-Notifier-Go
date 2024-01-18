import multiprocessing
from .blognotifier_test_utils import *

from hstest import StageTest, TestedProgram, CheckResult, dynamic_test


class TestBlogNotifierCLI(StageTest):

    @dynamic_test
    def test1_migrate_command(self):
        # Test the --migrate sub-command which creates the blogs.sqlite3 database and tables
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate").strip().lower()

        for table_name in tables_properties:
            if check_table_exists(table_name) is False:
                raise CheckResult.wrong(f"The --migrate command did not create the '{table_name}' table.")
            temp = check_table_properties(table_name)
            if temp[0] is False:
                raise CheckResult.wrong(
                    f"Wrong column types for '{table_name}' table. Expected column types for the '{table_name}' table are {tables_properties[table_name]}. Found {temp[1]}")

        return CheckResult.correct()

    @dynamic_test
    def test2_explore_command(self):
        # Test the --list sub-command which lists all blog sites in the watch list
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog_1 = blog_files[FLAT_MULTIPLE_LINKS_TEST][0]
        program.start('--explore', blog_1)
        program = TestedProgram()
        blog_2 = blog_files[FLAT_MULTIPLE_LINKS_TEST][1]
        program.start('--explore', blog_2)
        program = TestedProgram()
        blog_3 = blog_files[FLAT_MULTIPLE_LINKS_TEST][2]
        program.start('--explore', blog_3)
        program = TestedProgram()
        output = program.start("--list").strip()

        if f"{blog_1} {blog_1}" not in output or f"{blog_2} {blog_2}" not in output or f'{blog_3} {blog_3}' not in output:
            raise CheckResult.wrong("The --list command did not list all the blog sites in the watch list correctly. "
                                    "May be explore functionality is not implemented correctly")

        return CheckResult.correct()

    @dynamic_test
    def test3_remove_command(self):
        # Test the --remove sub-command which removes a blog from the watch list
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog_1 = blog_files[FLAT_MULTIPLE_LINKS_TEST][0]
        program.start('--explore', blog_1)
        program = TestedProgram()
        blog_2 = blog_files[FLAT_MULTIPLE_LINKS_TEST][1]
        program.start('--explore', blog_2)
        program = TestedProgram()
        program.start('--remove', blog_1).strip()

        program = TestedProgram()
        output = program.start("--list").strip()

        if f"{blog_1} {blog_1}" in output:
            raise CheckResult.wrong(
                "The --list command shows wrong output, seams like '--remove' flag was not implemented correctly")

        if f"{blog_2} {blog_2}" not in output:
            raise CheckResult.wrong(
                "The --list command shows wrong output, seams like '--remove' flag was not implemented correctly")

        return CheckResult.correct()

    @dynamic_test
    def test4_crawling_with_no_hyperlinks(self):
        # Test the crawl flag and list-posts sub-command.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore', blog_files[NO_LINKS_TEST])
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog_files[NO_LINKS_TEST])

        output.strip()

        # Expected links from the example output
        expected_output = ""

        # Check if all expected links are present in the output
        if expected_output != output:
            return CheckResult.wrong(
                f"The output of the program does not match the expected output for the list-posts sub-command."
                f"\nYour program output: {output}"
                f"\nExpected output: {expected_output}")

        return CheckResult.correct()

    @dynamic_test
    def test5_crawling_with_nested_links_a(self):
        # Test the crawl flag and list-posts sub-command for blog with one blog-posts.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[NESTED_LINKS_TEST_1][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog)

        output.strip()

        # Expected links from the example output
        expected_output = blog_files[NESTED_LINKS_TEST_1][0]

        # Check if all expected links are present in the output
        if expected_output not in output:
            return CheckResult.wrong(
                f"Test was carried out for blog site with just one blog post expected_output: {expected_output} program_output: {output}")

        return CheckResult.correct()

    @dynamic_test
    def test6_crawling_with_nested_links_b(self):
        # Test the crawl flag and list-posts sub-command for blog with 2 nested blog-posts.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[NESTED_LINKS_TEST_2][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog)

        output.strip()

        # Expected links from the example output
        expected_output = blog_files[NESTED_LINKS_TEST_2][:-1]

        # Check if all expected links are present in the output
        for link in expected_output:
            if link not in output:
                return CheckResult.wrong(f"Test was carried out for blog site with two blog posts {link} not found in "
                                         f"the program output")

        return CheckResult.correct()

    @dynamic_test
    def test7_crawling_with_flat_multiple_pages(self):
        # Test the crawl flag and list-posts sub-command for blog with many blog-posts.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[FLAT_MULTIPLE_LINKS_TEST][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog)

        output.strip()

        # Expected links from the example output
        expected_output = blog_files[FLAT_MULTIPLE_LINKS_TEST][:-1]

        # Check if all expected links are present in the output
        for link in expected_output:
            if link not in output:
                return CheckResult.wrong(
                    f"Test was carried out for blog site with multiple blog posts {link} not found in "
                    f"the program output")

        return CheckResult.correct()

    @dynamic_test
    def test8_crawling_with_nested_and_flat_posts(self):
        # Test the crawl flag and list-posts sub-command for blog with many blog-posts (flat and nested).
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[NESTED_AND_FLAT_LINKS_TEST][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("list-posts", "--site", blog)

        # Expected links from the example output
        expected_links = blog_files[NESTED_AND_FLAT_LINKS_TEST][:-1]

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in output:
                return CheckResult.wrong(
                    f"Test was carried out for blog site with multiple blog posts flat and nested. {link} not found in "
                    f"the program output")

        return CheckResult.correct()

    @dynamic_test
    def test9_crawling_and_update_last_link(self):
        # Test the crawl flag and checking if the last_link column of the blogs table is updated.
        remove_db_file()
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        blog = blog_files[FLAT_MULTIPLE_LINKS_TEST][-1]
        program.start('--explore', blog)
        program = TestedProgram()
        program.start("--crawl")

        program = TestedProgram()
        output = program.start("--list")

        output.strip()

        # Check if all expected links are present in the output
        for link in blog_files[FLAT_MULTIPLE_LINKS_TEST][:-1]:
            if f'{blog} {link}' in output:
                return CheckResult.correct()

        return CheckResult.wrong(
            f"Test was carried out for blog site with multiple blog posts seems like the last_link column in the blogs "
            f"table is not updated after crawling")

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
        create_yaml_file('credentials.yaml', yaml_content_1)

        program = TestedProgram()
        output = program.start('--config', 'credentials.yaml').strip()

        # Remove the created YAML file
        remove_yaml_file('credentials.yaml')

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
        create_yaml_file('credentials.yaml', yaml_content_2)

        program = TestedProgram()
        output = program.start('--config', 'credentials.yaml').strip()

        # Remove the created YAML file
        remove_yaml_file('credentials.yaml')

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


# Run the test cases
if __name__ == '__main__':
    http_server_process: multiprocessing.Process = None
    smtp_server_process: multiprocessing.Process = None
    mail_queue: Queue = Queue()  # aiosmtpd server will put mails it receives from the program in this queue
    stop_server_signal_queue: Queue = Queue()  # is used to send signal when to stop aiosmtpd server
    try:
        # creating fake blog(just html files) for testing
        create_blog_site_with_no_posts()
        create_blog_site_with_nested_posts(1, NESTED_LINKS_TEST_1)
        create_blog_site_with_nested_posts(2, NESTED_LINKS_TEST_2)
        create_flat_blog_site_with_multiple_posts()
        create_blog_site_with_nested_and_flat_posts()

        # starting python's http.server
        http_server_process = multiprocessing.Process(target=run_http_server, args=(8000,))
        http_server_process.start()

        # starting aiosmtpd.server
        smtp_server_process = multiprocessing.Process(target=start_smtp_server,
                                                      args=(mail_queue, stop_server_signal_queue))
        smtp_server_process.start()
        # getting aiosmtpd server's address
        controller_info['hostname'] = mail_queue.get()
        controller_info['port'] = mail_queue.get()

        # running tests
        TestBlogNotifierCLI().run_tests()
    finally:
        # stopping python's http.server
        http_server_process.kill()

        # removing all the html files created
        remove_fake_blog()

        # stopping SMTP server
        stop_server_signal_queue.put(None)
        mail_queue.close()
        stop_server_signal_queue.close()
        smtp_server_process.kill()
