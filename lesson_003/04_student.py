# -*- coding: utf-8 -*-

# (цикл while)

# Ежемесячная стипендия студента составляет A руб., а расходы на проживание превышают стипендию
# и составляют В руб. в месяц. Рост цен ежемесячно увеличивает расходы на 3%, кроме первого месяца
# Составьте программу расчета суммы денег, которую необходимо единовременно попросить у родителей,
# чтобы можно было прожить учебный год (10 месяцев), используя только эти деньги и стипендию.

A, B = 10000, 12000

scholarship_for_ten_months = A * 10
spending_for_ten_months = B
month = 1
while month < 10:
    B += B * 0.03
    spending_for_ten_months += B
    month += 1

parents_money = round(spending_for_ten_months) - scholarship_for_ten_months
print(parents_money)
