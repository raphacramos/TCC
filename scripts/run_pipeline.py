import os
import sys
import subprocess
import time

def run_command(cmd, cwd=None):
    print(f"\n>>> Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"Error: Command failed with code {result.returncode}")
        return False
    return True

def main():
    scripts_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(scripts_dir, "..", ".venv", "bin", "python")
    
    # 1. Download all missing PDFs
    print("=== STEP 1: DOWNLOADING MISSING PDFs ===")
    if not run_command([venv_python, "agente_extrator_resultados.py", "--download"], cwd=scripts_dir):
        sys.exit(1)
        
    # 2. Stage downloaded PDFs in git to ensure they are mirrored back to the host workspace
    print("\n=== STEP 2: STAGING PDFs IN GIT ===")
    if not run_command(["git", "add", "../pdfs_omega/"], cwd=scripts_dir):
        print("Warning: Failed to stage PDFs in git, proceeding anyway.")
        
    # 3. Run the ETL script to parse PDFs and update dataset_pacing_completo.csv
    print("\n=== STEP 3: RUNNING ETL PARSER ===")
    if not run_command([venv_python, "extrair_resultados_omega.py"], cwd=scripts_dir):
        sys.exit(1)
        
    # 4. Stage the updated CSV dataset and EDA plot in git
    print("\n=== STEP 4: STAGING DATASET CSV AND PLOT IN GIT ===")
    if not run_command(["git", "add", "dataset_pacing_completo.csv", "eda_pacing_completo.png"], cwd=scripts_dir):
        print("Warning: Failed to stage CSV and plot in git.")
        
    # 5. Run the auditor script to print the final status
    print("\n=== STEP 5: RUNNING AUDITOR ===")
    run_command([venv_python, "auditoria_campeonatos.py"], cwd=scripts_dir)
    
    print("\n=== PIPELINE COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    main()
