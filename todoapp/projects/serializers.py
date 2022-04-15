from rest_framework import serializers

from projects.models import Project
from users.serializers import UserTodosBaseSerializer

# Serializers for the Project model


class BaseProjectSerializer(serializers.ModelSerializer):
    '''
    Serializer for Project ID
    '''
    class Meta:
        model = Project
        fields = ('id', )


class ProjectNameSerializer(serializers.ModelSerializer):
    '''
    Serializer for Project ID and details
    '''
    project_name = serializers.CharField(source='name')
    done = serializers.BooleanField()

    class Meta:
        model = Project
        fields = ('project_name', 'done', 'max_members', )


class ProjectReportSerializer(serializers.ModelSerializer):
    '''
    Serializer for all members of Project
    '''
    project_title = serializers.CharField(source='name')
    report = UserTodosBaseSerializer(source='member_list', many=True)

    class Meta:
        model = Project
        fields = ('project_title', 'report', )


class ProjectDetailSerializer(BaseProjectSerializer):
    '''
    Serializer for Project status and member count info
    '''
    existing_member_count = serializers.IntegerField()
    status = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = BaseProjectSerializer.Meta.fields + \
            ('name', 'status', 'existing_member_count', 'max_members', )

    def get_status(self, obj):
        '''
        Readable name for status choice
        '''
        return obj.get_status_display()
