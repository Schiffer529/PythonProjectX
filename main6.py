from datetime import date
from typing import List

# -------------------------------
# 类定义（与前版相同）
# -------------------------------
class Customer:
    def __init__(self, name: str, contact: str, delivery_address: str, active: bool):
        self.name = name
        self.contact = contact
        self.delivery_address = delivery_address
        self.active = active

class Product:
    def __init__(self, title: str, weight: float, description: str, price: float):
        self.title = title
        self.weight = weight
        self.description = description
        self.price = price

    def get_price_for_quantity(self, quantity: int) -> float:
        return self.price * quantity

    def get_weight(self) -> float:
        return self.weight

class OrderDetail:
    def __init__(self, product: Product, quantity: int):
        self.product = product
        self.quantity = quantity

    def calculate_sub_total(self) -> float:
        return self.product.get_price_for_quantity(self.quantity)

    def calculate_weight(self) -> float:
        return self.product.get_weight() * self.quantity

class Payment:
    def __init__(self, amount: float):
        self.amount = amount

class Order:
    def __init__(self, create_date: date, status: str, customer: Customer, payment: Payment):
        self.create_date = create_date
        self.status = status
        self.customer = customer
        self.payment = payment
        self.details: List[OrderDetail] = []

    def add_detail(self, detail: OrderDetail):
        self.details.append(detail)

    def get_total_amount(self) -> float:
        return sum(detail.calculate_sub_total() for detail in self.details)

    def get_total_weight(self) -> float:
        return sum(detail.calculate_weight() for detail in self.details)

# -------------------------------
# 用户交互入口
# -------------------------------
if __name__ == "__main__":
    print("=== 客户信息输入 ===")
    name = input("姓名：")
    contact = input("联系电话：")
    address = input("邮寄地址：")
    active_input = input("是否激活（是/否）：")
    active = True if active_input == "是" else False
    customer = Customer(name, contact, address, active)

    print("\n=== 商品信息输入 ===")
    title = input("商品名称：")
    weight = float(input("单件重量（kg）："))
    description = input("商品描述：")
    price = float(input("单件价格（元）："))
    quantity = int(input("购买数量："))
    product = Product(title, weight, description, price)
    detail = OrderDetail(product, quantity)

    print("\n=== 支付信息 ===")
    amount = detail.calculate_sub_total()
    payment = Payment(amount)

    order = Order(date.today(), "PAID", customer, payment)
    order.add_detail(detail)

    print("\n=== 订单结果 ===")
    print("客户：", customer.name)
    print("总金额：", order.get_total_amount())
    print("总重量：", order.get_total_weight(), "kg")
