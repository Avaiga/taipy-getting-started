# First step in Taipy

## What is Taipy?

Taipy is an innovative **low-code** package to create complete applications in *Python*. It is composed of two independent components: a **Graphical User Interface** and a **Scenario Management** part.

<p align="center">
  <img src="taipy-gui-core-illustration.svg" height=300>
</p>

The **Graphical User Interface** of Taipy allows anyone with basic knowledge of Python to create a beautiful and interactive interface. It is a simple and intuitive way to create a GUI. No need to know how to design web pages with CSS or HTML; Taipy uses an augmented syntax of Markdown to create your desired web page.

The **Scenario Management** component of Taipy is a powerful tool to manage business problems and pipelines. The implementation of **Taipy Core** is straightforward. For example, it will allow you to:
- Keep track of your KPI, data, scenarios, pipelines, etc.
- Have smart scheduling
- Simplify industrialization for DataViz, Machine-Learning, Optimization, etc.


You can use the GUI component without the Scenario Management and vice-versa. However, as you will see, they are incredibly efficient when combined.

This **'Getting Started'** will go through all the basic concepts of *Taipy*. Each step is based on the code of the previous one. At the end of it, you will be able to create a complete application using *Taipy*. So, without further delay, let's begin to code!




## First web page

> You can download the code for this step [here](../src/step_00.py) or all the steps [here](https://github.com/Avaiga/taipy-getting-started/tree/develop/src).

To create your first Taipy web page, you only need one line of code. Create a `Gui` object with a String and run it. A client link will be displayed in the console. Enter it in a web browser to open your first Taipy web client!

```python
from taipy import Gui

Gui(page="# Getting started with *Taipy*").run()
```

> Note that you can style the text. Taipy uses the Markdown syntax to style your text and more. Therefore, # creates a title, ## makes a subtitle. Put your text in $'**'$ for italics or in $'*'$ to have it in bold (**italics**, *bold*).

<p align="center">
  <img src="result.png" width=700>
</p>
