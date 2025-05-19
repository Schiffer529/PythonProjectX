from datetime import datetime

# 商品类
class Product:
    def __init__(self, barcode, name, price, stock):
        self.barcode = barcode
        self.name = name
        self.price = price
        self.stock = stock

# 购物车条目类
class CartItem:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

# 购物车类
class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, product, quantity):
        if product.stock >= quantity:
            self.items.append(CartItem(product, quantity))
            product.stock -= quantity
        else:
            print(f"❗库存不足：{product.name} 仅剩 {product.stock} 件")

    def total_amount(self):
        return sum(item.product.price * item.quantity for item in self.items)

# 支付处理器类
class PaymentProcessor:
    def process_payment(self, amount, method='cash'):
        print(f"\n正在处理支付：方式={method}, 金额=¥{amount:.2f}")
        if method == 'cash':
            print(f"✅ 现金支付成功：¥{amount:.2f}")
            return True
        elif method == 'qr':
            print(f"📱 扫码支付成功：¥{amount:.2f}")
            return True
        else:
            print("❌ 不支持的支付方式")
            return False

# 小票打印类
class ReceiptPrinter:
    def print_receipt(self, cart):
        print("\n====== 收据 Receipt ======")
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"时间：{now}")
        for item in cart.items:
            subtotal = item.product.price * item.quantity
            print(f"{item.product.name} x {item.quantity} = ¥{subtotal:.2f}")
        print(f"\n总计 Total: ¥{cart.total_amount():.2f}")
        print("==========================")

# 模拟数据库的商品列表
def get_sample_products():
    return {
        "10001": Product("10001", "牛奶 Milk", 10.0, 5),
        "10002": Product("10002", "面包 Bread", 5.0, 10),
        "10003": Product("10003", "可乐 Coke", 3.5, 20)
    }

# 主程序
if __name__ == "__main__":
    products = get_sample_products()
    cart = Cart()

    print("📦 商品列表:")
    for code, p in products.items():
        print(f"{code}: {p.name} - ¥{p.price} (库存: {p.stock})")

    while True:
        barcode = input("\n请输入商品条码（或输入 q 结账）：").strip()
        if barcode.lower() == 'q':
            break
        if barcode not in products:
            print("❌ 商品条码无效")
            continue

        try:
            quantity = int(input("请输入购买数量："))
            if quantity <= 0:
                print("❌ 数量必须大于 0")
                continue
            cart.add_item(products[barcode], quantity)
        except ValueError:
            print("❌ 请输入有效数字")

    if not cart.items:
        print("🛒 购物车为空，已退出")
    else:
        print(f"\n🧾 应付总额：¥{cart.total_amount():.2f}")
        method = input("请输入支付方式（cash 或 qr）：").strip().lower()

        payment_processor = PaymentProcessor()
        if payment_processor.process_payment(cart.total_amount(), method=method):
            receipt_printer = ReceiptPrinter()
            receipt_printer.print_receipt(cart)
        else:
            print("⚠️ 支付失败，回滚库存...")
            for item in cart.items:
                item.product.stock += item.quantity
            cart.items.clear()
