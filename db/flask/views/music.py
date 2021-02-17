from flask import Blueprint, session, redirect, render_template, request, abort, g, redirect
from models import Authentication, Database, PageDetails, General
from functools import wraps

music = Blueprint("music", __name__)


def check_is_admin():
    def _check_is_admin(f):
        @wraps(f)
        def __check_is_admin(*args, **kwargs):
            result = f(*args, **kwargs)
            if not Authentication(session).is_admin():
                abort(401)
            return result

        return __check_is_admin

    return _check_is_admin


@music.route("/musics")
@music.route("/music")
def musics_index():
    ***REMOVED*** The Music page ***REMOVED***
    posts_per_page = 10
    page = request.args.get("page")
    posts = Database().get_all_musics_data_from_db()
    last_page = len(posts)//posts_per_page
    if len(posts) - last_page*posts_per_page > 0:
        last_page+=1
    if page is None:
        page = 1
    else:
        try:
            page = int(page)
        except ValueError:
            page = 1
    if page<1:
        return redirect("?page=1")
    limited_posts = (posts[(page-1)*posts_per_page:page*posts_per_page])
    if limited_posts == [] and page!=1:
        return redirect("?page={}".format(last_page))
    return render_template(
        "music/music_posts.html",
        details=PageDetails(session).index_data(),
        posts=limited_posts,
        now_page=page,
        last_page=last_page,
        pagination=General().pagination_designer(page,last_page)
    )



@music.route("/rekord")
def rekord():
    return render_template("music/rekord.html")
