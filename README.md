# Ink/Stitch Homepage #

This branch is used for the Ink/Stitch homepage: <https://inkstitch.org>

## Why this Website? ##
We want to describe every possible function with text, images and/or videos. Giving instructions about the installation process and give an overview of the best workflow.
Additionally we want to provide sample files which other users can make use of.

It also would be nice to get some example images of embroidered designs to prove what Ink/Stitch is able to do (as an appetizer for newcomers - and of course because we are so excited to see beautiful results!!!).

## Sounds good - but where do I find all this stuff ##
The website still needs a lot of work to fullfill its purpose to serve as a complete documentation on how to use the Inkscape Plugin.

Do you already have some experience using Ink/Stitch and want to help documenting or share images? You are very welcome to do so!

## Working with Github-Pages ##

Github-Pages make use of [Jekyll](https://jekyllrb.com/), a static page generator. It is also possible to install it locally for test purposes. For instructions see their website.
We are using the [Minimal Mistakes Theme](https://mmistakes.github.io/minimal-mistakes/), with very little customizations.

### Basic File Structure ###

* `_posts` news
* `_docs` documentation
* `_tutorials` tutorial
* `_pages` static pages such as about, terms or sitemap
* `assets` media files (images) and website styling (css)
* `_data/navigation.yml` data for every navigation found in the website

### Changing Existing Files ###
Change the content as you wish. Style your text with [markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/), which is also used in github for writing issues, etc.

Before saving the file, please also change the date on top of the page.

### Adding New Files ###

#### Docs, Tutorials ####
When adding new pages please be aware of the file name numbering (docs and tutorials).

Numbers are set to be able to use previous/next links below the article. They also fit to the sidebar menu structure, which you also should update when adding new sites.

Changing file names will not prevent the website from finding the files, since they use permalinks. So you can go ahead and change the numbers to your needs.

Every page should start with something like this:
```
---
title: "Some Title"
permalink: /unique/permalink
excerpt: "Small description what the document is about"
last_modified_at: yyyy-mm-dd # f.e. 2018-05-05
toc: true # set to false or delete if you don't wish to see a table of contents
---
```

#### Posts (News) ####

Post file names follow a certain structure, they should be named like this: yyyy-mm-dd-title.md

Every post should start with the following entry:

```
---
title:  "Some News"
date:   yyy-mm-dd
categories: news-category
---
```
