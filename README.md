# TMT - Talking Meta Trader

An NVDA plugin for Meta Trader 5

Allows to navigate in Meta Trader 5 using hot keys.

This addon comes with a standalone application called ChartReader.ChartReader can read chart data from MetaTrader and convert it into an HTML table or represent it as sound tones, helping blind users understand trends, levels, and figures.

## Requirements

 Meta Trader 5 x64
 
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

#### Ruler

- **Ctrl + S/W/A/D** – Set ruler start marker. If set, announces price difference and bar count.

#### Markers

- **M** – Place a marker
- **Shift + M** – Remove a marker
- **]** – Next marker
- **[** – Previous marker

#### Levels

- **Shift + S/W/A/D** – Set level
- **Shift + L** – Remove selected level
- **T** – Next level
- **G** – Previous level
- **L** – Closest level to current price

#### Other Functions

- **P** – Play preview.
- **R** – Say last output

## **Disclaimer**
By using this add-on and the accompanying software, the user assumes full responsibility and fully accepts all possible risks associated with the use of this software. The authors of the software bear no liability for any potential financial losses or any other harm caused by decisions made based on information obtained through the use of this software. The user uses this software entirely at their own risk and under their sole responsibility.
