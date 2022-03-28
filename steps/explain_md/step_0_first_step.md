# What is Taipy?

Taipy is an innovative low-code package to create full applications in Python. It is composed of two independant components: the **Graphical User Interface** and the **Scenario Management**.

<p align="center">
  <img src="/steps/images/taipy-gui-core-illustration.svg" height=300>
</p>

The **Graphical User Interface** allows anyone with basic knowledge in Python to create a graphical user interface. It is a simple and intuitive way to create a GUI.
- Minimal knowledge in Python
- No need to know how to design web pages, css, html, etc.
- Augmented syntax for Markdown
- Interactive

The **Scenario Management** of Taipy is a powerful tool to manage your scenarios and pipelines. A scenario is your business problem with initial parameters. The implementation of **Taipy Core** is intuitve and easy. It will allow you:
- To keep track of your KPI, data, scenarios, pipelines, etc.
- To have smart scheduling in your Python code


You can use the GUI component without the Scenario Management and vice-versa. However, as you will see, they are incredibly efficient when combined.

## First web page

To create your first Taipy web page, you only need one line of code. Create a Gui object with a String and run it. Then, the client link will be displayed in the console. Enter the URL in a web browser to open your first Taipy web client!

```python
from taipy.gui import Gui

Gui(page="# Getting started with *Taipy*").run()
```

> Note that you can style the text. Taipy uses the Markdown syntax to style your text and more. Therefore, # creates a title, ## makes a subtitle. Put your text in $'**'$ for italics or in $'*'$ to have it in bold (**italics**, *bold*).

<p align="center">
  <img src="/steps/images/step_0_result.png" width=700>
</p>
