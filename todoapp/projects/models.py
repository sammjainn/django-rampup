from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Project(models.Model):
    """
        Needed fields
        - members (m2m field to CustomUser; create through table and enforce unique constraint for user and project)
        - name (max_length=100)
        - max_members (positive int)
        - status (choice field integer type :- 0(To be started)/1(In progress)/2(Completed), with default value been 0)

        Add string representation for this model with project name.
    """

    members = models.ManyToManyField(User, through='ProjectMember')
    name = models.CharField(max_length=100, blank=True)
    max_members = models.PositiveIntegerField(default=0)

    FIRST = 0
    SECOND = 1
    THIRD = 2
    STATUS_CHOICES = (
        (FIRST, 'To be started'),
        (SECOND, 'In progress'),
        (THIRD, 'Completed'),
    )

    status = models.IntegerField(choices=STATUS_CHOICES, default=FIRST)

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    """
    Needed fields
    - project (fk to Project model)
    - member (fk to User model - use AUTH_USER_MODEL from settings)
    - Add unique constraints

    Add string representation for this model with project name and user email/first name.
    """

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.member.first_name + ' ' + self.member.email

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['project', 'member'], name='membership')]
