# /whatsnews/blues/auth/models.py


from functools import wraps
from flask import redirect, request, session, url_for


class UserAuth:
    
    def login(self, user):
        session['user'] = user
        print( f"### user_auth.login('{user.username}')")
    
    def logout(self):
        if 'user' in session:
            print( f"### user_auth.logout('{session['user'].username}')")
        else:
            print( f"### user_auth.logout(): no-op")
        session.pop('user', None)

    def is_logged_in(self):
        return 'user' in session
    
    def get_attr(self, attr_name):
        return getattr(session['user'], attr_name)


    #
    # Guards
    #


    # def ensure_logged_in(self, func):
    #     @wraps(func)
    #     def decorated_func(*args, **kwargs):
    #         if user_auth.is_logged_in():
    #             return func(*args, **kwargs)
    #         else:
    #             return redirect( url_for('auth.login', next=request.url) )
            
    #     return decorated_func
    

    # def ensure_doc_author_or_admin(self, func):
    #     @wraps(func)
    #     def decorated_func(*args, **kwargs):
    #         if not 'user' in session:
    #             return redirect( url_for('auth.login', next=request.url) )
    #         elif session['user'].role == RoleEnum.ADMIN:
    #             return func(*args, **kwargs)
            
    #         post = Document.get_by_id( request.view_args['id'] )
    #         if session['user'].id == post.author_id:
    #             return func(*args, **kwargs)
            
    #         abort(403)
            
    #     return decorated_func


    # def ensure_role_at_least(self, reqd_role):
    #     def actual_decorator(func):
    #         @wraps(func)
    #         def decorated_func(*args, **kwargs):
    #             if not 'user' in session:
    #                 return redirect( url_for('auth.login', next=request.url) )
    #             elif session['user'].role.value < reqd_role.value:
    #                 abort(403)
    #             else:
    #                 return func(*args, **kwargs)
    #         return decorated_func
            
    #     return actual_decorator


user_auth = UserAuth()