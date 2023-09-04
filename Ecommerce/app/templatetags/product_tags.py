from django import template
import math

register = template.Library()


@register.simple_tag
def call_sellprise(price, discount):

    if discount is None or discount == 0:
        return price

    sellprice = price
    sellprice = price - (price * discount / 100)
    print(math.floor(sellprice))
    return math.floor(sellprice)


@register.simple_tag
def progress_bar(total_quantity, Availability):
    progress_bar = Availability
    progress_bar = Availability * (100 / total_quantity)
    return math.floor(progress_bar)



