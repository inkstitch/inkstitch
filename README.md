# Ink/Stitch Homepage

This branch is used for the Ink/Stitch homepage: <https://inkstitch.org>

## Why this Website?
We want to describe every possible function with text, images and/or videos. Giving instructions about the installation process and give an overview of the best workflow.
Additionally we want to provide sample files which other users can make use of.

It also would be nice to get some example images of embroidered designs to prove what Ink/Stitch is able to do (as an appetizer for newcomers - and of course because we are so excited to see beautiful results!!!).

## Sounds good - but where do I find all this stuff
The website still needs a lot of work to fullfill its purpose to serve as a complete documentation on how to use the Inkscape Plugin.

Do you already have some experience using Ink/Stitch and want to help documenting or share images? You are very welcome to do so!

## Working with Github-Pages

Github-Pages make use of [Jekyll](https://jekyllrb.com/), a static page generator. It is also possible to install it locally for test purposes. For instructions see their website.
We are using the [Minimal Mistakes Theme](https://mmistakes.github.io/minimal-mistakes/), with very little customizations.

### Basic File Structure

* `_collections/_posts/language` news
* `_collections/_docs/language` documentation
* `_collections/_tutorials/language` tutorial main pages
* `_collections/_tutorial/language` specific tutorials
* `_collections/_developers/language` developers documentation
* `_pages/language` static pages such as about, terms or sitemap
* `assets/language` media files (images) and website styling (css)
* `_data/navigation_language.yml` data for every navigation found in the website

### Changing Existing Files
Change the content as you wish. Style your text with [markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/), which is also used with github issues, etc.

Before saving the file, please also change the date on top of the page.

### Adding New Files

#### Docs, Tutorials
When adding new pages please be aware of the file name numbering (docs and tutorials).

Numbers are set to be able to use previous/next links below the article. They also fit to the sidebar menu structure, which you also should update when adding new sites.

Changing file names will not prevent the website from finding the files, since they use permalinks. So you can go ahead and change the numbers to your needs.

Every page should start with something like this:
```
---
title: "Some Title"
permalink: /unique/permalink
excerpt: "Small description what the document is about"
last_modified_at: yyyy-mm-dd # e.g. 2018-05-05
toc: true # set to false or delete if you don't wish to display a table of contents
---
```

#### Posts (News)

Post file names follow a certain structure, they should be named like this: yyyy-mm-dd-title.md

Every post should start with the following entry:

```
---
title:  "Some News"
date:   yyy-mm-dd
categories: news-category
---
```

#### Additional Functions

##### Galleries

Adding galleries has become really simple: upload files into a new folder within `/assets/images/galleries/`.
Then add: `{% include folder-galleries path="new-folder-name/" %}` where ever you want to display a gallery containing `new-folder-name`s content.

If you want to provide preview images for faster loading, add -th to filename. E.g. `image.jpg` would use `image-th.jpg` as it's preview. Both files have to be in the same folder as specified in the include statement.

##### Categorising tutorials

Tutorial files in `_tutorial` folder should contain some keywords in the header to describe the particular tutorial. This could look like this:

```
---
permalink: /tutorials/applique/
title: Applique
last_modified_at: 2018-05-11
excerpt: "Applique example file"
image: "/assets/images/tutorials/samples/Applique Color Change.svg"

tutorial-type:
  - Sample File
  - Text
stitch-type: 
  - Running Stitch
  - Fill Stitch
  - Satin Stitch
techniques:
  - Applique
field-of-use:
user-level: Beginner
---
```

These categories then can be used to list tutorials with a specific keyword, e.g. `{% include tutorials/tutorial_list key="stitch-type" value="Fill Stitch" %}` would display a list of all tutorial files which have fill stitch specified in their header.

They can also be used to display a full list of categories. In this case categories need to be specified by every call of tutorial lists. Example:
```
{% assign tutorial_cats = 'Tutorial Type*Stitch Type*Techniques*Field Of Use*User Level' | split: '*' %}
{% include tutorials/display_tutorials tutorial_cats=tutorial_cats %}
```

