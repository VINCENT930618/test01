import json

INPUT_FILE = "orders.json"
OUTPUT_FILE = "output_orders.json"

def load_data(filename: str) -> list:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_orders(filename: str, orders: list) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(orders, file, indent=4, ensure_ascii=False)

def calculate_order_total(order: dict) -> int:
    return sum(item["price"] * item["quantity"] for item in order["items"])

def add_order(orders: list) -> str:
    order_id = input("請輸入訂單編號：").upper()
    if any(order["order_id"] == order_id for order in orders):
        return f"=> 錯誤：訂單編號 {order_id} 已存在！"

    customer = input("請輸入顧客姓名：")
    items = []

    while True:
        name = input("請輸入訂單項目名稱（輸入空白結束）：")
        if not name:
            break

        while True:
            try:
                price = int(input("請輸入價格："))
                if price < 0:
                    print("=> 錯誤：價格不能為負數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        while True:
            try:
                quantity = int(input("請輸入數量："))
                if quantity <= 0:
                    print("=> 錯誤：數量必須為正整數，請重新輸入")
                    continue
                break
            except ValueError:
                print("=> 錯誤：價格或數量必須為整數，請重新輸入")

        items.append({"name": name, "price": price, "quantity": quantity})

    if not items:
        return "=> 至少需要一個訂單項目"

    orders.append({
        "order_id": order_id,
        "customer": customer,
        "items": items
    })
    return f"=> 訂單 {order_id} 已新增！"

def print_order_report(data: list, title: str = "訂單報表", single: bool = False) -> None:
    print(f"\n{'='*20} {title} {'='*20}")
    for idx, order in enumerate(data, 1):
        if not single:
            print(f"訂單 #{idx}")
        print(f"訂單編號: {order['order_id']}")
        print(f"客戶姓名: {order['customer']}")
        print("-" * 50)
        print("商品名稱\t單價\t數量\t小計")
        print("-" * 50)
        total = 0
        for item in order["items"]:
            subtotal = item["price"] * item["quantity"]
            total += subtotal
            print(f"{item['name']}\t{item['price']}\t{item['quantity']}\t{subtotal}")
        print("-" * 50)
        print(f"訂單總額: {total}")
        print("=" * 50)

def process_order(orders: list) -> tuple:
    if not orders:
        return ("=> 沒有待處理訂單！", None)

    print("\n======== 待處理訂單列表 ========")
    for i, order in enumerate(orders, 1):
        print(f"{i}. 訂單編號: {order['order_id']} - 客戶: {order['customer']}")
    print("=" * 32)

    while True:
        choice = input("請選擇要出餐的訂單編號 (輸入數字或按 Enter 取消): ")
        if choice == "":
            return ("=> 已取消出餐操作。", None)
        if not choice.isdigit():
            print("=> 錯誤：請輸入有效的數字")
            continue
        index = int(choice)
        if 1 <= index <= len(orders):
            order = orders.pop(index - 1)
            return (f"=> 訂單 {order['order_id']} 已出餐完成", order)
        else:
            print("=> 錯誤：請輸入有效的數字")

def main() -> None:
    while True:
        print("***************選單***************")
        print("1. 新增訂單")
        print("2. 顯示訂單報表")
        print("3. 出餐處理")
        print("4. 離開")
        print("**********************************")
        choice = input("請選擇操作項目(Enter 離開)：").strip()
        if choice == "":
            break

        orders = load_data(INPUT_FILE)
        output_orders = load_data(OUTPUT_FILE)

        if choice == "1":
            msg = add_order(orders)
            print(msg)
            if "已新增" in msg:
                save_orders(INPUT_FILE, orders)

        elif choice == "2":
            if orders:
                print_order_report(orders)
            else:
                print("=> 沒有任何訂單可顯示！")

        elif choice == "3":
            msg, processed = process_order(orders)
            print(msg)
            if processed:
                output_orders.append(processed)
                save_orders(INPUT_FILE, orders)
                save_orders(OUTPUT_FILE, output_orders)
                print_order_report([processed], title="出餐訂單", single=True)

        elif choice == "4":
            break
        else:
            print("=> 請輸入有效的選項（1-4）")

if __name__ == "__main__":
    main()
