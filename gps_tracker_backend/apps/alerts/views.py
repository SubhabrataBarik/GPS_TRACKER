from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models import Child

from .models import Alert, Geofence
from .serializers import AlertSerializer, GeofenceSerializer


# =========================================================
# ALERT LIST VIEW  (last 50 alerts for the parent)
# =========================================================

class AlertListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        alerts = Alert.objects.filter(
            child__parent=request.user,
        ).select_related("child")[:50]

        serializer = AlertSerializer(alerts, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# =========================================================
# GEOFENCE LIST / CREATE VIEW  (per child)
# =========================================================

class GeofenceListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, child_id):

        child = get_object_or_404(Child, id=child_id, parent=request.user)

        geofences = child.geofences.all()

        serializer = GeofenceSerializer(geofences, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, child_id):

        child = get_object_or_404(Child, id=child_id, parent=request.user)

        serializer = GeofenceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(child=child)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# =========================================================
# GEOFENCE DETAIL VIEW  (retrieve / update / delete)
# =========================================================

class GeofenceDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, geofence_id, user):
        return get_object_or_404(Geofence, id=geofence_id, child__parent=user)

    def get(self, request, geofence_id):

        geofence = self.get_object(geofence_id, request.user)

        serializer = GeofenceSerializer(geofence)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, geofence_id):

        geofence = self.get_object(geofence_id, request.user)

        serializer = GeofenceSerializer(geofence, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, geofence_id):

        geofence = self.get_object(geofence_id, request.user)
        geofence.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
