"""
API file for result app

consists of the result list and add api
"""

from django.utils import timezone

from rest_framework import status, mixins
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets

from login.models import UserProfile
from discussion.models import Tag
from schedule.models import Schedule
from schedule.serializers import ScheduleSerializer, ScheduleCreateSerializer
from schedule import functions

from UCP.constants import result

class ScheduleViewSet(viewsets.ViewSet):
    """
    Viewset for creating and listing results
    """
    
    authentication_classes = (TokenAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    
    @list_route(methods=['POST'])
    def add(self,request):
        """
        Add a new Schedule
        ---
        parameters:
            - name : schedule_file
              type : file
            - name : tags
              type : string
              description : tag ids seperated by commas
        """
        response = {}
        serializer = ScheduleCreateSerializer(data = request.POST)
        if serializer.is_valid():
            teacher = UserProfile.objects.get(user = request.user)
            schedule = serializer.save(teacher = teacher)
            tag_ids = [ int(t) if t else 0 for t in request.POST.get("tags", "").split(",") ]
            tags = Tag.objects.filter(pk__in = tag_ids)
            schedule.tags = tags
            schedule.save()
            serializer = ScheduleSerializer(schedule)
            response["result"] = result.RESULT_SUCCESS
            response["data"] = serializer.data
        else:
            response["result"] = result.RESULT_FAILURE
            response["errors"] = serializer.errors
        return Response(response, status=status.HTTP_200_OK)
    
    @list_route()
    def get(self, request):
        """
        Get a list of all Schedules
        ---
        # YAML
        
        parameters:
            -   name: page
                description: page no. of the results
                type: string
                paramType: query
        """
        
        response = functions.get_schedules(request)

        return Response(response, status=status.HTTP_200_OK)
        
    
    def get_serializer_class(self):
        if self.action == "add":
            return ScheduleCreateSerializer
        else:
            return ScheduleSerializer