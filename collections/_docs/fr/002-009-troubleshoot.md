---
title: "Troubleshoot Objects"
permalink: /fr/docs/troubleshoot/
excerpt: ""
last_modified_at: 2019-08-11
toc: false
---
Ink/Stitch sometimes can be confusing. Especially for beginners. But also if you are using Ink/Stitch for a while, you will receive error messages, indicating that something went wrong and your shape cannot be rendered for whatever reason.

Ink/Stitch comes with an troubleshoot extension, which is designed to help you to understand the error while pointing you to the exact position were the problem lies. It will suggest how to resolve each kind of error and gives helpful tips for shapes that have issues, even if they won’t cause Ink/Stitch to error out.

## Usage

* (Optional) Select objects that you want to test. If you select none, the whole document will be tested.
* Run `Extensions > Ink/Stitch > Troubleshoot Objects`

You will either get a message, that no error could be found or a new layer with the troubleshoot information will be added to your SVG document. Use the objects panel (Ctrl + Shift + O) to delete the layer once you are finished.

![Troubleshoot Example](/assets/images/docs/en/troubleshoot.jpg)

**Tip:** It is possible that one object contains more than one error. Fill shapes only display the first error that will appear. Run the extension again, if you are receiving more error messages.
{: .notice--info }
