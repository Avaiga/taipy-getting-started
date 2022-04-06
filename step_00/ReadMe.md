> You can download the code for this step [here](../src/step_00.py) or all the steps [here](https://github.com/Avaiga/taipy-getting-started/tree/develop/src).

# First web page

To create your first Taipy web page, you only need one line of code. Create a `Gui` object with a String and run it. A client link will be displayed in the console. Enter it in a web browser to open your first Taipy web client!

```python
from taipy import Gui

Gui(page="# Getting started with *Taipy*").run()
```

> Note that you can style the text. Taipy uses the Markdown syntax to style your text and more. Therefore, # creates a title, ## makes a subtitle. Put your text in $'**'$ for italics or in $'*'$ to have it in bold (**italics**, *bold*).

![test](results.png)


<p align="center">
    <img src="results.png" width=700>
</p>

<center>
![test](results.png)
</center>

<p align="center">
  ![test](results.png){align=center}
</p>

<div align="center">
  ![test2](results.png)
</div>

<div style="margin: auto">
  ![test3](results.png)
</div>

<p align="center">
![test111](results.png)
</p>

<div align="center">
![test112](results.png)
</div>

<div style="margin: auto">
![test113](results.png)
</div>