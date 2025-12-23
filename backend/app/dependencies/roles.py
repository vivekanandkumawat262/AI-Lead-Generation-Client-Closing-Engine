from fastapi import Depends, HTTPException, status
from app.dependencies.auth import get_current_user
from app.core.roles import Role

def require_role(required_roles: list[Role]):
    def role_checker(user=Depends(get_current_user)):
        if user.get("role") not in [role.value for role in required_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        return user
    return role_checker
