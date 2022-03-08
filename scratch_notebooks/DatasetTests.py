# %%
from analysis_schema.base_model import show_plots
from analysis_schema.run_analysis import load_and_run
from analysis_schema.schema_model import ytModel
from analysis_schema.save_schema_file import save_schema

# %%

load_and_run(json_file="../analysis_schema/pydantic_schema_example.json",
files="Jupter")

# %%

save_schema()
# %%
