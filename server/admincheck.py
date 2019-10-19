# from django.shortcuts import HttpResponse, redirect
# from django.utils.deprecation import MiddlewareMixin
#
#
# class LoginAuth(MiddlewareMixin):
#
#     def process_request(self, request):
#
#         return_url = request.path
#
#         if return_url.startswith("/server") and not return_url.startswith("/server/login"):
#
#             if not request.session.get("admin", ""):
#                 return redirect("/server/login")



from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin
class LoginAuth(MiddlewareMixin):
    def process_request(self, request):
        url = request.path
        if url.startswith("/server") and not url==("/server/login/"):
            if  request.session.get('admin'):
                pass
            else:
                if url == "/server/loginHandler/" and request.POST.get("password") != None:
                    pass
                else:
                    return redirect("/server/login/")
