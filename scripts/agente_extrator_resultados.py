import os
import sys
import urllib.request
import argparse
import subprocess
import socket

# Force Python socket resolver to use IPv4 only to avoid IPv6 connection hangs in sandboxed environments
orig_getaddrinfo = socket.getaddrinfo
def getaddrinfo_ipv4(host, port, family=0, type=0, proto=0, flags=0):
    return orig_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
socket.getaddrinfo = getaddrinfo_ipv4

# Define the target mapping of championships to their destination paths and download URLs
CHAMPIONSHIPS_REGISTRY = [
    # World Long Course (mundiais_longa)
    {
        "name": "World Championships Shanghai 2011 (LC)",
        "category": "mundiais_longa",
        "file_name": "mundial_longa2011.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010B0100FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "World Championships Barcelona 2013 (LC)",
        "category": "mundiais_longa",
        "file_name": "mundial_longa2013.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010D0200FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "World Championships Kazan 2015 (LC)",
        "category": "mundiais_longa",
        "file_name": "mundial_longa2015.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010F0200FFFFFFFFFFFFFFFFFFFF20"
    },
    # World Short Course (mundiais_curta)
    {
        "name": "World Championships Dubai 2010 (SC)",
        "category": "mundiais_curta",
        "file_name": "mundial_curta2010.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010A0A00FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "World Championships Istanbul 2012 (SC)",
        "category": "mundiais_curta",
        "file_name": "mundial_curta2012.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010C0100FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "World Championships Doha 2014 (SC)",
        "category": "mundiais_curta",
        "file_name": "mundial_curta2014.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010E010DFFFFFFFFFFFFFFFFFFFF20"
    },
    # European Long Course (continentais_longa)
    {
        "name": "European Championships Budapest 2020 (LC)",
        "category": "continentais_longa",
        "file_name": "europeu_longa2020.pdf",
        "url": "http://budapest2020.microplustiming.com/export/NU_Budapest2021/NU/pdf/Book.pdf"
    },
    # European Short Course (continentais_curta)
    {
        "name": "European Championships Eindhoven 2010 (SC)",
        "category": "continentais_curta",
        "file_name": "europeu_curta2010.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010A0100FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "European Championships Szczecin 2011 (SC)",
        "category": "continentais_curta",
        "file_name": "europeu_curta2011.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010B0300FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "European Championships Chartres 2012 (SC)",
        "category": "continentais_curta",
        "file_name": "europeu_curta2012.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010C0200FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "European Championships Herning 2013 (SC)",
        "category": "continentais_curta",
        "file_name": "europeu_curta2013.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010D0100FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "European Championships Netanya 2015 (SC)",
        "category": "continentais_curta",
        "file_name": "europeu_curta2015.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=00010F0100FFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "European Championships Copenhagen 2017 (SC)",
        "category": "continentais_curta",
        "file_name": "europeu_curta2017.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=000111010AFFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "European Championships Glasgow 2019 (SC)",
        "category": "continentais_curta",
        "file_name": "europeu_curta2019.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=000113010DFFFFFFFFFFFFFFFFFFFF20"
    },
    {
        "name": "European Championships Kazan 2021 (SC)",
        "category": "continentais_curta",
        "file_name": "europeu_curta2021.pdf",
        "url": "http://www.omegatiming.com/File/Download?id=0001150001FFFFFFFFFFFFFFFFFFFF20"
    }
]

# Root folder for PDFs
PDFS_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pdfs_omega"))

def print_banner():
    print("=" * 60)
    print("      AGENTE EXTRATOR DE RESULTADOS DE CAMPEONATOS (PDF)")
    print("              Foco: Temporada 2010 até 2026")
    print("=" * 60)

def verify_local_status():
    """
    Checks the local files in pdfs_omega and correlates them with our registry.
    Returns lists of (present_championships, missing_championships).
    """
    present = []
    missing = []
    
    for item in CHAMPIONSHIPS_REGISTRY:
        dest_path = os.path.join(PDFS_ROOT, item["category"], item["file_name"])
        if os.path.exists(dest_path):
            present.append((item, dest_path))
        else:
            missing.append((item, dest_path))
            
    return present, missing

def run_status_audit():
    present, missing = verify_local_status()
    
    print("\n--- STATUS LOCAL DOS CAMPEONATOS REGISTRADOS ---")
    print(f"Total Registrado: {len(CHAMPIONSHIPS_REGISTRY)}")
    print(f"Presentes Localmente: {len(present)}")
    print(f"Ausentes/Faltando: {len(missing)}")
    print("-" * 60)
    
    if present:
        print("\n[+] Campeonatos Já Disponíveis:")
        for item, path in present:
            size_kb = os.path.getsize(path) / 1024
            print(f"  - {item['name']} ({item['file_name']}) -> {size_kb:.1f} KB")
            
    if missing:
        print("\n[-] Campeonatos Faltando (Prontos para Download):")
        for item, path in missing:
            print(f"  - {item['name']} (Salvar em: pdfs_omega/{item['category']}/{item['file_name']})")
    else:
        print("\n[v] Todos os campeonatos registrados estão disponíveis localmente!")
        
    print("=" * 60)

import time

def download_file(url, dest_path, name):
    max_retries = 3
    retry_delay = 5.0
    
    print(f"Baixando: {name}...")
    print(f"  Origem: {url}")
    print(f"  Destino: {dest_path}")
    
    # Ensure destination folder exists
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Set headers to avoid bot blocks
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.0.0 Safari/537.36"
        }
    )
    
    for attempt in range(1, max_retries + 1):
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                with open(dest_path, "wb") as f:
                    f.write(response.read())
            size_mb = os.path.getsize(dest_path) / (1024 * 1024)
            print(f"  [Sucesso] Salvo com sucesso! ({size_mb:.2f} MB)")
            # Stage file immediately to ensure persistence in sandboxed environments
            try:
                subprocess.run(["git", "add", dest_path], check=True)
                print(f"  [Git] Staged {dest_path}")
            except Exception as git_err:
                print(f"  [Git Warning] Failed to stage {dest_path}: {git_err}")
            return True
        except Exception as e:
            print(f"  [Erro] Tentativa {attempt}/{max_retries} falhou: {e}")
            # Clean up partial download if it exists
            if os.path.exists(dest_path):
                os.remove(dest_path)
            if attempt < max_retries:
                print(f"  Aguardando {retry_delay} segundos antes de tentar novamente...")
                time.sleep(retry_delay)
                
    return False

def execute_downloads(indices=None):
    present, missing = verify_local_status()
    
    if not missing:
        print("\n[v] Nenhum campeonato faltando. Todos já estão baixados!")
        return
        
    if indices is not None:
        # Filter missing to only include those in indices list
        filtered_missing = []
        for item, dest_path in missing:
            # Find the index of item in CHAMPIONSHIPS_REGISTRY
            try:
                idx = CHAMPIONSHIPS_REGISTRY.index(item)
                if idx in indices:
                    filtered_missing.append((item, dest_path))
            except ValueError:
                pass
        missing = filtered_missing
        
    if not missing:
        print("\n[v] Nenhum dos campeonatos especificados está faltando!")
        return
        
    print(f"\nIniciando o download de {len(missing)} campeonatos...")
    success_count = 0
    
    for idx, (item, dest_path) in enumerate(missing):
        # Prevent rate limiting by sleeping between calls (except the first one)
        if idx > 0:
            print("  Aguardando 3 segundos para evitar bloqueio por limite de requisições...")
            time.sleep(3.0)
            
        if download_file(item["url"], dest_path, item["name"]):
            success_count += 1
            
    print(f"\nFinalizado! {success_count}/{len(missing)} downloads efetuados com sucesso.")
    print("=" * 60)

def trigger_etl():
    etl_script = os.path.join(os.path.dirname(__file__), "extrair_resultados_omega.py")
    if not os.path.exists(etl_script):
        print(f"[Erro] Script ETL principal '{etl_script}' não encontrado.")
        return
        
    print("\nExecutando extração de dados e atualização do dataset completo (ETL)...")
    try:
        # Run in scripts directory to match paths
        subprocess.run(
            [sys.executable, "extrair_resultados_omega.py"],
            cwd=os.path.dirname(__file__),
            check=True
        )
        print("[Sucesso] Pipeline ETL executado e concluído!")
    except Exception as e:
        print(f"[Erro] Falha ao executar o ETL principal: {e}")

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description="Agente Extrator de Resultados de Campeonatos de Natação (PDF)")
    parser.add_argument("--status", action="store_true", help="Audita o status local dos campeonatos.")
    parser.add_argument("--download", action="store_true", help="Efetua o download dos PDFs ausentes.")
    parser.add_argument("--indices", type=str, help="Lista de índices (separados por vírgula) para baixar.")
    parser.add_argument("--run-etl", action="store_true", help="Executa o processamento ETL das novas parciais.")
    
    args = parser.parse_args()
    
    # Default behavior: if no arguments are provided, perform interactive audit
    if not any([args.status, args.download, args.indices, getattr(args, 'run_etl', False)]):
        run_status_audit()
        present, missing = verify_local_status()
        if missing:
            ans = input("\nDeseja baixar todos os campeonatos ausentes agora? (s/n): ").strip().lower()
            if ans == 's':
                execute_downloads()
                ans_etl = input("\nDeseja executar o script de processamento ETL agora? (s/n): ").strip().lower()
                if ans_etl == 's':
                    trigger_etl()
        return
        
    if args.status:
        run_status_audit()
        
    if args.indices:
        indices = [int(x) for x in args.indices.split(",")]
        execute_downloads(indices=indices)
    elif args.download:
        execute_downloads()
        
    if getattr(args, 'run_etl', False):
        trigger_etl()

if __name__ == "__main__":
    main()
