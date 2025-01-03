from predictor import app, state, db
from flask import render_template, request, redirect, url_for, flash
from predictor.forms import PredictForm, AddEntryForm, DeleteEntryForm, AddEntryCSV, DeleteAllEntries,\
    ExportAllEntries, RetrainModel, HyperTuneModel, GetCSVFormatForm, RegisterForm, LoginForm
from predictor.database import add_from_csv, purge, exportCSV, exportCSVFormat, serverExportCSV, serverExportCSVFormat
from predictor.models import Mould, User
import predictor.machine_learning as ml
import numpy as np
from werkzeug.utils import secure_filename
import os
from flask_login import login_user, logout_user, login_required
import markdown2 as md

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/main-page')
@login_required
def main_page():
    return render_template('main.html')


@app.route('/predict-page', methods=['GET', 'POST'])
@login_required
def predict_page():
    predict_form = PredictForm()
    output = np.zeros(shape=17)
    altOutputs = []
    if request.method == 'POST':
        if predict_form.validate_on_submit():
            output, altOutputs = ml.predict(
                Fill_time_min=predict_form.Fill_time_min.data,
                Fill_time_max=predict_form.Fill_time_max.data,
                Fill_time_res=predict_form.Fill_time_res.data,
                Injection_pres_min=predict_form.Injection_pres_min.data,
                Injection_pres_max=predict_form.Injection_pres_max.data,
                Injection_pres_res=predict_form.Injection_pres_res.data,
                Holding_pres_min=predict_form.Holding_pres_min.data,
                Holding_pres_max=predict_form.Holding_pres_max.data,
                Holding_pres_res=predict_form.Holding_pres_res.data,
                Holding_time_min=predict_form.Holding_time_min.data,
                Holding_time_max=predict_form.Holding_time_max.data,
                Holding_time_res=predict_form.Holding_time_res.data,
                Cooling_time_min=predict_form.Cooling_time_min.data,
                Cooling_time_max=predict_form.Cooling_time_max.data,
                Cooling_time_res=predict_form.Cooling_time_res.data,

                Mould_temp=predict_form.Mould_temp.data,
                Clamp_force=predict_form.Clamp_force.data,
                Shot_Weight=predict_form.Shot_Weight.data,

                Mould_SA=predict_form.Mould_SA.data,
                Mould_vol=predict_form.Mould_vol.data,
                Cavity_SA=predict_form.Cavity_SA.data,
                Cavity_vol=predict_form.Cavity_vol.data,

                Melt_temp=predict_form.Melt_temp.data,
                Mat_density=predict_form.Mat_density.data,
                Mat_GF=predict_form.Mat_GF.data,
                Mat_MMFR=predict_form.Mat_MMFR.data
            )
            print('Results: ', output)
            print('ALT Results: ', altOutputs)
            if not output:
                output = [0.0, 0.0, 0.0, 0.0, 0.0]
                flash('No optimal machine parameters were found for the given constraints', 'error')
                return render_template('predict.html', form=predict_form, output=output, altOutputs=altOutputs)
            else:
                flash('Successfully found optimal parameters', 'Success')
                return render_template('predict.html', form=predict_form, output=output, altOutputs=altOutputs)
        if predict_form.errors != {}:
            flash('Invalid values in Predict Form', category='error')
            return redirect(url_for('predict_page'))
    if request.method == 'GET':
        return render_template('predict.html', form=predict_form, output=output, altOutputs=altOutputs)



@app.route('/model-page', methods=['POST', 'GET'])
@login_required
def model_page():
    ml.init_load_up()
    retrainmodel = RetrainModel()
    hypertunemodel = HyperTuneModel()
    absMeanError = ml.ml_metrics.absolute_mean_error
    modelScore = ml.ml_metrics.modelScore
    maxError = ml.ml_metrics.max_error
    if request.method == 'POST':
        retrain = request.form.get('Retrain-model')
        if retrain:
            ml.retrain()
            flash('Model Retrained Successfully', 'success')
            return redirect(url_for('model_page'))
        retrain = request.form.get('HyperTune-model')
        if retrain:
            flash('Model HyperTuned Successfully', 'success')
            flash('If the model\'s performance has decreased then you need to run the HyperTune utility again', 'info')
            ml.hyperTune()
            return redirect(url_for('model_page'))
    if request.method == 'GET':
        return render_template('model.html',
                               absMeanError=absMeanError,
                               modelScore=modelScore,
                               maxError=maxError,
                               RetrainModel=retrainmodel,
                               HyperTuneModel=hypertunemodel)


app.jinja_env.globals.update(getPredict=ml.getPredict)


@app.route('/database-page', methods=['GET', 'POST'])
@login_required
def database_page():
    addentryform = AddEntryForm()
    addentrycsv = AddEntryCSV()
    deleteentryform = DeleteEntryForm()
    deleteallentries = DeleteAllEntries()
    exportallentries = ExportAllEntries()
    getCSVFormat = GetCSVFormatForm()
    if request.method == "POST":
        # add entry logic
        if addentryform.validate_on_submit():
            entry_to_create = Mould(
                fill_time=addentryform.Fill_time.data,
                injection_pres=addentryform.Injection_pres.data,
                holding_pres=addentryform.Holding_pres.data,
                holding_time=addentryform.Holding_time.data,
                cooling_time=addentryform.Cooling_time.data,
                mould_temp=addentryform.Mould_temp.data,
                clamp_force=addentryform.Clamp_force.data,
                shot_weight=addentryform.Shot_Weight.data,
                mould_SA=addentryform.Mould_SA.data,
                mould_vol=addentryform.Mould_vol.data,
                cavity_SA=addentryform.Cavity_SA.data,
                cavity_vol=addentryform.Cavity_vol.data,
                melt_temp=addentryform.Melt_temp.data,
                mat_density=addentryform.Mat_density.data,
                mat_GF=addentryform.Mat_GF.data,
                mat_MMFR=addentryform.Mat_MMFR.data,
                part_weight=addentryform.Part_weight.data
            )
            entry_to_create.add_self()
            flash('Entry added successfully', 'success')
            return redirect(url_for('database_page'))

        # add entry logic with csv
        if addentrycsv.validate_on_submit():
            filename = secure_filename(addentrycsv.file.data.filename)
            addentrycsv.file.data.save(os.path.join(app.config['UPLOADS'], filename))
            add_from_csv(os.path.join(app.config['UPLOADS'], filename))
            return redirect(url_for('database_page'))

        if getCSVFormat.validate_on_submit() and request.form.get('Get-CSV'):
            getCSV = request.form.get('Get-CSV')
            if state.queryServerState():
                print('sending format')
                results = serverExportCSVFormat()
                return results
            else:
                if getCSV:
                    if exportCSVFormat():
                        flash('format.csv placed on your desktop', 'success')
                        return redirect(url_for('database_page'))
                    else:
                        flash('Error in placing format.csv on your desktop as a file with the same name exists on your desktop', 'error')
                        return redirect(url_for('database_page'))


        # delete entry logic
        if deleteentryform.validate_on_submit():
            deleted_entry = request.form.get('deleted_entry')
            d_entry_object = Mould.query.filter_by(id=deleted_entry).first()
            if d_entry_object:
                d_entry_object.delete_self()
                flash('Entry deleted successfully', 'success')
                return redirect(url_for('database_page'))

        if exportallentries.validate_on_submit() and request.form.get('Export-DB'):
            export_db = request.form.get('Export-DB')
            print('sending database')
            if export_db:
                if state.queryServerState():
                    return serverExportCSV()
                else:
                    if exportCSV():
                        flash('Dataset exported to database.csv on your desktop', 'success')
                        return redirect(url_for('database_page'))
                    else:
                        flash('Dataset could not be exported as Database.csv file already exists on your desktop', 'error')
                        return redirect(url_for('database_page'))

        if deleteallentries.validate_on_submit():
            purge_db = request.form.get('Purge-DB')
            if purge_db:
                purge()
                flash('Dataset erased successfully', 'success')
                return redirect(url_for('database_page'))

        if addentrycsv.file.data and addentrycsv.errors != {}:  # If there are not errors from the validations
            for err_msg in addentrycsv.errors.values():
                flash(err_msg[0], category='error')
            return redirect(url_for('database_page'))

        if addentryform.Fill_time.raw_data and addentryform.errors != {}:  # If there are not errors from the validations
            flash('Invalid Values in New Entry Form', 'error')
            return redirect(url_for('database_page'))


    if request.method == "GET":
        entries = Mould.query.all()
        return render_template(
            'database.html',
            AddEntryForm=addentryform,
            DeleteEntryForm=deleteentryform,
            AddEntryCSV=addentrycsv,
            GetCSVFormatForm=getCSVFormat,
            DeleteAllEntries=deleteallentries,
            ExportAllEntries=exportallentries,
            entries=entries,
            getPredict=ml.getPredict
        )


@app.route('/help-page')
@login_required
def help_page():
    with open('index.md', 'r') as f:
        text = f.read()
        html = md.markdown(text, extras=["fenced-code-blocks","cuddled-lists","header-ids"])
    return render_template('help.html', information = html)


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('main_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('main_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))





