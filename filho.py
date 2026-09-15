"""Processo independente iniciado pelo OS Explorer."""

import os
import time


def main():
    print("\n[PROCESSO FILHO]", flush=True)
    print("Processo iniciado.", flush=True)
    print(f"PID: {os.getpid()}", flush=True)
    print("Executando durante 2 segundos...", flush=True)
    time.sleep(2)
    print("Finalizando...", flush=True)


if __name__ == "__main__":
    main()
