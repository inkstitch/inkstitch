---
title: "Ink/Stitch Localization"
permalink: /docs/help/localize/
excerpt: ""
last_modified_at: 2018-04-14
toc: false
---
The goal of the Ink/Stitch project is to put free, high-quality embroidery design tools in the hands of folks that might normally not have access to such tools.  To further that goal, we seek to support as many languages and locales as possible.

Ink/Stitch supports displaying text in the user's preferred language in the Params dialog and in error messages displayed by the Embroider extension.  Future work will add translations for the extension settings window (displayed by Inkscape) and project documentation (such as this file).

## Help wanted!

Want to help translate?  We'd really appreciate your contributions!  Ink/Stitch uses a the collaborative translation platform <a href="http://crowdin.com">CrowdIn</a> to facilitate community translations.  Through their generous open source program, we're able to use their platform free of charge, and we greatly appreciate their support.

To start translating, visit our <a href="https://crowdin.com/project/inkstitch">project page on CrowdIn</a>.  It's easy to sign in using your GitHub account.  Pick a language and start suggesting translations!

Approved contributors can accept your translations, which causes them to be submitted to this GitHub repository as a pull request.  If you'd like to become an approver, please ping [**@lexelby**](https://github.com/lexelby) or another approved contributor, or email **inkstitch-l10n** at **lex** dot **gd**.

**Please note that our [code of conduct](CODE_OF_CONDUCT.md) also covers contributions and interactions on our CrowdIn page.**

## Continuous Translation

When new code is added to ink/stitch, user-facing text can change and new messages can be added.  CrowdIn picks these changes up automatically and makes the new messages available to translators.

When CrowdIn creates a pull request, our [Travis-CI](http://travis-ci.org) integration (also generously provided for free!) picks up the new translations and builds a new version of Ink/Stitch as a development release.  Once Travis-CI finishes building, the new version is posted to our releases page [here](https://github.com/inkstitch/inkstitch/releases/tag/dev-build-l10n), and you can install it and make sure everything looks right before we merge.
