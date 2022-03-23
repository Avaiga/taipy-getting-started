**Taipy** is composed of two concepts: the **Graphical User Interface** and the **Scenario Management**. These two components are independent. You can use the GUI component without the Scenario Management and vice-versa. However, as you will see, they are incredibly efficient when combined.

<center><img src="/steps/images/taipy-gui-core-illustration.svg" height=500px width=500px></center>

To create your first Taipy web page, you only need one line of code. Create a Gui object with a String and run it. Then, the client link will be displayed in the console. Enter the URL in a web browser to open your first Taipy web client!

Note that you can style the text. Taipy uses the Markdown syntax to style your text and more. Therefore, # creates a title, ## makes a subtitle. Put your text in $'**'$ for italics or in $'*'$ to have it in bold (**italics**, *bold*).

```python
from taipy.gui import Gui

Gui(page="# Getting started with *Taipy*").run()
```

<center><img src="/steps/images/step_0_result.png"></center>