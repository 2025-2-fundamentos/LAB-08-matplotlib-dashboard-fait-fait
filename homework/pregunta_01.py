# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""

import os
from typing import Optional, Dict

import pandas as pd
import matplotlib.pyplot as plt


def _find_input_file() -> Optional[str]:
    """
    Buscar el archivo shipping-data.csv en rutas comunes usadas en ejercicios.
    Devuelve la ruta encontrada o None si no existe en ninguna.
    """
    candidates = [
        os.path.join("data", "shipping-data.csv"),
        os.path.join("data", "shipping-data.csv").replace("/", os.sep),
        os.path.join("files", "input", "shipping-data.csv"),
        os.path.join("files", "input", "shipping-data.csv").replace("/", os.sep),
        "shipping-data.csv",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def _save_bar(series: pd.Series, outpath: str, title: str, xlabel: str = "", ylabel: str = "Count") -> None:
    plt.figure(figsize=(6, 4.5))
    ax = series.plot(kind="bar")
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def _save_hist(data: pd.Series, outpath: str, title: str, bins: int = 25, xlabel: str = "", ylabel: str = "Frequency") -> None:
    plt.figure(figsize=(6, 4.5))
    ax = plt.gca()
    ax.hist(data.dropna(), bins=bins)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def _save_rating_plot(df: pd.DataFrame, outpath: str) -> None:
    """
    Genera un gráfico de promedio de Customer_rating por Warehouse_block.
    Si no hay Warehouse_block, se genera la distribución de rating.
    """
    plt.figure(figsize=(6, 4.5))
    ax = plt.gca()
    if "Warehouse_block" in df.columns and df["Warehouse_block"].notna().any():
        tmp = df[["Warehouse_block", "Customer_rating"]].dropna()
        if not tmp.empty:
            avg = tmp.groupby("Warehouse_block")["Customer_rating"].mean().sort_values(ascending=False)
            avg.plot(kind="bar", ax=ax)
            ax.set_ylabel("Average rating")
            ax.set_xlabel("")
            ax.set_title("Average customer rating by warehouse")
        else:
            df["Customer_rating"].dropna().value_counts().sort_index().plot(kind="bar", ax=ax)
            ax.set_title("Customer rating (distribution)")
            ax.set_xlabel("Rating")
            ax.set_ylabel("Count")
    else:
        df["Customer_rating"].dropna().value_counts().sort_index().plot(kind="bar", ax=ax)
        ax.set_title("Customer rating (distribution)")
        ax.set_xlabel("Rating")
        ax.set_ylabel("Count")

    ax.grid(axis="y", linestyle=":", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(outpath, dpi=150)
    plt.close()


def pregunta_01() -> Dict[str, str]:
    """
    Lee data/shipping-data.csv (busca en varias rutas si es necesario), crea la carpeta docs
    y genera cuatro gráficos en archivos separados y un index.html que los incrusta.

    Archivos generados en docs/:
      - shipping_per_warehouse.png
      - mode_of_shipment.png
      - average_customer_rating.png
      - weight_distribution.png
      - index.html

    Devuelve un dict con las rutas generadas (útil para debugging/tests manuales).
    """
    input_file = _find_input_file()
    if input_file is None:
       raise FileNotFoundError("No se encontró 'shipping-data.csv' en rutas esperadas. Buscadas: data/, files/input/, pwd.")

    out_dir = "docs"
    os.makedirs(out_dir, exist_ok=True)

    df = pd.read_csv(input_file)
    df.columns = [c.strip() for c in df.columns]
    if "Customer_rating" in df.columns:
        df["Customer_rating"] = pd.to_numeric(df["Customer_rating"], errors="coerce")
    if "Weight_in_gms" in df.columns:
        df["Weight_in_gms"] = pd.to_numeric(df["Weight_in_gms"], errors="coerce")

    shipping_per_warehouse_path = os.path.join(out_dir, "shipping_per_warehouse.png")
    if "Warehouse_block" in df.columns:
        wb_counts = df["Warehouse_block"].dropna().astype(str).str.strip().value_counts()
        if wb_counts.empty:
            plt.figure(figsize=(6, 4.5))
            plt.text(0.5, 0.5, "No data for Warehouse_block", ha="center", va="center")
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(shipping_per_warehouse_path, dpi=150)
            plt.close()
        else:
            _save_bar(wb_counts, shipping_per_warehouse_path, "Shipping per warehouse", xlabel="")
    else:
        plt.figure(figsize=(6, 4.5))
        plt.text(0.5, 0.5, "Column Warehouse_block not found", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(shipping_per_warehouse_path, dpi=150)
        plt.close()

    mode_of_shipment_path = os.path.join(out_dir, "mode_of_shipment.png")
    if "Mode_of_Shipment" in df.columns:
        mode_counts = df["Mode_of_Shipment"].dropna().astype(str).str.strip().value_counts()
        if mode_counts.empty:
            plt.figure(figsize=(6, 4.5))
            plt.text(0.5, 0.5, "No data for Mode_of_Shipment", ha="center", va="center")
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(mode_of_shipment_path, dpi=150)
            plt.close()
        else:
            _save_bar(mode_counts, mode_of_shipment_path, "Mode of shipment (counts)", xlabel="")
    else:
        plt.figure(figsize=(6, 4.5))
        plt.text(0.5, 0.5, "Column Mode_of_Shipment not found", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(mode_of_shipment_path, dpi=150)
        plt.close()

    average_customer_rating_path = os.path.join(out_dir, "average_customer_rating.png")
    if "Customer_rating" in df.columns:
        _save_rating_plot(df, average_customer_rating_path)
    else:
        plt.figure(figsize=(6, 4.5))
        plt.text(0.5, 0.5, "Column Customer_rating not found", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(average_customer_rating_path, dpi=150)
        plt.close()

    weight_distribution_path = os.path.join(out_dir, "weight_distribution.png")
    if "Weight_in_gms" in df.columns:
        w_series = df["Weight_in_gms"].dropna()
        if w_series.empty:
            plt.figure(figsize=(6, 4.5))
            plt.text(0.5, 0.5, "No data for Weight_in_gms", ha="center", va="center")
            plt.axis("off")
            plt.tight_layout()
            plt.savefig(weight_distribution_path, dpi=150)
            plt.close()
        else:
            _save_hist(w_series, weight_distribution_path, "Weight distribution (gms)", bins=30, xlabel="Weight (gms)")
    else:
        plt.figure(figsize=(6, 4.5))
        plt.text(0.5, 0.5, "Column Weight_in_gms not found", ha="center", va="center")
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(weight_distribution_path, dpi=150)
        plt.close()

    html_path = os.path.join(out_dir, "index.html")
    html_content = f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Shipping Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body {{ font-family: Arial, Helvetica, sans-serif; margin: 20px; background: #f7f7f7; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; max-width: 1100px; margin: 0 auto; }}
    .card {{ background: white; padding: 12px; border-radius: 6px; box-shadow: 0 1px 6px rgba(0,0,0,0.06); }}
    img {{ max-width: 100%; height: auto; display: block; margin: 0 auto; }}
    h1 {{ text-align: center; font-size: 20px; }}
  </style>
</head>
<body>
  <h1>Shipping Dashboard</h1>
  <div class="grid">
    <div class="card"><h3>Shipping per warehouse</h3><img src="shipping_per_warehouse.png" alt="shipping per warehouse"></div>
    <div class="card"><h3>Mode of shipment</h3><img src="mode_of_shipment.png" alt="mode of shipment"></div>
    <div class="card"><h3>Average customer rating</h3><img src="average_customer_rating.png" alt="average customer rating"></div>
    <div class="card"><h3>Weight distribution</h3><img src="weight_distribution.png" alt="weight distribution"></div>
  </div>
  <footer style="text-align:center; margin-top:14px; color:#666;">Generado por pregunta_01()</footer>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as fh:
        fh.write(html_content)

    # Devolver rutas para debugging/test
    return {
        "shipping_per_warehouse": shipping_per_warehouse_path,
        "mode_of_shipment": mode_of_shipment_path,
        "average_customer_rating": average_customer_rating_path,
        "weight_distribution": weight_distribution_path,
        "index_html": html_path,
    }


if __name__ == "__main__":
    print(pregunta_01())
