---
title: "Troubleshoot"
permalink: /docs/troubleshoot/
excerpt: ""
last_modified_at: 2023-04-29
toc: true
---

## Troubleshoot Objects

Ink/Stitch sometimes can be confusing. Especially for beginners. But also if you are using Ink/Stitch for a while, you will receive error messages, indicating that something went wrong and your shape cannot be rendered for whatever reason.

Ink/Stitch comes with an troubleshoot extension, which is designed to help you to understand the error while pointing you to the exact position were the problem lies. It will suggest how to resolve each kind of error and gives helpful tips for shapes that have issues, even if they won’t cause Ink/Stitch to error out.

### Usage

* (Optional) Select objects that you want to test. If you select none, the whole document will be tested.
* Run `Extensions > Ink/Stitch > Troubleshoot > Troubleshoot Objects`

You will either get a message, that no error could be found or a new layer with the troubleshoot information will be added to your SVG document. Use the objects panel (Ctrl + Shift + O) to delete the layer once you are finished.

![Troubleshoot Example](/assets/images/docs/en/troubleshoot.jpg)

**Tip:** It is possible that one object contains more than one error. Fill shapes only display the first error that will appear. Run the extension again, if you are receiving more error messages.
{: .notice--info }

## Remove embroidery settings

Use this function to remove the information Ink/Stitch has stored in your document.
This can be especially useful if you copy and paste objects from an embroidery design into another document.

The extensions will remove embroidery settings from your entire design or from selected objects:
* select objects
  (skip this step if you want to clear all embroidery information)
* Run `Extensions > Ink/Stitch > Troubleshoot > Remove embroidery settings...`
* Select one or all of the given options and click apply

![Remove embroidery settings - GUI](/assets/images/docs/en/remove-embroidery-settings.png)

## Cleanup Document

Sometimes you will find very small shapes and leftover objects from various operations during your designing process in your SVG file. Ink/Stitch offers a function to clean up your document and prevent those objects from causing trouble.

* Run `Extensions > Ink/Stitch > Troubleshoot > Cleanup Document...`
* Choose which types of objects should be removed and define a threshold
* Click apply

{% include upcoming_release.html %}

## Update Ink/Stitch svg

If you open a file created with an older version of Ink/Stitch you may need to update it:
* Select all objects
* Run `Extensions > Ink/Stitch > Troubleshoot > Update Ink/Stitch svg`

If you import an older file as part of a new file,  or copy/paste from an old file to a new one, you should
* Select all old objects
* Run `Extensions > Ink/Stitch > Troubleshoot > Update Ink/Stitch svg`


