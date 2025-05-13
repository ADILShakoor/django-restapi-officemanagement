from django.shortcuts import render, get_object_or_404,redirect
from .models import Asset
from django.contrib.auth.decorators import login_required
from .forms import AssetForm,AssertCategoryForm

@login_required
def list_assets(request):
    assets = Asset.objects.filter(company=request.user.company)
    # assets = Asset.objects.all() 
    return render(request, 'my_asset/asset_list.html', {'assets': assets})

@login_required
def asset_detail(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id, company=request.user.company)
    # asset = get_object_or_404(Asset, id=asset_id)

    return render(request, 'my_asset/asset_detail.html', {'asset': asset})

@login_required
def add_or_edit_asset(request,asset_id=None):
    if asset_id:
        asset = get_object_or_404(Asset,id=asset_id)
    else:
        asset=None
    if request.method=='POST':
        form=AssetForm(request.POST,instance=asset)
        if form.is_valid():
            asset=form.save(commit=False)
            asset.company=request.user.company
            asset.save()
            return redirect("list_assets")
    else:
        form =AssetForm(instance=asset)
    
    return render(request,'my_asset/add_or_edit_asset.html',{'form':form,"asset":asset})

def assert_category(request):
    if request.method=='POST':
        form=AssertCategoryForm(request.POST)
        if form.is_valid():
            category=form.save(commit=False)
            category.company=request.user.company
            form.save()
            return redirect("add_or_assign_asset")
    else:
        form=AssertCategoryForm()
    return render(request,"my_asset/add_asset_category.html",{"form":form})
            
def add_or_assign_asset(request):
    if request.method=='POST':
        form=AssetForm(request.POST)   
        if form.is_valid():
            asset=form.save(commit=False)
            asset.company=request.user.company
            form.save()
            return redirect("list_assets")
    else:
        form=AssetForm()
    return render(request,'my_asset/add_or_assing_asset.html',{'form':form})

def delete_asset(request,asset_id=None):
    asset=get_object_or_404(Asset,id=asset_id)
    if request.method== 'POST':
        asset.delete()
        print(asset.name)
        return redirect("list_assets")
        
        
    return render(request,'my_asset/confirm_delete_asset.html',{'asset':asset})
    