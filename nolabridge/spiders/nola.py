import scrapy
import json
from feedgen.feed import FeedGenerator

class NolaSpider(scrapy.Spider):
    name = "nola"
    start_urls = [
        "https://nola.com/news/"
    ]

    def parse(self, res):
        keys = [
            "headline",
            "link",
            "summary",
            "authors",
            "image"
        ]

        headlines = res.css("div.river-item__content > h2.river-item__headline > a.river-item__headline-link::text").getall()
        links = res.css("div.river-item__content > h2.river-item__headline > a.river-item__headline-link::attr(href)").getall()
        summaries = res.css("div.river-item__content > p.river-item__summary::text").getall()
        authors = res.css("a.river-item__byline-link::text").getall()
        image_links = res.css("img.river-item__thumbnail-image::attr(data-src)").getall()

        self.log("Lengths: headlines %d, links %d, summaries %d, authors %d, images %d" % (len(headlines), len(links), len(summaries), len(authors), len(image_links)))

        fg = FeedGenerator()
        fg.id("nola.rss.idlecore.dev")
        fg.title("NOLA.com Idlecore")
        fg.link(href="https://nola.com/news/", rel="alternate")
        fg.subtitle("NOLA.com news feed. Compiled by idlecore from nola.com/news.")
        fg.link(href="nola.rss.idlecore.dev", rel="self")
        fg.language("en")

        for i in [dict(zip(keys, x)) for x in zip(headlines, links, summaries, authors, image_links)]:
            self.log("Adding: %s" % i["headline"])
            fe = fg.add_entry()
            fe.id(i["link"])
            fe.title(i["headline"])
            fe.description(i["summary"])
            fe.link(href=i["link"])
            fe.enclosure(i["image"], 0, 'image/jpg')

        fg.atom_str(pretty=True)
        fg.atom_file("test.xml")
