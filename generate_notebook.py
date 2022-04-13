
import json

def add_line(source, line, step):
    on_change_needed = ['step_02', 'step_09', 'step_11']
    
    line = line.replace('Getting Started with Taipy', 'Getting Started with Taipy on Notebooks')
    line = line.replace('(../src/', '(https://docs.taipy.io/getting_started/src/')
    line = line.replace('(dataset.csv)', '(https://docs.taipy.io/getting_started/step_01/dataset.csv)')

    if line.startswith('!['):
        if step != 'index':
            line = line.replace('(', '(https://docs.taipy.io/getting_started/' + step + '/')
        else:
            line = line.replace('(', '(https://docs.taipy.io/getting_started/')
        
        # conversion of Markdown image to HTML
        img_src = line.split('](')[1].split(')')[0]
        width = line.split('](')[1].split(')')[1].split(' ')[1]
        
        source.append('<div align="center">\n')        
        source.append(f' <img src={img_src} {width}>\n')
        source.append('</div>\n')
    
    elif step == 'step_00' and line.startswith('Gui(page='):
        
        source.append('\n')
        source.append('# We can use Gui("# Getting Started with Taipy").run() directly\n')
        source.append('# However, we need a Markdown and Gui object to modify the content of the page\n')
        source.append('# in the Notebook\n')
        source.append('\n')
        source.append('main_page = Markdown("# Getting Started with Taipy")\n')
        source.append('gui = Gui(main_page)\n')
        source.append('gui.run(dark_mode=False)\n')    
      
    elif line.startswith('Gui(page=') and step != 'step_00':
        search_for_md = line.split(')')
        name_of_md = search_for_md[0][9:]
        
        source.append('gui.stop()\n')
        if step in on_change_needed:
            source.append('gui.on_change = on_change\n')
        source.append(f'main_page.set_content({name_of_md})\n')
        source.append('gui.run()\n')
        
    elif step == 'step_00' and line.startswith('from taipy'):
       source.append("from taipy.gui import Gui, Markdown\n")
    elif 'Notebook' in line and 'step' in step:
        pass
    else:
        source.append(line+'\n')
     
    return source
        


def detect_new_cell(notebook, source, cell, line, execution_count, force_creation=False):
    if line.startswith('```python') or line.startswith('```') and cell == 'code' or force_creation:
        source = source[:-1]
        
        if cell == 'code':
            notebook['cells'].append({
                "cell_type": "code",
                "metadata": {},
                "outputs": [],
                "execution_count": execution_count,
                "source": source
            })
            cell = 'markdown'
            execution_count += 1
        else:
            notebook['cells'].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": source
            })
            cell = 'code'

        source = []

    
    
    return cell, source, notebook, execution_count


def create_introduction(notebook, execution_count):
    with open('index.md', 'r') as f:
        text = f.read()

    splitted_text = text.split('\n')
    cell = "markdown"
    source = []

    for line in splitted_text:
        if not line.startswith('``` console'):
            add_line(source, line, 'index')
        else:
            break
    
    notebook['cells'].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": source
            })  
        
    notebook['cells'].append({
                "cell_type": "code",
                "metadata": {},
                "outputs": [],
                "execution_count": execution_count,
                "source": ['# !pip install taipy\n',
                           '# !pip install scikit-learn\n',
                           '# !pip install statsmodels']
            })
    
    notebook['cells'].append({
                "cell_type": "markdown",
                "metadata": {},
                "source": ['## Using Notebooks\n',
                           'Some functions will be used in the Getting Started for Notebooks that are primarly used for Notebooks (`gui.stop()`, `gui.run()`, `gui.on_change`, `set_content()`)\n',
                           'To have more explanation on these different functions, you can find the documentation related [here](https://docs.taipy.io/manuals/gui/notebooks/)\n',
                           '**Warning**: Do not forget to stop your server when you are finished. You can do so by stopping or restarting your kernel.\n']
            })
    
    execution_count += 1
    return notebook, execution_count



def create_steps(notebook, execution_count):
    steps = ['step_0' + str(i) for i in range(0, 10)] + ['step_10', 'step_11', 'step_12']
    source = []

    for step in steps:
        if source != []:
            cell, source, notebook, execution_count = detect_new_cell(notebook,
                                                                      source,
                                                                      cell,
                                                                      line,
                                                                      execution_count,
                                                                      force_creation=True)
        
        with open(step + '/ReadMe.md', 'r') as f:
            text = f.read()

        splitted_text = text.split('\n')
        cell = "markdown"
        

        for line in splitted_text:
            add_line(source, line, step)
            cell, source, notebook, execution_count = detect_new_cell(notebook, source, cell, line, execution_count)
            
    return notebook, execution_count


if __name__ == '__main__':
    

    notebook = {
        "cells":[ ],
        "metadata": {
         "language_info": {
          "codemirror_mode": {
           "name": "ipython",
           "version": 3
          },
          "file_extension": ".py",
          "mimetype": "text/x-python",
          "name": "python",
          "nbconvert_exporter": "python",
          "pygments_lexer": "ipython3"
         },
         "orig_nbformat": 4
        },
        "nbformat": 4,
        "nbformat_minor": 2 
    }
    
    execution_count = 0
    
    notebook, execution_count = create_introduction(notebook, execution_count)
    notebook, execution_count = create_steps(notebook, execution_count)
    
    with open('getting_started.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)