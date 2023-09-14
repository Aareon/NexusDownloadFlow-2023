# NexusDownloadFlow 2023 : Auto clicker script using computer vision

NexusDownloaderFlow (NDF) 2023 is a script that takes screenshots and detects if any template matches with the
screenshot taken. It was made to automate process with `Wabbajack modlist installation of Nexus' mods` in which
you have to manually click on `Slow download` button is your NexusMods account is not premium.

## How to use NDF 2023?

Just execute `NexusDownloadFlow 2023.exe` and open your NexusMods' download page.

## Configuration

The default delay for checking for the download button is 5 seconds. This value can be changed in `NexusDownloadFlow 2023/config.toml` by changing the `check_delay` value. It is not recommended to set this any lower than 1.

## Auto clicker is not clicking

Do not worry, you have to replace the templates files where you installed NDF with the one you will screenshot:
`NexusDownloadFlow 2023/assets/template{x}.png`

+ `template1.png` is the raw `Slow download` button
+ `template2.png` is the `Slow download` button with mouse hovering over
+ `template3.png` is the `Click here` link appearing after clicking on `Slow download` button

## Credits

Thanks to [parsiad](https://github.com/parsiad) for his repository [parsiad/nexus-autodl](https://github.com/parsiad/nexus-autodl)

Thanks to [greg-ynx](https://github.com/greg-ynx) for his work on the [2022 version](https://github.com/greg-ynx/NexusDownloadFlow-2022) of this program.

## Requirements

+ `PyAutoGUI==0.9.54`
+ `opencv-python==4.5.5.64`
+ `mss==6.1.0`
+ `toml==0.10.2`
