from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from .models import EmployeeDocument
from .forms import EmployeeDocumentForm

@login_required
def document_list(request):
  role=request.user.role
  print(role)
  if role=="ceo" or role=="hr": 
    documents = EmployeeDocument.objects.filter(company=request.user.company)
    return render(request, 'document_management/document_list.html', {'documents': documents})
  if role!="ceo" or role!="hr": 
    documents = EmployeeDocument.objects.filter(employee=request.user)
    return render(request, 'document_management/document_list.html', {'documents': documents})

  return HttpResponse("You are not allowed to perform this action.") 

@login_required
def document_upload(request):
  role=request.user.role 
  if role=="ceo" or role=="hr": 
    if request.method == 'POST':
        form = EmployeeDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.company=request.user.company
            if doc.signature_link: 
               doc.is_signed = True
            # doc.employee = request.user
            doc.save()
            return redirect('document-list')
    else:
        form = EmployeeDocumentForm()
    return render(request, 'document_management/document_upload.html', {'form': form})
  return HttpResponse("You are not allowed to perform this action.")

@login_required
def document_detail(request, pk):
    document = get_object_or_404(EmployeeDocument, pk=pk, company=request.user.company)
    return render(request, 'document_management/document_detail.html', {'document': document})

# for employee use 