Ink/Stitch Localization
=======================

The goal of the Ink/Stitch project is to put free, high-quality embroidery design tools in the hands of folks that might normally not have access to such tools.  To further that goal, we seek to support as many languages and locales as possible.

Ink/Stitch supports displaying text in the user's preferred language in the following places:
  * dialogs (such as Params and Install Add-Ons for Inkscape)
  * print PDF
  * error messages
  * extension settings dialogs and menu items
    * these are managed by Inkscape

Future work will add translations for project documentation (such as this file) and the <a href="https://inkstitch.org/">Ink/Stitch website</a>.

Help wanted!
-----------

Want to help translate?  We'd really appreciate your contributions!  Ink/Stitch uses a the collaborative translation platform <a href="http://crowdin.com">Crowdin</a> to facilitate community translations.  Through their generous open source program, we're able to use their platform free of charge, and we greatly appreciate their support.

To start translating, visit our <a href="https://crowdin.com/project/inkstitch">project page on Crowdin</a>.  It's easy to sign in using your GitHub account.  Pick a language and start suggesting translations!

Approved contributors can accept your translations, which causes them to be committed to this repository within 24 hours.  If you'd like to become an approver, please ping [**@lexelby**](https://github.com/lexelby) or another approved contributor, or email **inkstitch-l10n** at **lex** dot **gd**.

**Please note that our [code of conduct](CODE_OF_CONDUCT.md) also covers contributions and interactions on our Crowdin page.**

Continuous Translation
----------------------

When new code is added to Ink/Stitch, user-facing text can change and new messages can be added.  These changes will be uploaded to Crowdin within 24 hours and made available for contributors to translate.

Sometimes, it's necessary to see how your translated text looks in Ink/Stitch.  In order to do this, follow these steps:

1. Wait up to 24 hours until your new translations are committed to Ink/Stitch ([example](https://github.com/inkstitch/inkstitch/commit/96c319f870f7da5370ac4f3378f2cf6de0e0ccde)).
2. Make a new branch by following [these instructions](https://help.github.com/articles/creating-and-deleting-branches-within-your-repository/).
3. Once your build finishes, it will be posted to our [releases page](https://github.com/inkstitch/inkstitch/releases).

In order to do the above steps, you'll need to be added as a collaborator on this repository.  You can ping [**@lexelby**](https://github.com/lexelby) or email **inkstitch-l10n** at **lex** dot **gd** and we'll get you set up.
