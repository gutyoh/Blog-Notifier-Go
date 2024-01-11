from hstest import StageTest, TestedProgram, CheckResult, dynamic_test

class TestBlogNotifierCLI(StageTest):

    # TODO: a.html
    @dynamic_test
    def test1_crawling_with_multiple_pages(self):
        # Test crawling a site with multiple pages.
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

        # Check if there are no extra links in the output
        for link in links:
            if link not in expected_links:
                return CheckResult.wrong(f"There is an extra link {link} in the output.")

        return CheckResult.correct()

    # TODO: f.html
    @dynamic_test
    def test2_crawling_with_no_hyperlinks(self):
        # Test crawling a site with no hyperlinks.
        program = TestedProgram()
        output = program.start("--crawl-site", "http://noblogpostsyet.com").strip()

        # Expected message for a site with no hyperlinks
        expected_message = "No blog posts found for http://noblogpostsyet.com"

        # Check if the output matches the expected message
        if output != expected_message:
            return CheckResult.wrong(f"The output does not match the expected message.\nExpected: {expected_message}\nActual: {output}")

        return CheckResult.correct()

    # TODO: remove
    @dynamic_test
    def test3_crawling_with_invalid_url(self):
        # Test crawling with an invalid URL.
        program = TestedProgram()
        output = program.start("--crawl-site", "invalid_url").strip().lower()

        # Expected error message or indication for an invalid URL
        expected_phrases = ["error", "invalid", "could not reach", "not found"]

        # Check if the output contains indication of an error
        if not any(phrase in output for phrase in expected_phrases):
            return CheckResult.wrong("The output does not indicate an error occurred with an invalid URL.")

        return CheckResult.correct()

    # TODO: create a alpha.html, with nested hyperlinks with depth > 3
    @dynamic_test
    def test4_crawling_with_depth_limit(self):
        # Test crawling with a depth limit of 3.
        program = TestedProgram()
        output = program.start("--crawl-site", "https://depthlimit.com").strip()

        # Mocked output for depth 3 limit, assuming known structure
        expected_links = [
            "https://depthlimit.com/level1.html",
            "https://depthlimit.com/level2.html",
            "https://depthlimit.com/level3.html"
        ]

        # Splitting the output into lines for easier assertion
        links = output.strip().split('\n')

        # Check if all expected links are present in the output
        for link in expected_links:
            if link not in links:
                return CheckResult.wrong(f"The link {link} was not found in the output.")

        # Check if there are no links beyond depth 3
        for link in links:
            if link.count('/') > 4:  # Assuming the format https://domain.com/level
                return CheckResult.wrong(f"A link {link} was found that exceeds the depth limit of 3.")

        return CheckResult.correct()

    # TODO: index.html
    @dynamic_test
    def test5_crawling_with_duplicate_links(self):
        # Test crawling a site with duplicate hyperlinks.
        program = TestedProgram()
        output = program.start("--crawl-site", "https://duplicatelinks.com").strip()

        # Mocked output with duplicates, assuming known structure
        links_output = output.split('\n')

        # Check for duplicates by comparing set and list lengths
        if len(links_output) != len(set(links_output)):
            return CheckResult.wrong("The output contains duplicate links.")

        return CheckResult.correct()

# Run the tests
if __name__ == '__main__':
    TestBlogNotifierCLI().run_tests()
