from flask_app import app
from flask_app.models.achievement import Achievement
from flask import render_template, redirect, request, session

####### Visible Routes #######


@app.route('/achievement/create')
def create_achievement():
    if 'user_id' not in session:
        return redirect('/landing')
    return render_template('add_achv.html')


@app.route('/achievement/edit/<int:id>')
def edit_achievement_page(id):
    if 'user_id' not in session:
        redirect('/landing')
    data = {
        "id": id
    }
    return render_template('edit_achv.html', this_achievement=Achievement.get_achievement_by_id(data))


@app.route('/achievement/view/<int:id>')
def view_achievement_page(id):
    if 'user_id' not in session:
        redirect('/landing')
    id_data = {
        "id": id
    }
    return render_template('view_achv.html', this_achievement=Achievement.get_achievement_by_id(id_data))


####### Hidden Routes #######
@app.route('/process/create_achievement', methods=['POST'])
def process_create_achievement():
    if Achievement.validate_add_achievement(request.form) == False:
        return redirect('/achievement/create')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "points": request.form['points'],
        "id": session['user_id'],
    }
    Achievement.add_achievement_to_db(data)
    return redirect('/dashboard')


@app.route('/process/edit_achievement/<int:id>', methods=['POST'])
def edit_achievement(id):
    if Achievement.validate_add_achievement(request.form) == False:
        return redirect('/achievement/edit/<int:id>')
    data = {
        "id": id,
        "name": request.form['name'],
        "description": request.form['description'],
        "points": request.form['points'],
    }
    Achievement.update_achievement_by_id(data)
    return redirect('/dashboard')


@app.route('/process/view_achievement/<int:id>')
def view_achievement():
    pass


@app.route('/achievement/delete/<int:id>')
def delete_route(id):
    data = {
        "id": id
    }
    Achievement.delete_achievement_by_id(data)
    return redirect('/dashboard')


@app.route('/logout')
def logout_user():
    session.clear()
    return redirect('/')
