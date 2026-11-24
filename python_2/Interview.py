item_prices = [12.50, 8.00, 20.00, 4.50]
discount_rate = 0.10
cart_total = 0
for current_price in item_prices:
    cart_total += current_price
discount_amount = cart_total * discount_rate
final_total = cart_total - discount_amount
print("Cart total:", cart_total)
print("Final total after discount:", final_total)