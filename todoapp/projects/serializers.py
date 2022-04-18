from django.contrib.auth import get_user_model
from django.contrib.postgres.aggregates import *
from rest_framework import serializers
from users.serializers import UserTodosBaseSerializer
from projects.models import Project

User = get_user_model()

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


class AddMemberSerializer(serializers.ModelSerializer):
    '''
    Serializer for adding members to Project
    '''
    user_ids = serializers.ListField(write_only=True)
    logs = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['user_ids', 'logs']

    def validate(self, data):
        project_id = self.context['view'].kwargs.get('id')
        project = Project.objects.filter(id=project_id)

        if not project.exists():
            raise serializers.ValidationError("No such project")
        return data

    def update(self, project, validated_data):
        project_id = project.id
        user_ids = self.context['request'].data.get('user_ids')

        response = {}
        project_max_members = project.max_members
        project_member_count = project.members.count()

        user_projects = User.objects.filter(id__in=user_ids).annotate(
            projects=ArrayAgg('project__id')).values('id', 'projects')

        user_projects = {u['id']: u['projects'] for u in user_projects}

        limit_reached = 0
        users_to_be_added = []

        for id in user_ids:
            if not user_projects.__contains__(id):
                response[id] = "No such user"
                continue

            if project_member_count >= project_max_members:
                response[id] = "Max member limit for project reached"
                limit_reached = 1
                break

            user_project_count = len(user_projects[id])
            if user_project_count >= 2:
                response[id] = "Cannot add as User is a member in two projects"
                continue

            if project_id in user_projects[id]:
                response[id] = "User is already a Member"
                continue

            users_to_be_added.append(id)
            response[id] = "Member added Successfully"
            project_member_count += 1

        project.members.add(*users_to_be_added)

        if limit_reached == 1:
            for id in user_ids:
                if id not in response:
                    response[id] = "Max member limit for project reached"

        validated_data['logs'] = response

        return validated_data

    def get_logs(self, data):
        return data['logs']


class RemoveMemberSerializer(serializers.ModelSerializer):
    '''
    Serializer for removing members from Project
    '''
    user_ids = serializers.ListField(write_only=True)
    logs = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['user_ids', 'logs']

    def validate(self, data):
        project_id = self.context['view'].kwargs.get('id')
        project = Project.objects.filter(id=project_id)

        if not project.exists():
            raise serializers.ValidationError("No such project")
        return data

    def update(self, project, validated_data):
        user_ids = self.context['request'].data.get('user_ids')

        response = {}
        project_member_count = project.count

        project_members = list(project.members.values('id'))

        project_members = [member['id'] for member in project_members]

        users = User.objects.filter(id__in=user_ids).values('id')
        users = [u['id'] for u in users]

        limit_reached = 0
        users_to_be_removed = []

        for id in user_ids:
            if id not in users:
                response[id] = "No such user"
                continue

            if project_member_count == 0:
                response[id] = "Project has no more members"
                limit_reached = 1
                break

            if id not in project_members:
                response[id] = "Cannot remove as User is not a Member"
                continue

            users_to_be_removed.append(id)
            response[id] = "Member removed Successfully"
            project_member_count -= 1

        project.members.remove(*users_to_be_removed)

        if limit_reached == 1:
            for id in user_ids:
                if id not in response:
                    response[id] = "Project has no more members"

        validated_data['logs'] = response

        return validated_data

    def get_logs(self, data):
        return data['logs']
