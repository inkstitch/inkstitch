
### This allows you to use the MSYS2 UCRT terminal in VS Code

* `C:\Users\%USERNAME%\AppData\Roaming\Code\User\settings.json`
* Add the following configuration:

```json
{
    "terminal.integrated.profiles.windows": {
            "MSYS2 UCRT": {
                "path": "ucrt.bat",
            }
        }
}
```