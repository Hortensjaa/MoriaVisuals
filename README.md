# Moria Visuals - my ecommerce project
Moria is my friend's clothing brand ([credit to Michał!](https://www.instagram.com/moria.visuals)). 
One day, we came up with an idea to create a website to manage payments and orders.
And here it is — in project stage — Moria ecommerce website.

## Overview
The whole project is built using a Django framework. 
I focused on backend development (to be honest, frontend is not my thing... but you can see, I tried). 

💥 The most important features (some of them are not yet implemented):
- [x] [custom (hehe) Customer model](customers/models.py)
- [x] [customer's cart](carts)
- [x] [orders handling](orders)
- [x] [PayPal's payment service (for now using a sandbox account)](orders/views.py#:~:text=process_payment)
- [x] [automatic emails with order summaries using STMP](orders/views.py#:~:text=send_confirmation_email)
- [ ] delivery options (other than self-pickup) handling
- [ ] more payment options