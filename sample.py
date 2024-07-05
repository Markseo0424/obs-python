import subprocess
import time

# Path to the After Effects executable
after_effects_path = r"C:\Program Files\Adobe\Adobe After Effects 2024\Support Files\AfterFX.exe"

# Path to the ExtendScript file
script_path = r"C:\Users\marks\Documents\PyCharm\aePython\sample.jsx"

# Path to the After Effects project file
project_path = r"C:\Users\marks\Documents\PyCharm\aePython\sample.aep"

# Command to open the After Effects project
open_project_command = [after_effects_path, "-project", project_path]

# Open the project
subprocess.Popen(open_project_command)

time.sleep(10)

# Command to run the script
run_script_command = [after_effects_path, "-r", script_path]

# Execute the script
subprocess.run(run_script_command)
