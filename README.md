# TMT - Talking Meta Trader
An NVDA plugin for Meta Trader 5

Currently this is a super pre alpha activly developing version. Bugs are included.
## Requirements
 Meta Trader 5 x64
## Instalation
* Go to NVDA settings.
* Go to addvanced.
* Check "I understand that changing these settings may cause NVDA to function incorrectly."
* Check "Enable loading custom code from Developer Scratchpad directory"
* Click "Open developer scratchpad directory" button.
* Open or create a folder named "appModules"
* Extract the archive here.

Thus, the path to addon files should be like "C:\Users\[YourUserName]\AppData\Roaming\nvda\scratchpad\appModules\terminal64"

Restart the NVDA now.
## Basic Navigation
### Focus
* Control+1: toolbox window.
* Control+Shift+1: Focus on the toolbox tab list. Currently it uses OCR to retrieve tab names. After OCR use up and down arrows to select the tab you need.
* Control+2: data window.
* Control+3: navigator window.
* Control+4: market watch window.
* Control+5: workspace.

Appropriate checkboxes should be checked in the View menu and all panels should be visible.

### Announce
* Control+P: current profile.
* Control+0: terminal current time.
* NVDA+T: announces an active chart instrument instead of long account number and company name.
## Chart Reader
This addon comes with a standalone application called ChartReader.

ChartReader can read chart data from MetaTrader and convert it into an HTML table or represent it as sound tones, helping blind users understand trends, levels, and figures.

To start, run ChartReader.exe located in the addon's folder. If you see a Windows security warning, you can safely ignore it. You may also create a desktop shortcut for quicker access in the future.

Click the "Initialize MetaTrader" button. This will also launch the MetaTrader application if it is not already running.

In MetaTrader, press Control + Shift + 0. You should hear a couple of beeps.

Now, in ChartReader, you can either click the "Show in table" button to view the data in table format or use the "Q" and "E" keys to hear bars as sound tones.

As soon as ChartReader receives data from MetaTrader, it will play the most recent bar from the chart (today's bar if the chart is set to daily). Use "Q" to move left (backward) and "E" to move right (forward).

Each time you move from bar to bar, you will hear two tones:
* The first tone represents the open price.
* The second tone represents the close price.

If you check the "Play high/low" checkbox, you will hear four tones instead:
* For a bear bar (closing price lower than opening price): open, close, high, and low.
* For a bull bar (closing price higher than opening price): open, close, low, and high.

To navigate forward and backward, as well as to hear the numerical price values, use the following key combinations:
### Keyboard Shortcuts for ChartReader

#### Navigation

- **Ctrl + Shift + I** – Announce current chart and time frame.
- **Ctrl + Shift + Q** – Go to the first bar.
- **Ctrl + Shift + E** – Go to the last bar.
- **Shift + Q** – Move 5 bars back.
- **Shift + E** – Move 5 bars forward.
- **Ctrl + Q** – Move 12 bars back.
- **Ctrl + E** – Move 12 bars forward.
- **Q** – Go to the previous bar.
- **E** – Go to the next bar.

#### Price Information

- **A** – Announce the open price.
- **D** – Announce the close price.
- **S** – Announce the low price.
- **W** – Announce the high price.
- **F** – Announce the date.
- **V** – Announce the volume.
- **C** – Announce the current price.

#### Other Functions

- **P** – Play preview.
