import redis
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib import messages

from .forms import ImageCreateForm

from .models import Image

from images.common.decorators import ajax_required
from actions.utils import create_action

# connect to redis
r = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_item = form.save(commit=False)
            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image add successfully')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.POST)
    context = {
        'section': 'images',
        'form': form
    }
    return render(request, 'images/create.html', context)


@login_required
def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    # increment total image views by 1
    total_views = r.incr('image:{}:views'.format(image.id))
    # increment image ranking by 1
    r.zincrby('image_ranking', image.id, 1)

    context = {
        'section': 'images',
        'image': image,
        'total_views': total_views,
    }
    return render(request, 'images/detail.html', context)


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.GET.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.user_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required
def images_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
    images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'images/list_ajax.html', {'section': 'images', 'images': images})
    return render(request, 'images/list.html', {'section': 'images', 'images': images})


@login_required
def image_ranking(request):
    # get image ranking dictionary
    image_rankin = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_rankin_ids = [int(id) for id in image_rankin]
    # get most views image
    most_viewed = list(Image.objects.filter(id__in=image_rankin_ids))
    most_viewed.sort(key=lambda x: image_rankin_ids.index(x.id))
    return render(request, 'images/ranking.html', {'section': 'images', 'most_viewed': most_viewed})
