package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"

	"github.com/PuerkitoBio/goquery"
)

const MAX_DEPTH = 3

// finds all the links in a blog post
func findAllLinks(site string) ([]string, error) {
	res, err := http.Get(site)
	if err != nil {
		return nil, fmt.Errorf("could not reach the site: %s", site)
	}
	defer res.Body.Close()
	if res.StatusCode != 200 {
		return nil, err
	}

	// Load the HTML document
	doc, err := goquery.NewDocumentFromReader(res.Body)
	if err != nil {
		return nil, err
	}

	// Initialize an empty slice to store discovered links
	links := make([]string, 0)

	// Iterate over all 'a' (anchor) elements in the HTML document
	doc.Find("a").Each(func(i int, s *goquery.Selection) {
		// Extract the 'href' attribute value from each 'a' element
		link, exists := s.Attr("href")
		if exists {
			// Add the discovered link to the slice
			links = append(links, link)
		}
	})
	return links, nil
}

// recursive crawl function
func _crawl(link string, links *[]string, depth int) error {
	if depth > MAX_DEPTH {
		return nil
	}
	_links, err := findAllLinks(link)
	if err == nil {
		for _, _link := range _links {
			*links = append(*links, _link)
			err := _crawl(_link, links, depth+1)
			if err != nil {
				return err
			}
		}
		return nil
	} else {
		return err
	}
}

// implements the crawl functionality
func crawl(blogSite string) ([]string, error) {
	// crawl the sites

	links := make([]string, 0)
	err := _crawl(blogSite, &links, 0)
	if err != nil {
		return nil, err
	} else {
		uniqueLinksMap := make(map[string]bool)
		uniqueLinks := make([]string, 0)
		for _, _link := range links {
			if _, ok := uniqueLinksMap[_link]; !ok {
				uniqueLinks = append(uniqueLinks, _link)
				uniqueLinksMap[_link] = true
			}
		}
		return uniqueLinks, nil
	}

}

func main() {
	// Parse command-line arguments
	crawlFlag := flag.String("crawl-site", "", "Crawl the given website")

	flag.Parse()

	if *crawlFlag != "" {
		_links, err := crawl(*crawlFlag)
		if err != nil {
			log.Fatal(err)
		}
		if len(_links) == 0 {
			fmt.Printf("No blog posts found for %s\n", *crawlFlag)
		}
		for _, _link := range _links {
			fmt.Println(_link)
		}
	}
}
