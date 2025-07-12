from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from .forms import SwapRequestForm

from .forms import RegisterForm, ItemForm
from .models import Item, SwapRequest, SellRequest, UserProfile


# Admin check
def is_admin(user):
    return user.is_staff


# User registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


# Homepage with featured items
def index(request):
    featured = Item.objects.filter(status='available')[:5]
    return render(request, 'core/index.html', {'items': featured})


# List of all available items with optional search
def item_list(request):
    items = Item.objects.filter(status='available')
    query = request.GET.get('q')
    if query:
        items = items.filter(Q(title__icontains=query) | Q(tags__icontains=query))
    return render(request, 'core/item_list.html', {'items': items})


# Item detail page
def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    can_request = False
    already_requested = False

    if (
        request.user.is_authenticated
        and item.uploader != request.user
        and item.status == 'available'
        and item.type == 'swap'
    ):
        can_request = True
        already_requested = SwapRequest.objects.filter(item=item, requester=request.user).exists()

    return render(request, 'core/item_detail.html', {
        'item': item,
        'can_request': can_request,
        'already_requested': already_requested
    })


# Upload new item (pending approval)
@login_required
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.uploader = request.user
            item.status = 'pending'
            item.save()
            messages.success(request, "Item uploaded and awaiting admin approval.")
            return redirect('dashboard')
    else:
        form = ItemForm()
    return render(request, 'core/add_item.html', {'form': form})


# User dashboard: uploaded items, incoming & outgoing requests
@login_required
def dashboard(request):
    my_items = Item.objects.filter(uploader=request.user)
    incoming = SwapRequest.objects.filter(item__uploader=request.user).exclude(requester=request.user)
    outgoing = SwapRequest.objects.filter(requester=request.user)
    return render(request, 'core/dashboard.html', {
        'items': my_items,
        'incoming': incoming,
        'outgoing': outgoing,
    })


# User sends swap request

@login_required
def request_swap(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if item.uploader == request.user:
        messages.error(request, "You can't request your own item.")
        return redirect('item_detail', item_id=item.id)

    if item.status != 'available' or item.type != 'swap':
        messages.error(request, "This item is not available for swap.")
        return redirect('item_detail', item_id=item.id)

    my_items = Item.objects.filter(uploader=request.user, status='available', type='swap')

    if request.method == 'POST':
        offered_item_id = request.POST.get('offered_item')
        offered_item = get_object_or_404(Item, pk=offered_item_id, uploader=request.user, status='available', type='swap')

        if SwapRequest.objects.filter(item=item, requester=request.user, offered_item=offered_item, status='pending').exists():
            messages.warning(request, "You have already sent a request with this item.")
        else:
            SwapRequest.objects.create(item=item, requester=request.user, offered_item=offered_item)
            messages.success(request, "Swap request sent successfully.")
        return redirect('item_detail', item_id=item.id)

    return render(request, 'core/manage_requests.html', {
        'item': item,
        'my_items': my_items,
    })





# Uploader accepts or rejects swap request
@login_required
def respond_request(request, req_id, action):
    swap = get_object_or_404(SwapRequest, pk=req_id, item__uploader=request.user)
    if swap.status == 'pending':
        if action == 'accept':
            swap.status = 'accepted'
            swap.item.status = 'swapped'
            swap.item.save()
            swap.save()
            SwapRequest.objects.filter(item=swap.item, status='pending').exclude(pk=swap.pk).update(status='rejected')
            messages.success(request, "Swap request accepted.")
        elif action == 'reject':
            swap.status = 'rejected'
            swap.save()
            messages.info(request, "Swap request rejected.")
    else:
        messages.warning(request, "This request has already been processed.")
    return redirect('dashboard')


# Redeem item using points (fixed price or item.price)
@login_required
def redeem_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, type='redeem', status='available')
    buyer_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    uploader_profile, _ = UserProfile.objects.get_or_create(user=item.uploader)

    cost = item.price if item.price is not None else 50

    if request.user == item.uploader:
        messages.error(request, "You can't redeem your own item.")
        return redirect('item_detail', item_id=item_id)

    if buyer_profile.points < cost:
        messages.error(request, "Not enough points to redeem this item.")
    else:
        item.status = 'swapped'
        item.save()

        buyer_profile.points -= cost
        uploader_profile.points += cost
        buyer_profile.save()
        uploader_profile.save()

        SellRequest.objects.create(item=item, buyer=request.user, status='completed')

        messages.success(request, f"Item successfully redeemed for {cost} points.")
    return redirect('item_detail', item_id=item_id)


# Purchase sellable item
@login_required
def buy_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, type='sell', status='available')
    buyer = request.user
    seller_profile, _ = UserProfile.objects.get_or_create(user=item.uploader)
    buyer_profile, _ = UserProfile.objects.get_or_create(user=buyer)

    if buyer == item.uploader:
        messages.error(request, "You can't buy your own item.")
        return redirect('item_detail', item_id=item.id)

    if buyer_profile.points < item.price:
        messages.error(request, "You do not have enough points to buy this item.")
        return redirect('item_detail', item_id=item.id)

    # Process transaction
    buyer_profile.points -= item.price
    seller_profile.points += item.price
    buyer_profile.save()
    seller_profile.save()

    item.status = 'swapped'
    item.save()

    SellRequest.objects.create(item=item, buyer=buyer, status='completed')

    messages.success(request, "Purchase successful!")
    return redirect('dashboard')


# Admin view: items pending approval
@user_passes_test(is_admin)
def admin_approve_list(request):
    items = Item.objects.filter(status='pending')
    return render(request, 'core/admin_approve_list.html', {'items': items})


# Admin approves item
@user_passes_test(is_admin)
def approve_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, status='pending')
    item.status = 'available'
    item.save()
    messages.success(request, f"{item.title} approved and is now available.")
    return redirect('admin_approve_list')


# Admin rejects item
@user_passes_test(is_admin)
def reject_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id, status='pending')
    item.delete()
    messages.info(request, f"{item.title} has been rejected and deleted.")
    return redirect('admin_approve_list')
