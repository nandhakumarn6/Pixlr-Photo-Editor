from main.models import Directory
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from .forms import ImageForm
from django.http import JsonResponse
from django.contrib import messages
import os

class EditAPI(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, dir, format=None):
        if(request.POST.get('directory_name') == "home"):
            return JsonResponse("Image Cannot Be Named As Home", safe=False)

        try:
            image = Directory.objects.get(pk=dir)
            if(image.user_id_id != request.user.id):
                return JsonResponse("You Don't Have Permissions to that Image File", safe=False) 
        except Directory.DoesNotExist:
            return JsonResponse("Image File Does Not Exist", safe=False)
            
        if image.is_directory == 1:
            return JsonResponse("Image File Cannot Be A DIR", safe=False)

        print(request.FILES)
        print(request.POST)
        form = ImageForm(request.POST, request.FILES, instance=image)
        print(form) 
        if (form.is_valid()):
            form.save()
        else:
            return JsonResponse("File Is Not Valid", safe=False)
        return JsonResponse("Image Updated Successfully", safe=False)



class DirectoryAPI(APIView):

    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    #Upload Images############
    def post(self, request ,dir, format=None):

        if(request.POST.get('directory_name') == ""):
            payload={
                "info":"Image Name Cannot Be Empty",
            }
            return JsonResponse(payload, safe=False)

        if(request.POST.get('directory_name') == "home"):
            payload={
                "info":"Image Cannot Be Named As Home",
            }
            return JsonResponse(payload, safe=False)

        try:
            parent_dir = Directory.objects.get(pk=dir)
            if(parent_dir.user_id_id != request.user.id):
                payload={
                    "info":"You Don't Have Permissions to that DIR",
                }
                return JsonResponse(payload, safe=False)
        except Directory.DoesNotExist:
            parent_dir = None

        if parent_dir is None:
            payload={
                "info":"Parent DIR Does Not Exist",
            }
            return JsonResponse(payload, safe=False)
        if parent_dir.is_directory == 0:
            payload={
                "info":"Parent DIR Cannot Be A File",
            }
            return JsonResponse(payload, safe=False)

        form = ImageForm(request.POST, request.FILES)

        if (form.is_valid()):
            form = form.save(commit=False)
            form.user_id_id = request.user.id
            form.parent_directory = parent_dir
            form.is_directory = 0
            form.save()
            payload = "1"
        else:
            payload={
                "info":"File Is Not Valid",
            }
            return JsonResponse(payload, safe=False)
        payload={
                "info":"Image Uploaded Successfully",
                "dir" : form.pk,
                "directory_name" : form.directory_name,
            }
        return JsonResponse(payload, safe=False)

    

    #Create Folders#############
    def put(self, request, dir, format=None):

        if(request.data['name'] == ""):
            payload={
                "info":"DIR Name Cannot Be Empty",
            }
            return JsonResponse(payload, safe=False)
 
        if(request.data['name'] == "home"):
            payload={
                "info":"DIR Cannot Be Named As Home",
            }
            return JsonResponse(payload, safe=False)
        try:
            parent_dir = Directory.objects.get(pk=dir)
            if(parent_dir.user_id_id != request.user.id):
                payload={
                    "info":"You Don't Have Permissions to that DIR",
                }
                return JsonResponse(payload, safe=False)
        except Directory.DoesNotExist:
            parent_dir = None

        if parent_dir is None:
            payload={
                "info":"Parent DIR Does Not Exist",
            }
            return JsonResponse(payload, safe=False)
        if parent_dir.is_directory == 0:
            payload={
                "info":"Parent DIR Cannot Be A File",
            }
            return JsonResponse(payload, safe=False)
        existing_childs = Directory.objects.filter(parent_directory=parent_dir.pk)
        for child in existing_childs:
            if(str(child.directory_name).lower() == str(request.data['name']).lower()):
                payload={
                    "info":"Cannot Have Duplicate Folder Names",
                }
                return JsonResponse(payload, safe=False)
    
        new_dir = Directory(user_id=request.user, directory_name=request.data['name'])
        try:
            new_dir.parent_directory = parent_dir
            new_dir.save()
        except:
            payload={
                "info":"There Was A Problem!",
            }
            return JsonResponse(payload, safe=False)

        payload={
            "info":"Folder Created Sucessfully",
            "dir" : new_dir.pk,
            "directory_name" : new_dir.directory_name,
        }
        return JsonResponse(payload, safe=False)
            

    def delete(self, request, dir, format=None):
        try:
            delete_dir = Directory.objects.get(pk=dir)
            if(delete_dir.user_id_id != request.user.id):
                return JsonResponse("You Don't Have Permissions to that DIR", safe=False) 
        except Directory.DoesNotExist:
            delete_dir = None

        if delete_dir is None:
            return JsonResponse("Parent DIR Does Not Exist", safe=False) 
        if delete_dir.directory_name == "home":
            return JsonResponse("Cannot Delete Home DIR", safe=False) 

        if delete_dir.is_directory == False:
            delete_dir.delete()
        else:
            nodes_to_delete = get_all_child_nodes(delete_dir.id)
            for node in nodes_to_delete:
                Directory.objects.get(pk=node).delete()
                
        return JsonResponse("Folder Deleted Successfully", safe=False)



#BFS traversal for getting all nodes to delete
def get_all_child_nodes(node):
    visited = []   # List to keep track of nodes to be deleted!!.
    queue = []     #Initialize a queue
    visited.append(node)
    queue.append(node)

    while queue:
        s = queue.pop(0)

        for neighbour in Directory.objects.filter(parent_directory=s):
            if neighbour.pk not in visited:
                visited.append(neighbour.pk)
                queue.append(neighbour.pk)
                node = neighbour.pk

    visited.reverse()
    return visited
