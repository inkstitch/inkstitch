# Ink/Stitch Homepage

This branch is used for the Ink/Stitch homepage: <https://inkstitch.org>

## Purpose of the website.
Our goal is to document the features of Ink/Stitch using text, images, and videos.  You’ll find installation instructions, workflow recommendations, and downloadable sample files that you can use in your own projects.

We would also love to showcase photos of embroidery made from designs created with Ink/Stitch, both to inspire new users and to celebrate the amazing work of our community!

## Where is everything
This website it a work in progress.  

Our long-term goal is to provide complete, easy-to-follow documentation for the entire Inkscape plugin.

If you already have experience with Ink/Stitch and would like to help by writing documentation or sharing sample images, we’d be very happy to have your contributions!

## Working with Github-Pages

This website uses [Jekyll](https://jekyllrb.com/), a static site generator. You can also install Jelly locally for testing. For instructions see their website.
We are using the [Minimal Mistakes Theme](https://mmistakes.github.io/minimal-mistakes/), with only minor customizations.

### Basic file structure

* `_collections/_posts/language` news
* `_collections/_docs/language` documentation
* `_collections/_tutorials/language` tutorial main pages
* `_collections/_tutorial/language` specific tutorials
* `_collections/_developers/language` developers documentation
* `_pages/language` static pages such as about, terms or sitemap
* `assets/language` media files (images) and website styling (css)
* `_data/navigation_language.yml` data for every navigation found in the website

### Changing existing files
Feel free to edit content as needed. 
All pages use [markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/) (which is the same syntax used in Github issues).

Before saving your changes, please update the date at the top of the file.

### Adding new files

#### Document and tutorials
When adding new pages, follow the existing filename numbering system used for documents and tutorials.

The numbering preserves the correct order for the *previous/next* navigation links and keeps the sidebar structured. 

You can change numbers if needed.  The permalinks ensure the site will still find the correct page.

For continuity, every page should start with this:
```
---
title: "Some Title"
permalink: /unique/permalink
excerpt: "Small description what the document is about"
last_modified_at: yyyy-mm-dd # Example: 2018-05-04 for May 4, 2018
toc: true # set to false or delete if you don't wish to display a table of contents
---
```

#### Posts (News)

News posts must follow this filename format:
yyyy-mm-dd-title.md

For continuity, every post should begin with::

```
---
title:  "Some News"
date:   yyyy-mm-dd
categories: news-category
---
```

#### Additional features

##### Galleries

Adding image galleries is simple:
1. Create a new file in /assets/images/galleries/ and upload your images.
2. Add this line wherever you want the gallery to appear:
 `{% include folder-galleries path="new-folder-name/" %}` 

For faster loading, you can include preview images.

For example, if your files is `image.jpg`, add a thumbnail named `image-th.jpg` in the same folders. The thumbnail will load automatically.  Both files have to be in the same folder as specified in the include statement.

##### Categorising tutorials

Tutorial files in `_tutorial` folder should include descriptive keywords in the header to describe the particular tutorial. For example:

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

You can liste tutorials by keyword, for example: 
`{% include tutorials/tutorial_list key="stitch-type" value="Fill Stitch" %}` 
This would display a list of all tutorials which have *Fill Stitch* specified in their header.

Or to display a full list of tutorila categories, for example:
```
{% assign tutorial_cats = 'Tutorial Type*Stitch Type*Techniques*Field Of Use*User Level' | split: '*' %}
{% include tutorials/display_tutorials tutorial_cats=tutorial_cats %}
```