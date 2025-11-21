from accounts.models import Invitation

def invite_count(request):
    if request.user.is_authenticated:
        return {
            "invite_count": Invitation.objects.filter(
                receiver=request.user,
                status="pending"
            ).count()
        }
    return {"invite_count": 0}
