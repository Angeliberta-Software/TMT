# TMT - Talking Meta Trader

An NVDA plugin for Meta Trader 5

Allows to navigate in Meta Trader 5 using hot keys.

Also this addon can read chart data from MetaTrader and represent it as sound tones, helping blind users understand trends, levels, and figures.

## Requirements

 * Latest version of Meta Trader 5 x64.
 * NVDA 2026 and higher.
 
## Basic Navigation

### Focus

* Control+1: toolbox window.
* Control+Shift+1: Focus on the toolbox tab list. After Focus use NVDA object navigation left and right to select a tab.
* Control+2: data window.
* Control+3: navigator window.
* Control+4: market watch window.
* Control+5: workspace.

Appropriate checkboxes should be checked in the View menu and all panels should be visible.

### Announce

* Control+P: current profile.
* Control+0: terminal current time.
* NVDA+T: announces an active chart instrument instead of long account number and company name.

## Chart Reading

Open a new chart or control tab to a chart you want to read.

Use the "Q" and "E" keys to hear bars as sound tones.

Use "Q" to move left (backward) and "E" to move right (forward).

Each time you move from bar to bar, you will hear two tones:
* The first tone represents the open price.
* The second tone represents the close price.

If you enable  "Play high/low" option (control+C), you will hear four tones instead:
* For a bear bar (closing price lower than opening price): open, close, high, and low.
* For a bull bar (closing price higher than opening price): open, close, low, and high.

To navigate forward and backward, as well as to hear the numerical price values, use the following key combinations:

### Keyboard Shortcuts for Chart Reading

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
- **Ctrl + C** – Toggle play high/low.
- **Ctrl + L** – Announce crossing levels.
- **Ctrl + B** – Set bars count to read. Try to Alt+Tab if this dialog is not in focus.

## Donation

If you find this addon useful fill free to donate using this link: https://www.paypal.me/vladimirsuhhorukov

## Disclaimer

By using this addon the user assumes full responsibility and fully accepts all possible risks associated with the use of this software. The authors of the software bear no liability for any potential financial losses or any other harm caused by decisions made based on information obtained through the use of this software. The user uses this software entirely at their own risk and under their sole responsibility.
