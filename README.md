# Taipy Getting Started version: 2.2.0

## License
Copyright 2023 Avaiga Private Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with
the License. You may obtain a copy of the License at
[http://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0.txt)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

## Usage

- [License](#license)
- [Usage](#usage)
- [Taipy Getting Started](#what-is-taipy-getting-started)
- [Installation](#installation)
- [Contributing](#contributing)
- [Code of conduct](#code-of-conduct)
- [Directory Structure](#directory-structure)

## What is Taipy Getting started

Taipy is a Python library for creating Business Applications. More information on our [website](https://www.taipy.io).

[Taipy Getting Started](https://docs.taipy.io/en/latest/getting_started/) provides a step-by-step opening to Taipy. 
Taipy features are leveraged as the application becomes more and more complex.

A more in depth documentation of Taipy can be found [here](https://docs.taipy.io/en/latest/).

## Installation

Want to install _Taipy Getting Started_? Check out our [`INSTALLATION.md`](INSTALLATION.md) file.

## Notebooks

To follow the **Getting Started** in a Notebook environment, you must generate the notebook document using the [`generate_notebook.py`](generate_notebook.py) script. Clone the repository and run the script (`python generate_notebook.py`). A Notebook called `getting_started.ipynb` will be created in your current folder.

## Contributing

Want to help build _Taipy Getting Started_? Check out our [`CONTRIBUTING.md`](CONTRIBUTING.md) file.

## Code of conduct

Want to be part of the _Taipy Getting Started_ community? Check out our [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) file.

## Directory Structure

- `src`: Common code shared by all the steps. For more information, on each step a README.md file is available in their
  respective folder (`step_xx/ReadMe.md`).
- `step_00`: The presentation of Taipy and the minimum code to run the gui.
- `step_01`: Presentation of the interactiveness of Taipy as well as different controls (slider and chart).
- `step_02`: Introduction to the on_change function with the choice of the week. The week displayed on the graph is 
  the week of the slider.
- `step_03`: Introduction to Taipy Core. Creation of the configuration for a baseline model.
- `step_04`: Add to the previous config, a pipeline config to create and execute the pipeline without the GUI.
- `step_05`: Add the execution of the pipeline thanks to a "Predict" button on the Gui (first button). The default 
  parameters are used to run the pipeline. The results are shown in a chart.
- `step_06`: Creation of a second pipeline (the machine learning pipeline : Auto-Regressive model). Creation and 
  execution of the scenario with the default parameters without the GUI.
- `step_07`: Scenario is being run at the beginning, and we can change the selected pipeline through a selector 
  (first selector) and a button.
- `step_08`: A first scenario is created. We can change the default parameters of this scenario with controls (date, 
  number, selector); the default parameters are the date, the number of predictions and max capacity. A 
  'change_scenario' button is pressed to apply these changes and re-submit the scenario.
- `step_09`: Now, we want to show how to create scenarios directly through the gui and keep track of them.
- `step_10`: Organize the page with a menu, layouts and parts that can be not rendered.
- `step_11`: Introduce the concepts of Cycles and primary scenarios. Deletion of a scenario and setting a scenario, 
  primary.
- `step_12`: Create a 'Performance' page that will compare all the primary scenarios and display metrics of these 
  scenarios.
- `CODE_OF_CONDUCT.md`: Code of conduct for members and contributors of _taipy-getting-started_.
- `CONTRIBUTING.md`: Instructions to contribute to _taipy-getting-started_.
- `index.md`: Landing page of the generated documentation. 
- `INSTALLATION.md`: Instructions to install _taipy-getting-started_.
- `LICENSE`: The Apache 2.0 License.
- `README.md`: Current file.
