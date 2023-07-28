"""
A multi-page Taipy application, which includes 3 pages:
- A rootpage which is shared by other pages.
- Two pages named page_1 and page_2.

Please refer to https://docs.taipy.io/en/latest/manuals/gui/pages for more details.
"""

from pages import data_viz, scenario_page, performance
from pages.root import *

from config.config import *

from taipy.gui import Gui
import taipy as tp


def on_change(state, var_name: str, var_value):
    state['scenario'].on_change(state, var_name, var_value)


pages = {
    "/": root_page,
    "data_viz": data_viz,
    "scenario": scenario_page,
    "performance": performance
}


if __name__ == "__main__":
    tp.Core().run()
    gui = Gui(pages=pages)
    gui.run(title="Taipy Application")
