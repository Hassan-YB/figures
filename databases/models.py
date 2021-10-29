from django.db import models
from django.db.models.query_utils import subclasses

#Database entry
class Figures_db(models.Model):
    pic = models.ImageField(upload_to="media")
    title = models.CharField(max_length=50,blank=True,null=True)
    original_title = models.CharField(max_length=50,blank=True,null=True)
    pages = models.IntegerField(blank=True,null=True)
    paper_size = models.CharField(max_length=50,blank=True,null=True)
    tracks = models.CharField(max_length=50,blank=True,null=True)
    discs = models.CharField(max_length=50,blank=True,null=True)
    runtime = models.IntegerField(blank=True,null=True)
    description = models.CharField(max_length=1000,blank=True,null=True)
    region_free = models.BooleanField(default=False,null=True)
    version = models.CharField(max_length=50,blank=True,null=True)
    original_version = models.CharField(max_length=50,blank=True,null=True)
    numbering = models.CharField(max_length=50,blank=True,null=True)
    scale = models.IntegerField(blank=True,null=True)
    no_of_parts = models.IntegerField(blank=True,null=True)
    cancelled = models.BooleanField(default=False)
    rating = models.CharField(max_length=1000,blank=True,null=True)
    nsfw = models.BooleanField(default=False)
    episodes = models.IntegerField(blank=True,null=True)
    dimensions = models.CharField(max_length=100,blank=True,null=True)
    weight = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return f"id = {self.id}"

    class Meta:
        verbose_name = 'Figure'
        verbose_name_plural = 'Figures'

#Releases block 
class Figures_Releases(models.Model):
    date = models.DateField()
    price = models.CharField(max_length=50,default="Null")
    barcode = models.CharField(max_length=50,default="Null")
    catalog = models.CharField(max_length=50,default="Null")
    info = models.CharField(max_length=1000,default="Null")
    run = models.CharField(max_length=50,default="Null")
    figure = models.ForeignKey(Figures_db,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.date)
    
    def get_date(self):
        return str(self.date)

    class Meta:
        verbose_name = 'Release'
        verbose_name_plural = 'Releases'

#Cateogory block db
class Category(models.Model):
    root = models.CharField(max_length=50,default="Null")

    def __str__(self):
        return self.root

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

class SubCategory(models.Model):
    subcategory = models.CharField(max_length=50,default="Null")
    root = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.subcategory

    class Meta:
        verbose_name = 'Sub-Category'
        verbose_name_plural = 'Sub-Categories'

#Entries block db
class Entries(models.Model):
    category = models.CharField(max_length=50,default="Null")
    name = models.CharField(max_length=100,default="Null")
    original_name = models.CharField(max_length=100,default="Null")
    other_name = models.CharField(max_length=50,null=True,blank=True)
    homepage = models.CharField(max_length=50,default="Null",null=True,blank=True)
    image = models.ImageField(upload_to="media",null=True,blank=True)
    pg = models.BooleanField(default=False)
    description = models.CharField(max_length=1000,null=True,blank=True)
    source = models.CharField(max_length=100,null=True,blank=True)
    note = models.CharField(max_length=500,null=True,blank=True)

    def __str__(self):
        return str(self.category)+" : "+self.name

    class Meta:
        verbose_name = 'Entry'
        verbose_name_plural = 'Entries'
        
#Pictures block db
class Pictures(models.Model):
    figure = models.ForeignKey(Figures_db,on_delete=models.CASCADE,null=True)
    picture = models.ImageField(upload_to="media")

    def __str__(self):
        return self.picture
    
    class Meta:
        verbose_name = 'Picture'
        verbose_name_plural = 'Pictures'

class Figures_entries(models.Model):
    figure = models.ForeignKey(Figures_db,on_delete=models.CASCADE)
    entry = models.ForeignKey(Entries,on_delete=models.CASCADE)

    def __str__(self):
        return f"Figure id = {self.figure.id}" + " : " + f"{self.entry.category}"

    class Meta:
        verbose_name = 'Figure Entry'

class Figures_category(models.Model):
    figure = models.ForeignKey(Figures_db,on_delete=models.CASCADE)
    category = models.ForeignKey(SubCategory,on_delete=models.CASCADE)

    def __str__(self):
        return self.category.subcategory

    class Meta:
        verbose_name = 'Figure Category'
