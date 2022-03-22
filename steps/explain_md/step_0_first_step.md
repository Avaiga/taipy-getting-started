**Taipy** is composed of two different concepts: the **Graphical User Interface** and the **Scenario Management**. These two components are independant. You can use the GUI component without the Scenario Management and vice-versa. However, as you will see, they are extremely efficient when combined.

<img src="/steps/images/taipy-gui-core-illustration.svg" height=500px width=500px/>

To create your first Taipy web page. To do so, you just need one line of code. Create a Gui object with a String and run it. Then, the client link will be displayed in the console. Enter the URL in a web browser to open your very first Taipy web client!

Note that the text can be styled. Taipy uses the Markdown syntax to style your text and more. Therefore, # creates a title, ## creates a subtitle. Put your text in $'**'$ to have it in italics or in $'*'$ to have it in bold (**italics**, *bold*).

```python
from taipy.gui import Gui

Gui(page="# Getting started with *Taipy*").run()
```

<img src="/steps/images/step_0_result.png" />
