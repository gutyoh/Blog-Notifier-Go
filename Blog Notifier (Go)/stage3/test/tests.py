import multiprocessing
from .blog_notifier_test_utils import *

from hstest import StageTest, TestedProgram, CheckResult, dynamic_test


class TestBlogNotifierCLI(StageTest):

    @dynamic_test
    def test1_crawling_with_flat_multiple_pages(self):
        # Test crawling a site with multiple pages.
        program = TestedProgram()
        output = program.start("--crawl-site", blog_files[FLAT_MULTIPLE_LINKS_TEST][-1])

        # Splitting the output into lines for easier assertion
        links = output.strip().split('\n')

        # Expected links from the example output
        expected_links = blog_files[FLAT_MULTIPLE_LINKS_TEST][:-1]

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in links:
                return CheckResult.wrong("Not all the links in the blog-site are discovered")

        # # Check if there are no extra links in the output
        for link in links:
            if link.endswith(".html"):
                if link not in expected_links:
                    return CheckResult.wrong(f"There is an extra link {link} in the output.")

        return CheckResult.correct()

    @dynamic_test
    def test2_crawling_with_no_hyperlinks(self):
        # Test crawling a site with no links.
        program = TestedProgram()
        output = program.start("--crawl-site", blog_files[NO_LINKS_TEST])

        # Splitting the output into lines for easier assertion
        output = output.strip()

        # Expected links from the example output
        expected_output = f"No blog posts found for {blog_files[NO_LINKS_TEST]}"

        # Check if all expected links are present in the output
        if expected_output not in output:
            return CheckResult.wrong(
                f"The output of the program does not match the expected output."
                f"\nYour program output: {output}"
                f"\nExpected output: {expected_output}")

        return CheckResult.correct()

    @dynamic_test
    def test3_crawling_with_duplicate_links_a(self):
        # Test crawling a site with multiple pages, this is check for duplicate links.
        program = TestedProgram()
        output = program.start("--crawl-site", "https://brianpzaide.github.io/blog-notifier")

        # Splitting the output into lines for easier assertion
        links = output.strip().split('\n')

        # Expected links from the example output
        expected_links = [
            "https://brianpzaide.github.io/blog-notifier/a.html",
            "https://brianpzaide.github.io/blog-notifier/b.html",
            "https://brianpzaide.github.io/blog-notifier/c.html",
            "https://brianpzaide.github.io/blog-notifier/d.html",
            "https://brianpzaide.github.io/blog-notifier/e.html",
            "https://brianpzaide.github.io/blog-notifier/f.html"
        ]

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in links:
                return CheckResult.wrong(f"The link {link} was not found in the output.")

        links = [link for link in links if link.endswith(".html")]

        if len(links) > len(expected_links):
            return CheckResult.wrong("The output contains more links than expected, could be duplicate, please return "
                                     "unique links.")

        # Check if there are no extra links in the output
        for link in links:
            if link not in expected_links:
                return CheckResult.wrong("The output contains extra links, could be duplicate, please return unique "
                                         "links.")

        return CheckResult.correct()

    @dynamic_test
    def test4_crawling_with_depth_limit_a(self):
        # checking code with blogs having depth of 2.
        program = TestedProgram()
        output = program.start("--crawl-site", blog_files[NESTED_LINKS_TEST][-4]).strip()

        # Mocked output for depth 3 limit, assuming known structure
        expected_links = blog_files[NESTED_LINKS_TEST][-5::-1]

        # Splitting the output into lines for easier assertion
        links = output.strip().split('\n')

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in links:
                return CheckResult.wrong("Program did not discover all the expected links.")

        links = [link for link in links if link.endswith(".html")]
        if len(links) > len(expected_links):
            return CheckResult.wrong(f"The output contains more links than expected, seams like the program crawls "
                                     f"beyond the depth limit of '3'")

        return CheckResult.correct()

    @dynamic_test
    def test5_crawling_with_depth_limit_b(self):
        # checking code with blogs having depth of 3.
        program = TestedProgram()
        output = program.start("--crawl-site", blog_files[NESTED_LINKS_TEST][-3]).strip()

        # Mocked output for depth 3 limit, assuming known structure
        expected_links = blog_files[NESTED_LINKS_TEST][-4::-1]

        # Splitting the output into lines for easier assertion
        links = output.strip().split('\n')

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in links:
                return CheckResult.wrong("Program did not discover all the expected links.")

        links = [link for link in links if link.endswith(".html")]
        if len(links) > len(expected_links):
            return CheckResult.wrong(f"The output contains more links than expected, seams like the program crawls "
                                     f"beyond the depth limit of '3'")

        return CheckResult.correct()

    @dynamic_test
    def test6_crawling_with_depth_limit_c(self):
        # checking code with blogs having depth of more than 3.
        program = TestedProgram()
        output = program.start("--crawl-site", blog_files[NESTED_LINKS_TEST][-1]).strip()

        # Mocked output for depth 3 limit, assuming known structure
        expected_links = blog_files[NESTED_LINKS_TEST][-2:-5:-1]

        # Splitting the output into lines for easier assertion
        links = output.strip().split('\n')

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in links:
                return CheckResult.wrong("Program did not discover all the expected links.")

        links = [link for link in links if link.endswith(".html")]
        if len(links) > len(expected_links):
            return CheckResult.wrong(f"The output contains more links than expected, seams like the program crawls "
                                     f"beyond the depth limit of '3'")

        return CheckResult.correct()

    @dynamic_test
    def test7_crawling_with_duplicate_links_b(self):
        # Test checks for cross-referencing posts (posts that have references of each other). Checks whether the code
        # breaks out of infinite recursion by obeying a depth limit of '3'.
        program = TestedProgram()
        output = program.start("--crawl-site", blog_files[CYCLIC_LINKS_TEST][-1])

        # Splitting the output into lines for easier assertion
        links = output.strip().split('\n')

        # Expected links from the example output
        expected_links = blog_files[CYCLIC_LINKS_TEST]

        links = [link for link in links if link.endswith(".html")]

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in links:
                return CheckResult.wrong("Program did not discover all the expected links.")


        if len(links) > len(expected_links):
            return CheckResult.wrong(f"The output contains duplicate links.")

        # Check if there are no extra links in the output
        for link in links:
            if link not in expected_links:
                return CheckResult.wrong(f"There is an extra link {link} in the output.")

        return CheckResult.correct()

    @dynamic_test
    def test8_crawling_with_nested_and_flat_posts(self):
        # Test checks for blogs that have flat blog-posts(blog-post that has no hyperlinks) or nested blog-posts(
        # blog-post that have hyperlinks to other blog-posts) .
        program = TestedProgram()
        output = program.start("--crawl-site", blog_files[NESTED_AND_FLAT_LINKS_TEST][-1])

        # Splitting the output into lines for easier assertion

        links = output.strip()

        # Expected links from the example output
        expected_links = blog_files[NESTED_AND_FLAT_LINKS_TEST][-2::-1]

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in links:
                return CheckResult.wrong("Program did not discover all the expected links.")

        links = output.strip().split('\n')
        links = [link for link in links if link.endswith(".html")]
        # Check if there are no extra links in the output
        for link in links:
            if link not in expected_links:
                return CheckResult.wrong(f"There is an extra link {link} in the output.")

        return CheckResult.correct()

    @dynamic_test
    def test9_crawling_with_invalid_url(self):
        # checks how the code handles the case when given url of a non-existing blog
        non_existing_blog = f"http://{generate_random_text(4)}.html"
        # Test crawling with an invalid URL.
        program = TestedProgram()
        output = program.start("--crawl-site", non_existing_blog).strip().lower()

        # Expected error message or indication for an invalid URL
        expected_output = f"could not reach the site: {non_existing_blog}"

        # Check if the output contains indication of an error
        if expected_output not in output:
            return CheckResult.wrong("The output does not indicate an error occurred with an invalid URL.")
        return CheckResult.correct()


# Run the tests
if __name__ == '__main__':
    http_server_process: multiprocessing.Process = None
    try:
        # creating fake blog(just html files) for testing
        create_blog_site_with_no_posts()
        create_flat_blog_site_with_multiple_posts()
        create_blog_site_with_nested_posts(5)
        create_blog_site_with_nested_and_flat_posts()
        # starting python's http.server
        http_server_process = multiprocessing.Process(target=run_http_server, args=(8000,))
        http_server_process.start()
        # running tests
        TestBlogNotifierCLI().run_tests()
    finally:
        # stopping python's http.server
        http_server_process.kill()
        # removing all the html files created
        remove_fake_blog()
