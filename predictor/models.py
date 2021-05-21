from predictor import db
import os


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











