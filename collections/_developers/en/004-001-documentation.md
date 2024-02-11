---
title: "Documentation"
permalink: /developers/documentation/
last_modified_at: 2020-10-04
toc: true
---
We want to describe every possible function with text, images, and/or videos. We also want to provide instructions about the installation process and give an overview of the best workflow. Additionally, we want to provide sample files which other users can make use of. It also would be nice to get some example images of embroidered designs to prove what Ink/Stitch is able to do.

Another, yet quite incomplete, part of the documentation will be to help other developers get started diving into the code, and enable them to introduce new functionalities to Ink/Stitch or whatever they might come up with.

## Get involved
This website needs a lot of care, generating new content and updating existing content with the ongoing developement of Ink/Stitch. We could use any helping hand.

You do not need to know how to build a website, since we use [Markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/) for text formatting. All files needed to build the website can be found in the [gh-pages-branch](https://github.com/inkstitch/inkstitch/tree/gh-pages) GitHub.

If you have an interest in helping with the documentation, file an issue on [github](https://github.com/inkstitch/inkstitch/issues) and tell us that you are willing to help.

## Working with Github-Pages

Github-Pages makes use of [Jekyll](https://jekyllrb.com/), a static page generator. It is also possible to install it locally for test purposes. For instructions see their website.
We are using the [Minimal Mistakes Theme](https://mmistakes.github.io/minimal-mistakes/), with very few customizations.

### Basic File Structure

* `_collections/_posts/language` news
* `_collections/_docs/language` documentation
* `_collections/_tutorials/language` tutorial main pages
* `_collections/_tutorial/language` specific tutorials
* `_collections/_developers/language` developer documentation
* `_pages/language` static pages such as about, terms or sitemap
* `assets/language` media files (images) and website styling (css)
* `_data/navigation_language.yml` data for every navigation found in the website

### Changing Existing Files
Change the content as you wish. Style your text with [markdown](https://help.github.com/articles/basic-writing-and-formatting-syntax/), which is also used with Github issues, etc.

Before saving the file, please also change the date on top of the page.

### Adding New Files

#### Docs, Tutorials, Developers
When adding new pages please be aware of the numbering in the file name (for docs and tutorials).

Numbers are set to allow us to use previous/next links below the article for navigation. They also apply to the sidebar menu structure, which you also should update when adding new pages.

Changing file names will not prevent the website from finding the files, since they use permalinks. So you can go ahead and change the numbers to your needs.

Every page should start with something like this:

```
---
title: "Some Title"
permalink: /unique/permalink
excerpt: "Small description of what the document is about"
last_modified_at: yyyy-mm-dd # e.g. 2018-05-05
toc: true # set to false or delete if you don't wish to display a table of contents
---
```

#### Posts (News)

File names for posts follow a certain structure. They should be named like this: yyyy-mm-dd-title.md

Every post should start with the following entry:

```
---
title:  "Some News"
date:   yyy-mm-dd
categories: news-category
---
```

### Additional Functions

#### Galleries

Adding galleries has become really simple: upload files into a new folder within `/assets/images/galleries/`.
Then add: 

{% raw %}
```
{% include folder-galleries path="new-folder-name/" %}
```
{% endraw %}
wherever you want to display a gallery containing `new-folder-name`'s content.

If you want to provide preview images for faster loading, add -th to filename. E.g. `image.jpg` would use `image-th.jpg` as its preview. Both files have to be in the same folder as specified in the include statement.

#### Categorising tutorials

Tutorial files in the `_tutorial` folder should contain some keywords in the header to describe the particular tutorial. This could look like this:


```
---
permalink: /tutorials/applique/
title: Applique
last_modified_at: 2018-05-11
excerpt: "Applique example file"
image: "/assets/images/tutorials/samples/Applique Color Change.svg"
language: en
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

These categories then can be used to list tutorials with a specific keyword, e.g. 
{% raw %}
```
{% include tutorials/tutorial_list key="stitch-type" value="Fill Stitch" %}
```
{% endraw %}
would display a list of all tutorial files which have "fill stitch" specified in their header.

They can also be used to display a full list of categories. In this case, categories need to be specified by every call of tutorial lists. Example:

{% raw %}
```
{% assign tutorial_cats = 'Tutorial Type*Stitch Type*Techniques*Field Of Use*User Level' | split: '*' %}
{% include tutorials/display_tutorials tutorial_cats=tutorial_cats %}
```
{% endraw %}


