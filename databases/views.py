from django.db.models.fields import related
from databases.models import *
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def index(request):
    db = Figures_db.objects.all()
    context={}
    context['db'] = db
    return render(request,'databases/mfc.html',context)


def database(request):
    context = {
            'category' : Category.objects.all(),
            'subcategory' : SubCategory.objects.all,
            'origins' : Entries.objects.filter(category="Origin"),
            'characters' : Entries.objects.filter(category="Character"),
            'companies' : Entries.objects.filter(category="Company"),
            'artists' : Entries.objects.filter(category="Artist"),
            'classcifications' : Entries.objects.filter(category="Classification"),
            'materials' : Entries.objects.filter(category="Material"),
            'events' : Entries.objects.filter(category="Event"),
        }
    if request.method == "GET":
        return render(request,'databases/index.html',context)
    else:
        _subcat = request.POST.getlist('subcategory')
        _pic = request.FILES['pic1']
        _nsfw = request.POST.get('nsfw','False')
        _cancelled = request.POST.get('canceled','False')
        _origin = request.POST['origin']
        _character = request.POST['character']
        _company = request.POST['company']
        _artist = request.POST['artist']
        _classification = request.POST['classification']
        _material = request.POST['material']
        _event = request.POST['event']
        _date = request.POST.getlist('date',None)
        _version = request.POST['version']
        _original_version = request.POST['original_version']
        _numbering = request.POST['numbering']
        _scale = request.POST['scale']
        _part = request.POST['part']
        _dimension = request.POST['dimension']
        _weight = request.POST['weight']
        _title = request.POST['title']
        _original_title = request.POST['original_title']
        _pages = request.POST['page']
        _size = request.POST['size']
        _episode = request.POST['episodes']
        _track = request.POST['tracks']
        _disc = request.POST['discs']
        _runtime = request.POST['runtime']
        _region = request.POST.get('region','False')
        _rating = request.POST.get('rating',None)
        _description = request.POST['description']

        if not _pic:
            messages.error(request, 'No picture found!')
            return redirect("database")

        if not _company:
            messages.error(request, 'Company is required!')
            return redirect("database")

        db = None
        if _company:
            db =  Figures_db()
            db.pic = _pic
            db.title = _title 
            db.original_title = _original_title 
            if _pages:
                db.pages = _pages 
            db.paper_size = _size
            db.tracks = _track 
            db.discs = _disc
            if _runtime:
                db.runtime = _runtime
            db.description = _description
            db.region_free = _region
            db.version = _version
            db.original_version = _original_version
            if _numbering:
                db.numbering = _numbering
            if _scale:
                db.scale = _scale
            if _part:
                db.no_of_parts = _part
            db.cancelled = _cancelled
            db.rating = _rating
            db.nsfw = _nsfw
            if _episode:
                db.episodes = _episode
            db.dimensions = _dimension
            db.weight = _weight
            db.save()
            messages.success(request,"Object created successfully")
        else:
            messages.error(request,"Image and Company name is required!")
            return redirect("database")
        
        if _origin:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_origin)
            )
        
        if _company:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_company)
            )

        if _character:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_character)
            )
        
        if _artist:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_artist)
            )

        if _classification:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_classification)
            )
        
        if _material:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_material)
            )

        if _event:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_event)
            )

        if _date:
            for i in _date:
                release = None
                release = Figures_Releases.objects.get(
                    id = i
                )
                release.figure = db
                release.save()

        if _subcat:
            for i in _subcat:
                type = None
                type = Figures_category.objects.create(
                    figure = db,
                    category = SubCategory.objects.get(id=i)
                )
                type.save()

        return render(request,'databases/index.html',context)

def releases(request):
    data = {'success': False} 
    if request.method=='POST':
        _run = request.POST.get('run','null')
        _price = request.POST.get('price','null')
        _date = request.POST.get('date')
        _barcode = request.POST.get('barcode','null')
        _catalog = request.POST.get('catalog','null')
        _info = request.POST.get('info','null')
        obj = None
        if _date:
            try:
                obj = Figures_Releases.objects.get(
                date = _date,
                run = _run,
                price = _price,
                info = _info,
                catalog = _catalog,
                barcode = _barcode
                )
                data['success'] = True
                data['object'] = obj.id
            except:
                obj = Figures_Releases.objects.create(
                    date = _date,
                    run = _run,
                    price = _price,
                    info = _info,
                    catalog = _catalog,
                    barcode = _barcode
                )
                data['success'] = True
                data['object'] = obj.id
                data['date'] = obj.date
        else:
            data['success'] = False

    return JsonResponse(data)

def entries(request):
    data = {'success': False} 
    if request.method=='POST':
        _name = request.POST.get('name')
        _original = request.POST.get('original')
        _category = request.POST.get('object')
        print(_category)

        obj = None
        if _name and _original and _category:
            try:
                obj = Entries.objects.get(
                    category = _category,
                    name = _name,
                )
                data['success'] = True
                data['msg'] = "Entries with similar name already existed"
            except:
                obj = Entries.objects.create(
                    category = _category,
                    name = _name,
                    original_name = _original
                )
                data['success'] = True
                data['object'] = obj.id
                data['msg'] = "Entry created successfully, kindly reload the page to see the list"
        else:
            data['success'] = False

    return JsonResponse(data)

def details(request,id):
    context = {}
    obj = Figures_db.objects.get(id=id)
    context['obj'] = obj
    context['origin'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Origin").first()
    context['event'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Event").first()
    context['material'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Material").first()
    context['classification'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Classification").first()
    context['artist'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Artist").first()
    context['company'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Company").first()
    context['character'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Character").first()
    context['release'] = Figures_Releases.objects.filter(figure=obj)
    context['subcategory'] =Figures_category.objects.filter(figure=obj)
    return render(request,'databases/details.html',context)

def update(request,id):
    if request.method == "GET":
        context = {}
        obj = Figures_db.objects.get(id=id)
        context['obj'] = obj
        context['category'] = Category.objects.all()
        context['subcategory'] = SubCategory.objects.all
        context['origins'] = Entries.objects.filter(category="Origins")
        context['characters'] = Entries.objects.filter(category="Characters")
        context['companies'] = Entries.objects.filter(category="Companies")
        context['artists'] = Entries.objects.filter(category="Artists")
        context['classcifications'] = Entries.objects.filter(category="Classifications")
        context['materials'] = Entries.objects.filter(category="Materials")
        context['events'] = Entries.objects.filter(category="Events")
        context['ratings'] = Entries.objects.filter(category="Ratings")
        context['origin'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Origin").first()
        context['event'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Event").first()
        context['material'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Material").first()
        context['classification'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Classification").first()
        context['artist'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Artist").first()
        context['company'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Company").first()
        context['character'] = Figures_entries.objects.filter(figure=obj,entry__category__contains="Character").first()
        context['release'] = Figures_Releases.objects.filter(figure=obj)
        context['subcategory'] =Figures_category.objects.filter(figure=obj)
        return render(request,'databases/update.html',context)
    else:
        context = {}
        _pic = request.FILES.get('pic1',None)
        _origin = request.POST['origin']
        _character = request.POST['character']
        _company = request.POST['company']
        _artist = request.POST['artist']
        _classification = request.POST['classification']
        _material = request.POST['material']
        _event = request.POST['event']
        _date = request.POST.getlist('date',None)
        _version = request.POST['version']
        _original_version = request.POST['original_version']
        _numbering = request.POST['numbering']
        _scale = request.POST['scale']
        _part = request.POST['part']
        _dimension = request.POST['dimension']
        _weight = request.POST['weight']
        _title = request.POST['title']
        _original_title = request.POST['original_title']
        _pages = request.POST['page']
        _size = request.POST['size']
        _episode = request.POST['episodes']
        _track = request.POST['tracks']
        _disc = request.POST['discs']
        _runtime = request.POST['runtime']
        _description = request.POST['description']

        db =  Figures_db.objects.get(id=id)
        if _pic:
            db.pic = _pic
        db.title = _title 
        db.original_title = _original_title 
        if _pages:
            db.pages = _pages 
        db.paper_size = _size
        db.tracks = _track 
        db.discs = _disc
        if _runtime:
            db.runtime = _runtime
        db.description = _description
        db.version = _version
        db.original_version = _original_version
        if _numbering:
            db.numbering = _numbering
        if _scale:
            db.scale = _scale
        if _part:
            db.no_of_parts = _part
        if _episode:
            db.episodes = _episode
        db.dimensions = _dimension
        db.weight = _weight
        db.save()
        messages.success(request,"Object updated successfully")

        if _origin:
            try:
                Figures_entries.objects.get(
                    figure = db,
                    entry = Entries.objects.get(id=_origin)
                )
            except:
                Figures_entries.objects.create(
                    figure = db,
                    entry = Entries.objects.get(id=_origin)
                )
        
        if _company:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_company)
            )

        if _character:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_character)
            )
        
        if _artist:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_artist)
            )

        if _classification:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_classification)
            )
        
        if _material:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_material)
            )

        if _event:
            Figures_entries.objects.create(
                figure = db,
                entry = Entries.objects.get(id=_event)
            )

        if _date:
            for i in _date:
                release = None
                release = Figures_Releases.objects.get(
                    id = i
                )
                release.figure = db
                release.save()

        return redirect("update",id)

