# """View module for handling requests about park areas"""
# from django.http import HttpResponseServerError
# from rest_framework.viewsets import ViewSet
# from rest_framework.response import Response
# from rest_framework import serializers
# from rest_framework import status
# from kennywoodapi.models import ParkArea


# class ParkAreaSerializer(serializers.HyperlinkedModelSerializer):
#     """JSON serializer for park areas

#     Arguments:
#         serializers.HyperlinkedModelSerializer
#     """
#     class Meta:
#         model = ParkArea
#         url = serializers.HyperlinkedIdentityField(
#             view_name='parkarea',
#             lookup_field='id'
#         )
#         fields = ('id', 'url', 'name', 'theme')


# class ParkAreas(ViewSet):
#     """Park Areas for Kennywood Amusement Park"""

#     def retrieve(self, request, pk=None):
#         """Handle GET requests for single park area

#         Returns:
#             Response -- JSON serialized park area instance
#         """
#         try:
#             area = ParkArea.objects.get(pk=pk)
#             serializer = ParkAreaSerializer(area, context={'request': request})
#             return Response(serializer.data)
#         except Exception as ex:
#             return HttpResponseServerError(ex)
            
#     def list(self, request):
#         """Handle GET requests to park areas resource

#         Returns:
#             Response -- JSON serialized list of park areas
#         """
#         areas = ParkArea.objects.all()
#         serializer = ParkAreaSerializer(
#             areas,
#             many=True,
#             context={'request': request}
#         )
#         return Response(serializer.data)

"""Park Areas for Kennywood Amusement Park"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from kennywoodapi.models import ParkArea


class ParkAreaSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for park areas

    Arguments:
        serializers
    """
    class Meta:
        model = ParkArea
        # you are giving the serializer the model to use as a bluprint for the translator to know the structure the translated data should be in
        url = serializers.HyperlinkedIdentityField(
            view_name='parkarea',
            lookup_field='id'
        )
        # here we are specifying which fields from the model we want to be provided in the JSON response
        # these are the only things I'm exposing from this endpoint
        # There is no depth specified here becasue there is no foreign key here. if you specify the depth is shows data as nested. this example is flat
        fields = ('id', 'url', 'name', 'theme')


class ParkAreas(ViewSet):
    """Park Areas for Kennywood Amusement Park"""

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized ParkArea instance
        """
        newarea = ParkArea()
        newarea.name = request.data["name"]
        newarea.theme = request.data["theme"]
        newarea.save()

        serializer = ParkAreaSerializer(newarea, context={'request': request})
        # here you are instantiating the  serializer- you are making an instance. you are also making the serializer available within in the scope of the class
        return Response(serializer.data)
        # Response contains data as a property on serializer, which contains th serialized queryset

    def retrieve(self, request, pk=None):
        """Handle GET requests for single park area

        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            area = ParkArea.objects.get(pk=pk)
            serializer = ParkAreaSerializer(area, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a park area

        Returns:
            Response -- Empty body with 204 status code
        """
        area = ParkArea.objects.get(pk=pk)
        area.name = request.data["name"]
        area.theme = request.data["theme"]
        area.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single park area

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            area = ParkArea.objects.get(pk=pk)
            area.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except ParkArea.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to park areas resource

        Returns:
            Response -- JSON serialized list of park areas
        """
        areas = ParkArea.objects.all()
        serializer = ParkAreaSerializer(
            areas, many=True, context={'request': request})
        return Response(serializer.data)