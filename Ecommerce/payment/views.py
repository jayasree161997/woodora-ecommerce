import logging
import razorpay 
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from products.models import Order,OrderItem,Cart,CartItem
from home.models import Address
from django.contrib import messages
import paypalrestsdk
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import decimal
from decimal import Decimal,InvalidOperation,ROUND_HALF_UP
from datetime import datetime, timedelta
from django.utils.timezone import now
from datetime import timedelta, date

RAZORPAY_KEY_ID = "rzp_test_MAimzLa32DUYt6"
RAZORPAY_SECRET = "qbDDZBXaEQPNG72T9ZPVPytC"




# client = razorpay.Client(auth=("rzp_test_MAimzLa32DUYt6", "qbDDZBXaEQPNG72T9ZPVPytC"))

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=("rzp_test_MAimzLa32DUYt6", "qbDDZBXaEQPNG72T9ZPVPytC"))

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initiate_payment(request):
    if request.method == "GET":
        try:
            # Get the user's cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = CartItem.objects.filter(cart=cart)

            if not cart_items.exists():
                messages.error(request, "Your cart is empty.")
                return redirect('cart_detail')

            # Calculate total cost using Decimal
            total_cost = sum(Decimal(str(item.quantity)) * Decimal(str(item.product.price)) for item in cart_items)
            discount_amount = Decimal(str(cart.discount_amount)) if cart.discount_amount else Decimal("0.00")
            delivery_charge = Decimal("60.00")
            

            # Ensure final price is correctly calculated and formatted
            # final_price = (total_cost - discount_amount).quantize(Decimal("1.00"))  # Ensuring two decimal places
            final_price = (total_cost - discount_amount + delivery_charge).quantize(Decimal("1.00"))  # Ensuring two decimal places

            if final_price <= 0:
                return JsonResponse({"error": "Final amount must be greater than zero."}, status=400)

            # Convert final price to paise for Razorpay
            amount_in_paise = int(final_price * 100)  # Convert to integer

            # Create Razorpay client instance
            client = razorpay.Client(auth=("rzp_test_MAimzLa32DUYt6", "qbDDZBXaEQPNG72T9ZPVPytC"))

            # Create Razorpay order
            order_data = {
                "amount": amount_in_paise,
                "currency": "INR",
                "payment_capture": "1",  # Automatic capture
            }
            razorpay_order = client.order.create(order_data)
            logger.debug(f"Order created successfully: {razorpay_order}")

            # Fetch the first address of the user
            user_address = Address.objects.filter(user=request.user).first()
            if not user_address:
                messages.error(request, "No address found for the user.")
                return redirect('cart_detail')

            # Create Django Order from cart
            django_order = Order.objects.create(
                user=request.user,
                address=user_address,  # Use the fetched address
                total_price=final_price,
                payment_method='RAZORPAY',
                razorpay_order_id=razorpay_order["id"],
                payment_status='Pending',
                coupon_code=cart.coupon_code,
                discount_amount=discount_amount
            )

            # Create OrderItems from CartItems
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=django_order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            context = {
                "amount": amount_in_paise,
                "order_id": razorpay_order["id"],
                "razorpay_key": 'rzp_test_MAimzLa32DUYt6',
                "callback_url": request.build_absolute_uri('/payment/payment-status/'),
            }
            return render(request, "user/payment.html", context)

        except InvalidOperation:
            return JsonResponse({"error": "Invalid decimal operation. Please check the price values."}, status=400)

        except razorpay.errors.BadRequestError as bad_request_error:
            logger.error(f"Bad request error (possibly authentication): {bad_request_error}")
            return JsonResponse({"error": "Payment initiation failed: " + str(bad_request_error)}, status=400)

        except Exception as e:
            logger.error(f"Error occurred during payment initiation: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return redirect('cart_detail')



def set_delivery_date(order):
    """Set the delivery date dynamically based on order status."""
    
    if order.status == "Shipped" and not order.delivery_date:
        order.delivery_date = now() + timedelta(days=7)  # Default: 7 days from today
        order.save(update_fields=["delivery_date"])

    elif order.payment_method == "cash_on_delivery" and not order.delivery_date:
        order.delivery_date = now() + timedelta(days=10)  # Example: 10 days for COD
        order.save(update_fields=["delivery_date"])

logger = logging.getLogger(__name__)

@csrf_exempt


# @login_required
# def payment_success(request):
#     razorpay_payment_id = request.GET.get('razorpay_payment_id')
#     razorpay_order_id = request.GET.get('razorpay_order_id')

#     logger.info(f"Payment Success Called - Order ID: {razorpay_order_id}, Payment ID: {razorpay_payment_id}")

#     if not (razorpay_order_id and razorpay_payment_id):
#         logger.error("Missing payment details")
#         return render(request, "user/payment_success.html", {"error": "Missing payment details."})

#     try:
#         # Ensure order exists
#         order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)

#         # Logging current order details
#         logger.info(f"Fetched Order - ID: {order.id}, Razorpay Payment ID: {order.razorpay_payment_id}")

#         # Update order details
#         order.razorpay_payment_id = razorpay_payment_id
#         order.payment_status = "Success"
#         order.status = "Confirmed"
#         set_delivery_date(order)  # Set delivery date
        #   order.save()

#         # Reduce stock for each product
#         for item in order.order_items.all():
#             product = item.product
#             product.stock -= item.quantity
#             product.save()

#         # Ensure the cart is properly deleted
#         try:
#             cart = Cart.objects.get(user=request.user)
#             cart.cartitem_set.all().delete()
#             cart.delete()
#             logger.info(f"Cart for user {request.user} cleared successfully.")
#         except Cart.DoesNotExist:
#             logger.warning(f"No cart found for user {request.user}")

#         # Fetch purchased products
#         purchased_products = order.order_items.all()
#         if not purchased_products:
#             logger.warning(f"Order {order.id} has no items!")

#         # Pass data to template
#         context = {
#             "order": order,
#             "transaction_id": razorpay_payment_id,
#             "total_amount": order.total_price,
#             "payment_status": order.payment_status,
#             "payment_method": "Razorpay",
#             "payment_state": "Success",
#             "shipping_address": order.address,
#             "purchased_products": purchased_products,
#         }

#         logger.debug(f"Context Data: {context}")

#         return render(request, "user/payment_success.html", context)

#     except Exception as e:
#         logger.error(f"Error updating order: {e}")
#         return render(request, "user/payment_success.html", {"error": str(e)})







@login_required
def payment_success(request):
    razorpay_payment_id = request.GET.get("razorpay_payment_id")
    razorpay_order_id = request.GET.get("razorpay_order_id")

    logger.info(f"Payment Success Called - Order ID: {razorpay_order_id}, Payment ID: {razorpay_payment_id}")

    if not (razorpay_order_id and razorpay_payment_id):
        logger.error("Missing payment details")
        return render(request, "user/payment_success.html", {"error": "Missing payment details."})

    try:
        # Fetch the order using Razorpay order ID
        order = get_object_or_404(Order, razorpay_order_id=razorpay_order_id)

        # Log order details
        logger.info(f"Fetched Order - ID: {order.id}, Razorpay Payment ID: {order.razorpay_payment_id}")

        # Update order details
        order.razorpay_payment_id = razorpay_payment_id
        order.payment_status = "Success"
        order.status = "Confirmed"
        set_delivery_date(order)
        order.save()

        # Reduce stock for each purchased product
        order_items = order.order_items.all()  # ✅ Correct related_name
        for item in order.order_items.all():
            product = item.product
            product.stock -= item.quantity
            product.save()

        # Clear user's cart
        try:
            cart = Cart.objects.get(user=request.user)
            cart.cartitem_set.all().delete()  # ✅ Correct related_name
            cart.delete()
            logger.info(f"Cart for user {request.user} cleared successfully.")
        except Cart.DoesNotExist:
            logger.warning(f"No cart found for user {request.user}")

            
#         # Fetch purchased products
        purchased_products = order.order_items.all()
        if not purchased_products:
            logger.warning(f"Order {order.id} has no items!")

        if not order.delivery_date:
            order.delivery_date = date.today() + timedelta(days=7)  # Example: 5 days from today
            order.save()


        # Pass order details to the template

        context = {
            "order": order,
            "transaction_id": razorpay_payment_id,
            "total_amount": order.total_price,
            "payment_status": order.payment_status,
            "payment_method": "Razorpay",
            "payment_state": "Success",
            "shipping_address": order.address,  # Ensure Order model has address field
            "purchased_products": order_items,
            # "purchased_products": purchased_products
        }

        logger.debug(f"Context Data: {context}")

        return render(request, "user/payment_success.html", context)

    except Exception as e:
        logger.error(f"Error updating order: {e}")
        return render(request, "user/payment_success.html", {"error": str(e)})



@login_required
def payment_failure(request):
    return render(request, "user/payment-failed.html", {"error": "Payment failed. Please try again or contact support."})












