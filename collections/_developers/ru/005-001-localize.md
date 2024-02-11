---
title: "Localization"
permalink: /ru/developers/localize/
last_modified_at: 2021-10-03
toc: true
---
The goal of the Ink/Stitch project is to put free, high-quality embroidery design tools in the hands of folks that might normally not have access to such tools.  To further that goal, we seek to support as many languages and locales as possible.

Ink/Stitch supports displaying text in the user's preferred language in the following places:
  * dialogs (such as params)
  * print / realistic preview
  * error messages
  * extension settings dialogs and menu items (managed by Inkscape)
  * Ink/Stitch website

## Ink/Stitch User Interface

Want to help translate?  We'd really appreciate your contributions!  Ink/Stitch uses a the collaborative translation platform [Crowdin](http://crowdin.com) to facilitate community translations.  Through their generous open source program, we're able to use their platform free of charge, and we greatly appreciate their support.

To start translating, visit our [project page on Crowdin](https://translate.inkstitch.org).  It's easy to sign in using your GitHub account.  Pick a language and start suggesting translations!

**Info:** If you want your language to appear in the release section of Ink/Stitch, watch out for the string `"Generate INX files"` and make sure you create a translation for it. This is the key for Ink/Stitch to create the menu files in your language.
{: .notice--warning }

Approved contributors can accept your translations, which causes them to be committed to this repository within 24 hours.  If you'd like to become an approver, please contact us on [GitHub](https://github.com/inkstitch/inkstitch/issues).

**Please note that our [code of conduct](https://github.com/inkstitch/inkstitch/blob/main/CODE_OF_CONDUCT.md) also covers contributions and interactions on our Crowdin page.**

### Continuous Translation

If you find these steps too complicated just add your translations to our [project page on Crowdin](https://crowdin.com/project/inkstitch) and inform us about your update.
{: .notice--info}

When new code is added to Ink/Stitch, user-facing text can change and new messages can be added.  These changes will be uploaded to Crowdin within 24 hours and made available for contributors to translate.

Sometimes, it's necessary to see how your translated text looks in Ink/Stitch.  In order to do this, follow these steps:

1. Wait up to 24 hours until your new translations are committed to Ink/Stitch ([example](https://github.com/inkstitch/inkstitch/commit/96c319f870f7da5370ac4f3378f2cf6de0e0ccde)).
2. Make a new branch by following [these instructions](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/). This will trigger a development release to be build.
3. Once your build finishes, it will be posted to our [releases page](https://github.com/inkstitch/inkstitch/releases).

In order to do the above steps, you'll need to be added as a collaborator on this repository.  You can contact us through [GitHub](https://github.com/inkstitch/inkstitch/issues) and we'll get you set up.

## Website

This website is multilingual. When you are willing to translate the documentation please ask for directions on [GitHub](https://github.com/inkstitch/inkstitch/issues).

If your native language is already translated, have a look at the list below. The list contains pages which are not translated yet or will need an update.

{% include compare_translations %}
