from flask import render_template


def page_not_found(e):
    return render_template("base/error.html", 
                           code=404, 
                           title="Page not found!", 
                           description="The current URL doesn't return anything...", 
                           comment="You can go back to the website by using the top navbar"
        ), 404

def unauthorized(e):
    return render_template("base/error.html", 
                           code=401, 
                           title="Unauthorized!", 
                           description="You are not authorized to access this page...", 
                           comment="You can log yourself by using the top navbar"
        ), 401