from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from crm.models.property import Property, PropertyImage
from crm.forms.property import PropertyForm


@login_required
def property_list(request):
    qs = Property.objects.select_related('listed_by').prefetch_related('images')

    search = request.GET.get('q')
    if search:
        qs = qs.filter(
            Q(title__icontains=search) |
            Q(listing_id__icontains=search) |
            Q(city__icontains=search) |
            Q(address__icontains=search)
        )

    property_type = request.GET.get('type')
    if property_type:
        qs = qs.filter(property_type=property_type)

    status = request.GET.get('status')
    if status:
        qs = qs.filter(status=status)

    city = request.GET.get('city')
    if city:
        qs = qs.filter(city__icontains=city)

    min_price = request.GET.get('min_price')
    if min_price:
        qs = qs.filter(price__gte=min_price)

    max_price = request.GET.get('max_price')
    if max_price:
        qs = qs.filter(price__lte=max_price)

    min_beds = request.GET.get('min_beds')
    if min_beds:
        qs = qs.filter(bedrooms__gte=int(min_beds))

    featured = request.GET.get('featured')
    if featured:
        qs = qs.filter(featured=True)

    sort = request.GET.get('sort', '-listed_date')
    qs = qs.order_by(sort)

    paginator = Paginator(qs, 12)
    page = request.GET.get('page')
    properties = paginator.get_page(page)

    cities = Property.objects.values_list('city', flat=True).distinct().order_by('city')

    context = {
        'properties': properties,
        'cities': cities,
        'search': search,
    }
    return render(request, 'crm/property_list.html', context)


@login_required
def property_create(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            prop = form.save(commit=False)
            prop.listed_by = request.user
            prop.save()
            messages.success(request, f'Property {prop.listing_id} created successfully.')
            return redirect('property_detail', pk=prop.pk)
    else:
        form = PropertyForm()
    return render(request, 'crm/property_form.html', {'form': form, 'title': 'Add Property'})


@login_required
def property_detail(request, pk):
    prop = get_object_or_404(Property.objects.prefetch_related('images', 'documents', 'deals', 'visits'), pk=pk)
    context = {
        'property': prop,
        'images': prop.images.all(),
        'deals': prop.deals.select_related('lead', 'agent')[:5],
    }
    return render(request, 'crm/property_detail.html', context)


@login_required
def property_edit(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=prop)
        if form.is_valid():
            form.save()
            messages.success(request, 'Property updated successfully.')
            return redirect('property_detail', pk=prop.pk)
    else:
        form = PropertyForm(instance=prop)
    return render(request, 'crm/property_form.html', {'form': form, 'title': 'Edit Property', 'property': prop})


@login_required
def property_delete(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        prop.delete()
        messages.success(request, 'Property deleted.')
        return redirect('property_list')
    return render(request, 'crm/property_confirm_delete.html', {'property': prop})


@login_required
def property_add_image(request, pk):
    prop = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        image = request.FILES.get('image')
        caption = request.POST.get('caption', '')
        is_primary = request.POST.get('is_primary') == 'on'
        if image:
            if is_primary:
                prop.images.update(is_primary=False)
            PropertyImage.objects.create(property=prop, image=image, caption=caption, is_primary=is_primary)
            messages.success(request, 'Image added.')
    return redirect('property_detail', pk=pk)
