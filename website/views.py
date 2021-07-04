from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Note, db
import json

views = Blueprint('views', __name__)

@views.route("/", methods=['GET', 'POST'])
@login_required
def index():
    if request.method == "POST":
        data = request.form['note']

        if len(data) < 1:
            flash('Note is too short!', category="error")
        else:
            new_note = Note(data=data, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added", category="success")
    return render_template('index.html', user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note['noteId']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/update-note/<int:id>', methods=["GET", "POST"])
def update_note(id):
    note = Note.query.get_or_404(id)
    if request.method == "POST":
        data = request.form['note']
        if len(data) < 1:
            flash('Note is too short!', category="error")
        else:
            note.data = data
            db.session.commit()
            return redirect(url_for('views.index'))
    return render_template("update.html", note=note, user=current_user)
