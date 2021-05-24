from predictor import db, login_manager
from predictor import bcrypt
from flask_login import UserMixin
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)



class Mould(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    fill_time = db.Column(db.Integer(), nullable=False)
    injection_pres = db.Column(db.Integer(), nullable=False)
    holding_pres = db.Column(db.Integer(), nullable=False)
    holding_time = db.Column(db.Integer(), nullable=False)
    cooling_time = db.Column(db.Integer(), nullable=False)

    mould_temp = db.Column(db.Integer(), nullable=False)
    clamp_force = db.Column(db.Integer(), nullable=False)
    shot_weight = db.Column(db.Float(), nullable=False)

    mould_SA = db.Column(db.Float(), nullable=False)
    mould_vol = db.Column(db.Float(), nullable=False)
    cavity_SA = db.Column(db.Float(), nullable=False)
    cavity_vol = db.Column(db.Float(), nullable=False)

    melt_temp = db.Column(db.Float(), nullable=False)
    mat_density = db.Column(db.Float(), nullable=False)
    mat_GF = db.Column(db.Integer(), nullable=False)
    mat_MMFR = db.Column(db.Float(), nullable=False)

    part_weight = db.Column(db.Float(), nullable=False)

    def delete_self(self):
        db.session.delete(self)
        db.session.commit()

    def add_self(self):
        db.session.add(self)
        db.session.commit()


class DBModelMetrics(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    absolute_mean_error = db.Column(db.Float(), nullable=True)
    model_score = db.Column(db.Float(), nullable=True)
    max_error = db.Column(db.Float(), nullable=True)

    def save(self):
        DBModelMetrics.query.filter_by(id=1).delete()
        db.session.add(self)
        db.session.commit()


def initDb():
    if not os.path.exists('predictor/data.db'):
        db.create_all()
        db.session.commit()


initDb()











