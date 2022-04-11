> You can download the code for this step [here](../src/step_00.py) or all the steps [here](https://github.com/Avaiga/taipy-getting-started/tree/develop/src).

# Step 0: First web page

To create your first Taipy web page, you only need one line of code. Create a `Gui` object with a String and run it. A client link will be displayed in the console. Enter it in a web browser to open your first Taipy web client!

```python
from taipy import Gui

# A dark mode is available in Taipy
# However, we we will use the light mode for the Getting Started
Gui(page="# Getting started with *Taipy*").run(dark_mode=False)
```

Note that you can style the text. Taipy uses the Markdown syntax to style your text and more. Therefore, `#` creates a title, `##` makes a subtitle. Put your text in `*` for *italics* or in `**` to have it in **bold**.


![First Web Page](result.png){ width=700 style="margin:auto;display:block" }
