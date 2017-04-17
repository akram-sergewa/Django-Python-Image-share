# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from myproject.myapp.models import Document
from myproject.myapp.forms import DocumentForm

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from myproject.myapp.forms import RegistrationForm, LoginForm, EditForm, ChooseFXForm
from myproject.myapp.models import Drinker
from django.contrib.auth import authenticate, login, logout
from myproject.myapp.imgvidfx import FaceDetection
from myproject.myapp.imgvidfx import MakeVideoFX, ImageEffects

def mainPage(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.list'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    documents = Document.objects.all()

    # Render list page with the documents and the form
    if not request.user.is_authenticated():
        drinker = 'drinker'
    else:
        drinker = request.user.drinker
        
    context = {'drinker': drinker, 'form': form}
    return render_to_response(
        'mainPage.html',context,context_instance=RequestContext(request)
    )

def UserRegistration(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/myapp/profile/')
        if request.method == 'POST':
                form = RegistrationForm(request.POST)
                if form.is_valid():
                        user = User.objects.create_user(username=form.cleaned_data['username'], email = form.cleaned_data['email'], password = form.cleaned_data['password'])
                        user.save()
                        drinker = Drinker(user=user, name=form.cleaned_data['name'], birthday=form.cleaned_data['birthday'])
                        drinker.save()
                        return HttpResponseRedirect('/myapp/profile/')
                else:
                        return render_to_response('register.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show them a blank registration form '''
                form = RegistrationForm()
                context = {'form': form}
                return render_to_response('register.html', context, context_instance=RequestContext(request))

def LoginRequest(request):
        if request.user.is_authenticated():
                return HttpResponseRedirect('/myapp/profile/')
        if request.method == 'POST':
                form = LoginForm(request.POST)
                if form.is_valid():
                        username = form.cleaned_data['username']
                        password = form.cleaned_data['password']
                        drinker = authenticate(username=username, password=password)
                        if drinker is not None:
                                login(request, drinker)
                                return HttpResponseRedirect('/')
                        else:
                                return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
                else:
                        return render_to_response('login.html', {'form': form}, context_instance=RequestContext(request))
        else:
                ''' user is not submitting the form, show the login form '''
                form = LoginForm()
                context = {'form': form}
                return render_to_response('login.html', context, context_instance=RequestContext(request))

def LogoutRequest(request):
        logout(request)
        return HttpResponseRedirect('/')
	
@login_required
def Profile(request):
        MAX_SPACE = 100
        if not request.user.is_authenticated():
                return HrttpResponseRedirect('/login/')


        drinker = request.user.drinker
        documents = Document.objects.filter(owner=drinker)
        context = {'drinker': drinker, 'usedSpace': getSize(documents), 'maxSpace': MAX_SPACE}
        return render_to_response('profile.html', context, context_instance=RequestContext(request))

@login_required
def Browse(request):
    MAX_SPACE = 100
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            print "####################################################"
            print "FORM IS VALID"
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.owner = request.user.drinker
            newdoc.description = form.cleaned_data['description']
            newdoc.shared = form.cleaned_data['shared'] 
            documents =Document.objects.filter(owner = request.user.drinker)
            
            allSpace = getSize(documents) + (newdoc.docfile.size/(1024*1024))
            
            #Check if allowed space is exceeded
            if allSpace > MAX_SPACE:
                context = {'error': 'You exceeded your Space, delete some photos to Upload new ones'}
                return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
                
                
            newdoc.save()
        else:
            print "####################################################"
            print "FORM IS NOT VALID"
            

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('myproject.myapp.views.Browse'))
    else:
        form = DocumentForm()  # A empty, unbound form
        

    # Load documents for the list page
    #documents = Document.objects.all()
    page = request.GET.get('p', False)
    print "look here here here here here"
    print page 
    if page == False:
        page = 1
        page = int(page)
    else:
        if page.isdigit():
            page = int(page)
        else:
            page = 1

    if page < 1:
        page = 1
    
    elementsPerPage = 8
    lastElement = page * elementsPerPage
    firstElement = lastElement - elementsPerPage
    
    drinker = request.user.drinker
    documents = Document.objects.filter(owner=drinker).order_by('-id')[firstElement:lastElement]
    
    next = False
    previous = False
    #Check if there are objects in the previous page
    
    try:
        Document.objects.filter(owner=drinker).order_by('-id')[firstElement-elementsPerPage:lastElement-elementsPerPage]
        previous = True
    except :
        previous = False
   
    try:
        Document.objects.filter(owner=drinker).order_by('-id')[firstElement+elementsPerPage:lastElement+elementsPerPage]
        next = True
    except :
        next = False
    
        
    # Render list page with the documents and the form
    return render_to_response(
        'browse.html',
        {'documents': documents, 'form': form, 'drinker': drinker, 'next': next, 'previous': previous, 'npage': page+1, 'ppage': page-1},
        context_instance=RequestContext(request)
    )
 
    
@login_required
def ApplyFX(request):
        if not request.user.is_authenticated():
                return HrttpResponseRedirect('/login/')
        if request.method == 'GET':
            # List of chosen images
            #try:
            img_id = int(request.GET.get('img_id'))
            fx_id = int(request.GET.get('fx_id'))

            document = Document.objects.filter(pk=img_id)
            
            if not document[0].owner == request.user.drinker:
                context = {'error': 'You cannot delete this image, You donnot own this image'}
                return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
                    
            documentFX = Document.objects.filter(pk=fx_id)
            document_URL = document[0].docfile.url
            
            if not documentFX[0].fx:
                context = {'error': 'You cannot delete this image, You donnot own this image'}
                return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
                    
            documentFX_URL = documentFX[0].docfile.url
            imageEffects = ImageEffects(document_URL,documentFX_URL, request.user.username)
            imageEffects.applyFX()
            newDocumentPath = imageEffects.getDstPath()
        
            document = Document.objects.filter(pk=img_id)
                
            #except:
            #context = {'error': 'There is no image'}
            #return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
                
            
            
            ## Store the file in the database
            newdoc = Document(docfile=newDocumentPath)
            newdoc.owner = request.user.drinker
            newdoc.save()
            return HttpResponseRedirect('/myapp/browse/')
        
        context = {'error': 'Check the source and effect'}
        return render_to_response('errorPage.html', context, context_instance=RequestContext(request))                
            

        
        
@login_required
def DeleteImage(request):
        if not request.user.is_authenticated():
                return HrttpResponseRedirect('/login/')
        if request.method == 'GET':
            # Delete image
            img_id = request.GET.get('img_id', False)
            #documents = Document.objects.filter(docfile.name=imageName)
            document = Document.objects.filter(pk=img_id)
            if not document[0].owner == request.user.drinker:
                context = {'error': 'You cannot delete this image, You donnot own this image'}
                return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
                
            document.delete()
        return HttpResponseRedirect('/myapp/browse/')

        
@login_required
def EditImage(request):
        if not request.user.is_authenticated():
                return HrttpResponseRedirect('/login/')
        if request.method == 'GET':
            # Edit image
            img_id = request.GET.get('img_id', False)
            form = EditForm(request.POST)
            try:
                document = Document.objects.filter(pk=img_id)
                if not document[0].owner == request.user.drinker:
                    context = {'extra': 'this image is not yours'}
                    context = {'error': 'You cannot delete this image, You donnot own this image'}
                    return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
            except:
                context = {'error': 'There is no image'}
                return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
            
  
            return render_to_response('editImage.html', {'form': form, 'document': document[0]}, context_instance=RequestContext(request))
            
        if request.method == 'POST':
                form = EditForm(request.POST)
                if form.is_valid():
                        print '####################Edit image VALID'
                        imageId = form.cleaned_data['imageId']
                        document = Document.objects.get(pk=imageId)
                        print "document.description"
                        print document.description                     
                        document.description = form.cleaned_data['description']
                        print "form.cleaned_data['description']"
                        print form.cleaned_data['description']   
                        document.shared = form.cleaned_data['shared']
                        document.save()
                        return HttpResponseRedirect('/myapp/browse/')
                else:
                        print '####################NOT VALID'
                        return HttpResponseRedirect('/myapp/browse/')
        else:
                return HttpResponseRedirect('/myapp/browse/')

                

def BrowseAll(request):
    # Load documents for the list page
    #documents = Document.objects.all()
    page = request.GET.get('p', False)
    print "look here here here here here"
    print page 
    if page == False:
        page = 1
        page = int(page)
    else:
        if page.isdigit():
            page = int(page)
        else:
            page = 1

    if page < 1:
        page = 1
    
    elementsPerPage = 8
    lastElement = page * elementsPerPage
    firstElement = lastElement - elementsPerPage
    
    documents = Document.objects.filter(shared=True).order_by('-id')[firstElement:lastElement]
    
    next = False
    previous = False
    #Check if there are objects in the previous page
    
    try:
        Document.objects.filter(shared=True).order_by('-id')[firstElement-elementsPerPage:lastElement-elementsPerPage]
        previous = True
    except :
        previous = False
   
    try:
        Document.objects.filter(shared=True).order_by('-id')[firstElement+elementsPerPage:lastElement+elementsPerPage]
        next = True
    except :
        next = False
    
        
    # Render list page with the documents and the form
    return render_to_response(
        'browseAll.html',
        {'documents': documents, 'next': next, 'previous': previous, 'npage': page+1, 'ppage': page-1},
        context_instance=RequestContext(request)
    )
    

@login_required
def ChooseFX(request):
        if not request.user.is_authenticated():
                return HrttpResponseRedirect('/login/')
        if request.method == 'GET':
            # Edit image
            img_id = request.GET.get('img_id', False)
            form = EditForm(request.POST)
            chooseFXForm = ChooseFXForm(request.POST)
            
            try:
                document = Document.objects.filter(pk=img_id)
                documentsFX = Document.objects.filter(fx=True)
                if not document[0].owner == request.user.drinker:
                    context = {'extra': 'this image is not yours'}
                    context = {'error': 'You cannot delete this image, You donnot own this image'}
                    return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
            except:
                context = {'error': 'There is no image'}
                return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
            
  
            return render_to_response('chooseFX.html', {'form': form, 'chooseFXForm': chooseFXForm, 'document': document[0], 'documentsFX': documentsFX}, context_instance=RequestContext(request))
            
        if request.method == 'POST':
                chooseFXForm = ChooseFXForm(request.POST)
                form = EditForm(request.POST)
                if not chooseFXForm.is_valid():
                    print '####################chooseFXForm NOT VALID'
                    context = {'error': 'The image URL is not acceptable'}
                    return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
                    
                if form.is_valid():
                        print '####################chooseFXForm VALID'
                        imageId = form.cleaned_data['imageId']
                        document = Document.objects.get(pk=imageId)
                        document_URL = document.docfile.url
                        documentFX_URL = chooseFXForm.cleaned_data['FX_URL']
                        imageEffects = ImageEffects(document_URL,documentFX_URL)
                        imageEffects.applyFX()
                        return HttpResponseRedirect('/myapp/browse/')
                else:
                        print '####################NOT VALID'
                        context = {'error': 'Form'}
                        return render_to_response('errorPage.html', context, context_instance=RequestContext(request))
        else:
                return HttpResponseRedirect('/myapp/browse/')

                
def getSize (documents):
    usedSpace = 0
    for document in documents:
        usedSpace += document.docfile.size
    return (usedSpace / (1024*1024))

