import os
import shutil
import glob
import PyInstaller.__main__

def translate_lsl_to_python(lev_content):
    # Translates LSL syntax to Python syntax
    python_lines = []
    for line in lev_content.splitlines():
        if line.startswith("say"):
            # Extract the message after 'say'
            message = line[len("say"):].strip()

            # Add quotes around the message if not already present
            if not (message.startswith('"') and message.endswith('"')):
                message = f'"{message}"'

            python_lines.append(f'print({message})')
        elif line == "clear":
            # Add a clear screen command in Python
            python_lines.append('import os; os.system("cls" if os.name == "nt" else "clear")')
        # Add more translations if necessary
    
    # Add a final line to wait for user input
    python_lines.append('input("Press Enter to exit...")')
    
    return "\n".join(python_lines)

def display_menu():
    print("===================================================")
    print(" Officerdown IDE and Compiler for LSL Scripts v1.0 ")
    print("===================================================")
    print("1. Create New LSL Script")
    print("2. Compile LSL Script to Executable")
    print("3. Cleanup Build Files")
    print("4. Exit")
    print("===================================================")

def create_script():
    filename = input("Enter the filename to save (without extension): ") + ".lev"
    
    print("\nEnter your LSL script (end input with 'EOF' on a new line):")
    script_content = []
    while True:
        line = input()
        if line == "EOF":
            break
        script_content.append(line)
    
    # Write to file
    with open(filename, 'w') as f:
        f.write("\n".join(script_content))
    
    print(f"\nScript saved as {filename}\n")

def compile_script():
    lev_file = input("Enter the LSL script filename to compile (with .lev extension): ")
    if not os.path.exists(lev_file):
        print(f"Error: File '{lev_file}' not found.")
        return

    with open(lev_file, 'r') as f:
        lev_content = f.read()

    # Translate LSL content to Python
    python_content = translate_lsl_to_python(lev_content)

    # Save translated Python content
    python_file = os.path.splitext(lev_file)[0] + ".py"
    with open(python_file, 'w') as f:
        f.write(python_content)
    
    # Only Windows compilation
    output_file = os.path.splitext(lev_file)[0]
    
    PyInstaller.__main__.run([
        '--onefile',
        '--name=%s' % output_file,  # No --windowed option here
        python_file
    ])
    print(f"Windows executable created: {output_file}.exe\n")



def cleanup():
    # Cleanup the build and .spec files
    try:
        shutil.rmtree('build')  # Remove the build directory
        # Remove all .spec files
        for spec_file in glob.glob('*.spec'):
            os.remove(spec_file)
        print("Cleanup completed. Removed build directory and .spec files.")
    except Exception as e:
        print(f"Cleanup failed: {e}")

def main():
    while True:
        display_menu()
        choice = input("Select an option (1-4): ")
        
        if choice == "1":
            create_script()
        elif choice == "2":
            compile_script()
        elif choice == "3":
            cleanup()
        elif choice == "4":
            print("Thank you for using Officerdown IDE and Compiler for LSL v1.0.")
            break
        else:
            print("Invalid selection. Please choose 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()

