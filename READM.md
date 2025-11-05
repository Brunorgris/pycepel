# pycepel.py

This library provides a set of tools for working with CEPEL (Centro de Pesquisas de Energia Elétrica) files, specifically the `.pwf` format used in power flow studies. It allows for extracting data from different sections of the file, converting them into pandas DataFrames, and updating values programmatically.

## `FuncsCepel` Class

This class provides methods for parsing and manipulating data from CEPEL files.

### `__init__(self, type_cepel='DBAR')`

Initializes the `FuncsCepel` class.

- **`type_cepel` (str):** The default type of the file section to be processed (e.g., 'DBAR', 'DLIN').

### `extrair_secao(self, type_cepel=None, text=None)`

Extracts a section from the CEPEL file content.

- **`type_cepel` (str):** The type of section to extract.
- **`text` (str):** The text content of the file.
- **Returns:** The extracted section as a string.

### `dict_to_df(self, type_cepel=None)`

Converts a section of the CEPEL file into a pandas DataFrame.

- **`type_cepel` (str):** The type of section to convert.
- **Returns:** A pandas DataFrame containing the data from the specified section.

### `get_df_dbar(self, report_path)`

Converts the DBAR section of a PWF file to a DataFrame.

- **`report_path` (str):** The path to the `.pwf` file.
- **Returns:** A pandas DataFrame with the DBAR section data.

### `get_df_dcer(self, report_path)`

Converts the DCER section of a PWF file to a DataFrame.

- **`report_path` (str):** The path to the `.pwf` file.
- **Returns:** A pandas DataFrame with the DCER section data.

### `get_df_by_key(self, report_path, type_cepel=None)`

Converts a section of a PWF file to a DataFrame based on the provided key.

- **`report_path` (str):** The path to the `.pwf` file.
- **`type_cepel` (str):** The key of the section to be converted.
- **Returns:** A pandas DataFrame with the section data.

### `ajusta_float_string(self, value_key, valor, largura_valor)`

Adjusts the string formatting of a float value.

- **`value_key` (str):** The key of the value to be adjusted.
- **`valor` (float):** The float value.
- **`largura_valor` (int):** The width of the value.
- **Returns:** The formatted value as a string.

### `atualizar_valores_dbar(self, value_key, str_dbar, novos_valores, operacao=True)`

Updates values in the DBAR section of the file.

- **`value_key` (str):** The key of the value to be updated (e.g., "Pg", "Qg").
- **`str_dbar` (str):** The content of the DBAR section.
- **`novos_valores` (pd.DataFrame):** A DataFrame with the new values.
- **`operacao` (bool):** A flag to determine the operation type.
- **Returns:** The updated DBAR section as a string.

### `get_value_length(self, type_cepel=None)`

Gets the length of a value in a specific section.

- **`type_cepel` (str):** The type of the section.
- **Returns:** A dictionary with the value lengths.

### `initializing_str(self, df, type_cepel=None)`

Initializes a string for a specific section.

- **`df` (pd.DataFrame):** The DataFrame to be converted.
- **`type_cepel` (str):** The type of the section.
- **Returns:** The initialized string.

### `generate_string(self, df, type_cepel=None)`

Generates a string in the CEPEL format from a DataFrame.

- **`df` (pd.DataFrame):** The DataFrame to be converted.
- **`type_cepel` (str):** The type of the section.
- **Returns:** The generated string.

### `condicionar_pg(self, caminho_arquivo, bus_to_query, interc_new, ug_data)`

Adjusts the 'Pg' values based on participation factors.

- **`caminho_arquivo` (str):** The path to the file.
- **`bus_to_query` (list):** A list of bus IDs to be queried.
- **`interc_new` (float):** The new interchange value.
- **`ug_data` (pd.DataFrame):** A DataFrame with the generation unit data.
- **Returns:** An adjusted DataFrame with the new 'Pg' values.

## `TemplateCepel` Class

This class is used to create template files for controlling the execution of ANAREDE.

### `__init__(self, file_path, save_name=None, rest_save_case=True, case_number=None, save_name_to_save=None, case_number_to_save=None, content_flag=True, content_text="", save_pwf_report=False, name_pwf_report=None, close_anarede=True, save_cartao_pwf=True, name_cartao_pwf=None)`

Initializes the `TemplateCepel` class.

- **`file_path` (str):** The path to the file.
- **`save_name` (str):** The name of the save file.
- **`rest_save_case` (bool):** A flag to restore a saved case.
- **`case_number` (int):** The case number.
- **`save_name_to_save` (str):** The name to save the case as.
- **`case_number_to_save` (int):** The case number to save.
- **`content_flag` (bool):** A flag to include additional content.
- **`content_text` (str):** The additional content to include.
- **`save_pwf_report` (bool):** A flag to save a PWF report.
- **`name_pwf_report` (str):** The name of the PWF report.
- **`close_anarede` (bool):** A flag to close ANAREDE after execution.
- **`save_cartao_pwf` (bool):** A flag to save the PWF card.
- **`name_cartao_pwf` (str):** The name of the PWF card.

### `create_template(self)`

Creates the template for controlling ANAREDE.

- **Returns:** A dictionary containing the template if `save_cartao_pwf` is `True`, otherwise returns the template as a string.

## `run_anarede` Function

This function executes the ANAREDE simulation tool.

### `run_anarede(ANAREDE, PWD, fileNAME)`

- **`ANAREDE` (str):** The path to the ANAREDE executable.
- **`PWD` (str):** The path to the working directory.
- **`fileNAME` (str):** The name of the `.pwf` file to be executed.

## Usage Example

```python
import os
from pycepel import FuncsCepel, TemplateCepel, run_anarede

# Initialize FuncsCepel
cepel_funcs = FuncsCepel()

# Get the DBAR DataFrame from a .pwf file
df_dbar = cepel_funcs.get_df_dbar('path/to/your/file.pwf')

# Create a template for ANAREDE
content_text = (
    'DBAR\n'
    '    12L1 GERRO---IPU50 G           0.   0.-999999999                     10010000\n'
    '430002L2 NAYO B1   500 N1050  0.   0.   0.-999999999                     10310260\n'
    '99999\n'
    'EXLF NEWT CREM CTAP VLIM STEP RMON MFCT RCVG\n')

file_path = (os.getcwd() + '\\').replace("\\", "/")
save_name = "ajusta_caso"
case_number = 1
save_name_to_save = "ajusta_caso_exe"
case_number_to_save = 98
name_pwf_report = "resultado"

template_cepel = TemplateCepel(
    file_path=file_path,
    save_name=save_name,
    case_number=case_number_to_save,
    save_name_to_save=save_name_to_save,
    case_number_to_save=case_number_to_save,
    content_text=content_text,
    save_pwf_report=True,
    name_pwf_report=name_pwf_report,
    close_anarede=True,
    save_cartao_pwf=True,
    name_cartao_pwf='exemplo'
)

template = template_cepel.create_template()

# Run ANAREDE
# run_anarede('path/to/anarede.exe', 'path/to/working/dir', 'exemplo.pwf')
```
