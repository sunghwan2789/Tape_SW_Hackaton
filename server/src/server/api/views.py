import json
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import TemporaryUploadedFile, UploadedFile
from django.http.response import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import serializers, viewsets
from rest_framework.parsers import FormParser, MultiPartParser

from .models import *

# Create your views here.


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = [
            "id",
            "user",
            "title",
            "filepath",
            "filterpath",
            "pub_date",
            "thumbnail",
            "description",
            "filters",
        ]
        depth = 1

    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.profile.name


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.order_by("-id")
    serializer_class = VideoSerializer
    parser_classes = (
        MultiPartParser,
        FormParser,
    )
    read_only_fields = ("user",)

    def get_queryset(self):
        queryset = Video.objects.order_by("-id")

        q = self.request.query_params.get("q", None)
        if q is not None:
            queryset = queryset.filter(title__contains=q) | queryset.filter(
                description__contains=q
            )

        return queryset

    def perform_create(self, serializer):
        """
        1. upload된 영상 파일을 os tape input file로 전달.
        2. os 모듈로 main.py 실행.
        3. upload 영상 filtering.
        4. filtering된 영상 db에 가져와 저장.
        5. app 화면에는 filtering된 영상 업로드.
        """
        upload_file: UploadedFile = self.request.data.get("filepath")

        with tempfile.NamedTemporaryFile("wb") as temp_uploaded_video:
            # copy raw video into tape input directory
            for chunk in upload_file.chunks():
                temp_uploaded_video.file.write(chunk)

            # 상대 경로이기 때문에 cd로 해당 루트로 들어가서 실행.
            # system 첫 호출시 위치는 root.
            completed_subprocess = subprocess.run(
                ["python", "main.py", temp_uploaded_video.name],
                cwd=settings.TAPE_ROOT,
                stdout=subprocess.PIPE,
            )
            completed_subprocess.check_returncode()

            tape_result = json.loads(completed_subprocess.stdout)

        result_filename = "filter_" + upload_file.name
        thumnail_filename = "filter_" + upload_file.name + ".jpg"

        # copy media directory
        fs = FileSystemStorage()
        result_filename = fs.save(
            result_filename, open(tape_result["filter_video"], "rb")
        )
        fs = FileSystemStorage()
        thumnail_filename = fs.save(
            thumnail_filename, open(tape_result["thumbnail"], "rb")
        )
        fs = FileSystemStorage()
        upload_filename = fs.save(None, upload_file)

        # fix permissions
        os.system('chown 1000:1000 -R "' + settings.MEDIA_ROOT + '"')
        os.system('chmod +r -R "' + settings.MEDIA_ROOT + '"')

        video = serializer.save(
            user=User.objects.get(pk=self.request.data.get("user", 1)),
            title=self.request.data.get("title"),
            filepath=upload_filename,
            description=self.request.data.get("description"),
            filterpath=result_filename,
            thumbnail=thumnail_filename,
        )

        FilterSection.objects.bulk_create(
            [FilterSection(video=video, **i) for i in tape_result["filter_sections"]]
        )


@csrf_exempt
def login(request):
    try:
        user = auth.authenticate(
            request, username=request.POST["phone"], password=request.POST["password"]
        )
        if user is not None:
            auth.login(request, user)
            return JsonResponse({"id": user.id,})
        raise ValueError("user not found or incorrect password!")
    except Exception as ex:
        return JsonResponse({"error": str(ex),})


@csrf_exempt
def signup(request):
    try:
        user = User.objects.create_user(
            username=request.POST["phone"], password=request.POST["password"]
        )
        user.profile.name = request.POST["name"]
        user.profile.passwordQuestion = request.POST["password_question"]
        user.profile.passwordQuestionAnswer = request.POST["password_question_answer"]
        auth.login(request, user)
        return JsonResponse({"id": user.id,})
    except Exception as ex:
        return JsonResponse({"error": str(ex),})
