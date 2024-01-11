import os

from hstest import StageTest, TestedProgram, CheckResult, dynamic_test, WrongAnswer

DB_FILE = 'blogs.sqlite3'
class TestBlogNotifierCLI(StageTest):

    @staticmethod
    def remove_db_file():
        print(os.curdir)
        if os.path.exists(DB_FILE):
            os.remove(DB_FILE)

    @dynamic_test
    def test1_migrate_command(self):
        # Test the --migrate sub-command which creates the blogs.sqlite3 database and tables
        program = TestedProgram()
        output = program.start("--migrate").strip().lower()

        if "database 'blogs.sqlite3' created successfully" not in output:
            raise WrongAnswer("The --migrate command did not report successful creation of the database.")

        if "tables 'blogs', 'posts', and 'mails' initialized" not in output:
            raise WrongAnswer("The --migrate command did not report successful initialization of the tables.")

        self.remove_db_file()

        return CheckResult.correct()

    @dynamic_test
    def test2_explore_command(self):
        # Test the --explore sub-command which adds a new blog to the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        output = program.start('--explore', 'https://hyperskill.org/blog/').strip()

        if "New blog added to watchlist" not in output:
            raise WrongAnswer("The --explore command did not report adding a new blog to the watch list.")

        if "site: https://hyperskill.org/blog/" not in output or "last link: https://hyperskill.org/blog/" not in output:
            raise WrongAnswer("The --explore command did not output the correct blog information.")

        return CheckResult.correct()

    @dynamic_test
    def test3_edge_cases(self):
        # Test the --explore sub-command which adds a blog to the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore', 'https://blog1.com')
        program = TestedProgram()
        output = program.start('--explore', 'https://blog1.com').strip()

        if "https://blog1.com already exists in the watch list" not in output:
            raise WrongAnswer("The --explore command did not report the correct message on adding a blog that is already in the watch list.")

        self.remove_db_file()

        return CheckResult.correct()

    @dynamic_test
    def test4_list_command(self):
        # Test the --list sub-command which lists all blog sites in the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore','https://blog1.com')
        program = TestedProgram()
        program.start('--explore','https://blog2.com')
        program = TestedProgram()
        output = program.start("--list").strip()

        if "https://blog1.com https://blog1.com" not in output or "https://blog2.com https://blog2.com" not in output:
            raise WrongAnswer("The --list command did not list all the blog sites in the watch list correctly.")

        self.remove_db_file()

        return CheckResult.correct()

    @dynamic_test
    def test5_update_last_link_command(self):
        # Test the --update-last-link sub-command which updates the last link of a blog site
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore', 'https://blog1.com')
        program = TestedProgram()
        output = program.start('update-last-link', '--site', 'https://blog1.com', '--post', 'https://blog1.com/post200').strip()

        if "The last link for https://blog1.com updated to https://blog1.com/post200" not in output:
            raise WrongAnswer("The --update-last-link command did not report the correct update message.")

        program = TestedProgram()
        output = program.start("--list").strip().lower()

        if "https://blog1.com https://blog1.com/post200" not in output:
            raise WrongAnswer("The --list command shows wrong output, seams that 'update-last-link' sub-command was not implemented correctly")

        self.remove_db_file()

        return CheckResult.correct()

    @dynamic_test
    def test6_remove_command(self):
        # Test the --remove sub-command which removes a blog from the watch list
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        program.start('--explore', 'https://blog1.com')
        program = TestedProgram()
        output = program.start('--remove', 'https://blog1.com').strip()

        if "https://blog1.com removed from the watch list." not in output:
            raise WrongAnswer("The --remove command did not report the correct removal message.")

        program = TestedProgram()
        output = program.start("--list").strip()

        if "https://blog1.com https://blog1.com" in output:
            raise WrongAnswer("The --list command shows wrong output, seams that '--remove' flag was not implemented correctly")

        self.remove_db_file()

        return CheckResult.correct()

    @dynamic_test
    def test7_edge_cases(self):
        # Test edge cases like removing a non-existent blog site
        program = TestedProgram()
        program.start("--migrate")
        program = TestedProgram()
        output = program.start('--remove', 'https://nonexistentblog.com').strip()

        if "https://nonexistentblog.com does not exist in the watch list" not in output:
            raise WrongAnswer("The --remove command did not handle non-existent blog sites correctly.")

        return CheckResult.correct()

if __name__ == '__main__':
    TestBlogNotifierCLI().run_tests()
