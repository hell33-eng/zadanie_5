import tkinter as tk
from tkinter import ttk
import requests
import json

def exchange():
    base = base_currency.get().lower()
    second_base = second_base_currency.get().lower()
    target = target_currency.get().lower()

    # Проверка: все ли поля заполнены
    if not base or not second_base or not target:
        result_label.config(text="Выберите все валюты в выпадающих списках.")
        return

    # Запрет одинаковых валют
    if base == target or second_base == target:
        result_label.config(text="Базовая и целевая валюты не должны совпадать.")
        return

    coin_id = "bitcoin"
    currencies_string = ",".join([base, second_base, target])

    params = {
        "ids": coin_id,
        "vs_currencies": currencies_string
    }
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://api.coingecko.com/api/v3/simple/price"

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        coin_data = data[coin_id]

        output_data = {
            "coin": coin_id,
            "base": base.upper(),
            "second_base": second_base.upper(),
            "target": target.upper(),
            "rates": {}
        }

        rate_base = coin_data.get(base)
        rate_second = coin_data.get(second_base)
        rate_target = coin_data.get(target)

        lines = []

        if rate_base and rate_target:
            cross_rate_1 = rate_target / rate_base
            output_data["rates"][f"{base.upper()}_to_{target.upper()}"] = cross_rate_1
            lines.append(f"{base.upper()} → {target.upper()}: {cross_rate_1:.4f}")
        else:
            lines.append(f"Не удалось получить курс {base.upper()} → {target.upper()}")

        if rate_second and rate_target:
            cross_rate_2 = rate_target / rate_second
            output_data["rates"][f"{second_base.upper()}_to_{target.upper()}"] = cross_rate_2
            lines.append(f"{second_base.upper()} → {target.upper()}: {cross_rate_2:.4f}")
        else:
            lines.append(f"Не удалось получить курс {second_base.upper()} → {target.upper()}")

        # Вывод JSON в консоль — требование задания
        print(json.dumps(output_data, ensure_ascii=False, indent=2))

        result_text = "\n".join(lines)
        result_label.config(text=result_text)

    except requests.exceptions.RequestException as e:
        result_label.config(text=f"Ошибка сети или API: {e}")
    except KeyError as e:
        result_label.config(text=f"Ошибка данных: {e}. Возможно, CoinGecko не знает такую валюту.")
    except Exception as e:
        result_label.config(text=f"Неожиданная ошибка: {e}")

# Интерфейс (без изменений по сравнению с коммитом 2)
root = tk.Tk()
root.title("Курсы валют (CoinGecko)")
root.geometry("420x380")

ttk.Label(root, text="Базовая валюта").pack(pady=5)
base_currency = ttk.Combobox(root, values=["eur", "usd", "gbp", "jpy"], state="readonly")
base_currency.set("eur")
base_currency.pack(pady=5)

ttk.Label(root, text="Вторая базовая валюта").pack(pady=5)
second_base_currency = ttk.Combobox(root, values=["eur", "usd", "gbp", "jpy"], state="readonly")
second_base_currency.set("usd")
second_base_currency.pack(pady=5)

ttk.Label(root, text="Целевая валюта").pack(pady=5)
target_currency = ttk.Combobox(root, values=["rub", "eur", "usd", "gbp", "jpy"], state="readonly")
target_currency.set("rub")
target_currency.pack(pady=5)

btn = ttk.Button(root, text="Получить курс обмена", command=exchange)
btn.pack(pady=20)

result_label = ttk.Label(root, text="", wraplength=380, justify="center", foreground="blue")
result_label.pack(pady=10)

root.mainloop()