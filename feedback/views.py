from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import QRCode, QRCodeFeedback, FormFeedback, SocialMediaFeedback, Alert
from .serializers import QRCodeFeedbackSerializer, FormFeedbackSerializer, QRCodeSerializer, SocialMediaFeedbackSerializer, AlertSerializer
import pandas as pd
import qrcode
from django.http import HttpResponse
from feedback.models import QRCode
from TextSentimentAnalysis.SocialMediaFeedback_scripts import analyze_multilingual_sentiment
from rest_framework.views import APIView


class QRCodeFeedbackViewSet(viewsets.ModelViewSet):
    queryset = QRCodeFeedback.objects.all()
    serializer_class = QRCodeFeedbackSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        qr_code = self.request.query_params.get('qr_code')
        if qr_code:
            queryset = queryset.filter(qr_code__code=qr_code)
        return queryset
    
    def perform_create(self, serializer):
        """Override perform_create to analyze sentiment and language before saving."""
        content = serializer.validated_data.get('content')  # Get content from request data
        language, sentiment = analyze_multilingual_sentiment(content)  # Analyze content
        feedback = serializer.save(sentiment=sentiment, langue=language)

    def perform_update(self, serializer):
        """Override perform_update to analyze sentiment and language before updating."""
        content = serializer.validated_data.get('content')  # Get content from request data
        language, sentiment = analyze_multilingual_sentiment(content)  # Analyze content
        serializer.save(sentiment=sentiment, langue=language)

class FormFeedbackViewSet(viewsets.ModelViewSet):
    queryset = FormFeedback.objects.all()
    serializer_class = FormFeedbackSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        service = self.request.query_params.get('service')
        if service:
            queryset = queryset.filter(service=service)
        return queryset

    def perform_create(self, serializer):
        """Override perform_create to analyze sentiment and language before saving."""
        content = serializer.validated_data.get('content')  # Get content from request data
        language, sentiment = analyze_multilingual_sentiment(content)  # Analyze content
        serializer.save(sentiment=sentiment, langue=language)

    def perform_update(self, serializer):
        """Override perform_update to analyze sentiment and language before updating."""
        content = serializer.validated_data.get('content')  # Get content from request data
        language, sentiment = analyze_multilingual_sentiment(content)  # Analyze content
        serializer.save(sentiment=sentiment, langue=language)  # Update fields with sentiment and langue



class SocialMediaFeedbackViewSet(viewsets.ViewSet):
    """
    A ViewSet to manage SocialMediaFeedback entries, including importing from a dataset.
    """

    def create(self, request):
        """
        Handle POST requests to import data from a CSV file into the SocialMediaFeedback model.
        """
        try:
            # Specify your dataset path
            file_path = r'/home/th3_l4dy/Documents/Hackthon/InovPOst/auth_drf/TextSentimentAnalyst/data/analyzed_multilingual_comments.csv'  # Adjust as needed
            df = pd.read_csv(file_path)

            # Create model instances for each row
            feedback_entries = [
                SocialMediaFeedback(
                    username=row['profileName'],
                    content=row['cleaned_comment'],
                    sentiment=row['sentiment'],
                    langue=row['language']
                )
                for _, row in df.iterrows()
            ]

            # Bulk create entries
            SocialMediaFeedback.objects.bulk_create(feedback_entries, ignore_conflicts=True)

            return Response({'message': 'Data imported successfully.'}, status=status.HTTP_201_CREATED)

        except FileNotFoundError:
            return Response({'error': 'CSV file not found.'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def list(self, request):
        """
        Handle GET requests to retrieve all SocialMediaFeedback entries.
        """
        feedbacks = SocialMediaFeedback.objects.all()
        serializer = SocialMediaFeedbackSerializer(feedbacks, many=True)        
        return Response(serializer.data)   

class QRCodeViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for viewing and editing QRCode instances.
    """
    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer


def generate_qr_code_image(request, code):
    try:
        # Get the QRCode instance
        qr_instance = QRCode.objects.get(code=code)
        
        # Generate QR code image
        qr = qrcode.make(qr_instance.code)
        
        # Create an HTTP response with the image
        response = HttpResponse(content_type="image/png")
        qr.save(response, "PNG")
        return response
    except QRCode.DoesNotExist:
        return HttpResponse("QR Code not found", status=404)
    

# stats*************
class QRCodeFeedbackStats(APIView):
    def get(self, request, *args, **kwargs):
        feedback_stats = {
            "positive": QRCodeFeedback.objects.filter(sentiment="positive").count(),
            "neutral": QRCodeFeedback.objects.filter(sentiment="neutral").count(),
            "negative": QRCodeFeedback.objects.filter(sentiment="negative").count(),
        }
        return Response(feedback_stats)
class FormFeedbackStats(APIView):
    def get(self, request, *args, **kwargs):
        feedback_stats = {
            "positive": FormFeedback.objects.filter(sentiment="positive").count(),
            "neutral": FormFeedback.objects.filter(sentiment="neutral").count(),
            "negative": FormFeedback.objects.filter(sentiment="negative").count(),
        }
        return Response(feedback_stats)
class SocialMediaFeedbackStats(APIView):
    def get(self, request, *args, **kwargs):
        feedback_stats = {
            "positive": SocialMediaFeedback.objects.filter(sentiment="positive").count(),
            "neutral": SocialMediaFeedback.objects.filter(sentiment="neutral").count(),
            "negative": SocialMediaFeedback.objects.filter(sentiment="negative").count(),
        }
        return Response(feedback_stats)
    
class AllFeedbackStats(APIView):
    def get(self, request, *args, **kwargs):
        stats = {
            "positive": (
                QRCodeFeedback.objects.filter(sentiment="positive").count()
                + FormFeedback.objects.filter(sentiment="positive").count()
                + SocialMediaFeedback.objects.filter(sentiment="positive").count()
            ),
            "neutral": (
                QRCodeFeedback.objects.filter(sentiment="neutral").count()
                + FormFeedback.objects.filter(sentiment="neutral").count()
                + SocialMediaFeedback.objects.filter(sentiment="neutral").count()
            ),
            "negative": (
                QRCodeFeedback.objects.filter(sentiment="negative").count()
                + FormFeedback.objects.filter(sentiment="negative").count()
                + SocialMediaFeedback.objects.filter(sentiment="negative").count()
            ),
        }
        return Response(stats)

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer


