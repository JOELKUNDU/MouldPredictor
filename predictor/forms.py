from flask_wtf import FlaskForm
import os
from wtforms import IntegerField, SubmitField, FloatField, FileField
from wtforms.validators import DataRequired, NumberRange, ValidationError


class PredictForm(FlaskForm):

    Fill_time_min = IntegerField(label='Fill time Min', validators=[DataRequired(message='Please enter a valid input for Minimum Fill Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Fill Time')])
    Fill_time_max = IntegerField(label='Fill time Max', validators=[DataRequired(message='Please enter a valid input for Maximum Fill Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Fill Time')])
    Fill_time_res = IntegerField(label='Fill time Res', validators=[DataRequired(message='Please enter a valid input for Fill Time Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Fill Time Resolution')])

    Injection_pres_min = IntegerField(label='Injection pressure Min', validators=[DataRequired(message='Please enter a valid input for Minimum Injection Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Injection Pressure')])
    Injection_pres_max = IntegerField(label='Injection pressure Max', validators=[DataRequired(message='Please enter a valid input for Maximum Injection Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Injection Pressure')])
    Injection_pres_res = IntegerField(label='Injection pressure Res', validators=[DataRequired(message='Please enter a valid input for Injection Pressure Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Injection Pressure Resolution')])

    Holding_pres_min = IntegerField(label='Holding PressureMin', validators=[DataRequired(message='Please enter a valid input for Minimum Holding Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Holding Pressure')])
    Holding_pres_max = IntegerField(label='Holding PressureMax', validators=[DataRequired(message='Please enter a valid input for Maximum Holding Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Holding Pressure')])
    Holding_pres_res = IntegerField(label='Holding PressureRes', validators=[DataRequired(message='Please enter a valid input for Holding Pressure Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Holding Pressure Resolution')])

    Holding_time_min = IntegerField(label='Holding time Min', validators=[DataRequired(message='Please enter a valid input for Minimum Holding Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Holding Time')])
    Holding_time_max = IntegerField(label='Holding time Max', validators=[DataRequired(message='Please enter a valid input for Maximum Holding Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Holding Time')])
    Holding_time_res = IntegerField(label='Holding time Res', validators=[DataRequired(message='Please enter a valid input for Holding Time Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Holding Time Resolution')])

    Cooling_time_min = IntegerField(label='Cooling time Min', validators=[DataRequired(message='Please enter a valid input for Minimum Cooling Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Minimum Cooling Time')])
    Cooling_time_max = IntegerField(label='Cooling time Max', validators=[DataRequired(message='Please enter a valid input for Maximum Cooling Time'), NumberRange(min=0, max=999999, message='Please enter a valid input for Maximum Cooling Time')])
    Cooling_time_res = IntegerField(label='Cooling time Res', validators=[DataRequired(message='Please enter a valid input for Cooling Time Resolution'), NumberRange(min=0, max=999999, message='Please enter a valid input for Cooling Time Resolution')])

    Mould_temp = IntegerField(label='Mould Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Mould Temperature'), NumberRange(min=0, max=999999, message='Please enter a valid input for Mould Temperature')])
    Clamp_force = IntegerField(label='Clamp force in tonnes', validators=[DataRequired(message='Please enter a valid input for Clamp Force'), NumberRange(min=0, max=999999, message='Please enter a valid input for Clamp Force')])
    Shot_Weight = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Shot Weight'), NumberRange(min=0, max=999999, message='Please enter a valid input for Shot Weight')])

    Mould_SA = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Mould Surface Area'), NumberRange(min=0, max=999999, message='Please enter a valid input for Mould Surface Area')])
    Mould_vol = FloatField(label="Mould Volume in cm3", validators=[DataRequired(message='Please enter a valid input for Mould Volume'), NumberRange(min=0, max=999999, message='Please enter a valid input for Mould Volume')])
    Cavity_SA = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Cavity Surface Area'), NumberRange(min=0, max=999999, message='Please enter a valid input for Cavity Surface Area')])
    Cavity_vol = FloatField(label="Mould Volume in cm3", validators=[DataRequired(message='Please enter a valid input for Cavity Volume'), NumberRange(min=0, max=999999, message='Please enter a valid input for Cavity Volume')])

    Mat_density = FloatField(label="Material Density g/cm3", validators=[DataRequired(message='Please enter a valid input for Material Density'), NumberRange(min=0, max=999999, message='Please enter a valid input for Material Density')])
    Melt_temp = IntegerField(label='Melt Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Material Melt Temperature'), NumberRange(min=0, max=999999, message='Please enter a valid input for Material Melt Temperature')])
    Mat_GF = IntegerField(label='Melt Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Material GF%'), NumberRange(min=0, max=999999, message='Please enter a valid input for Material GF%')])
    Mat_MMFR = FloatField(label="Material Density g/cm3", validators=[DataRequired(message='Please enter a valid input for Material Melt Mass Flow Rate'), NumberRange(min=0, max=999999, message='Please enter a valid input for Material Melt Mass Flow Rate')])
    submit = SubmitField(label='Predict')




class AddEntryForm(FlaskForm):
    Fill_time = IntegerField(label='Fill time', validators=[DataRequired(message='Please enter a valid input for Fill Time'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Injection_pres = IntegerField(label='Injection pressure', validators=[DataRequired(message='Please enter a valid input for Injection Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Holding_pres = IntegerField(label='Holding Pressure', validators=[DataRequired(message='Please enter a valid input for Holding Pressure'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Holding_time = IntegerField(label='Holding time', validators=[DataRequired(message='Please enter a valid input for Holding Time'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Cooling_time = IntegerField(label='Cooling time', validators=[DataRequired(message='Please enter a valid input for Cooling Time'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Mould_temp = IntegerField(label='Mould Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Mould Temp'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Clamp_force = IntegerField(label='Clamp force in tonnes', validators=[DataRequired(message='Please enter a valid input for Clamp Force'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Shot_Weight = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Shot Weight'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Mould_SA = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Mould Surface Area'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Mould_vol = FloatField(label="Mould Volume in cm3", validators=[DataRequired(message='Please enter a valid input for Mould Volume'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Cavity_SA = FloatField(label="Mould Surface Area in mm3", validators=[DataRequired(message='Please enter a valid input for Cavity Surface Area'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Cavity_vol = FloatField(label="Mould Volume in cm3", validators=[DataRequired(message='Please enter a valid input for Cavity Volume'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Mat_density = FloatField(label="Material Density g/cm3", validators=[DataRequired(message='Please enter a valid input for Material Density'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Melt_temp = IntegerField(label='Melt Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Material Melt Temperature'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Mat_GF = IntegerField(label='Melt Temp in Cel', validators=[DataRequired(message='Please enter a valid input for Material GF%'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Mat_MMFR = FloatField(label="Material Density g/cm3", validators=[DataRequired(message='Please enter a valid input for Material Melt Mass Flow Rate'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    Part_weight = FloatField(label="Part Weight", validators=[DataRequired(message='Please enter a valid input for Part Weight'), NumberRange(min=0, max=999999, message='Please enter a valid input')])
    submit = SubmitField(label='ADD')


class AddEntryCSV(FlaskForm):
    file = FileField(label="csv file path", validators=[DataRequired(message='Please enter a valid input for ')])
    submit = SubmitField(label='ADD')


class DeleteEntryForm(FlaskForm):
    submit = SubmitField(label="DELETE")


class DeleteAllEntries(FlaskForm):
    submit = SubmitField(label="WARNING: DELETE ENTIRE DATABASE")


class ExportAllEntries(FlaskForm):
    submit = SubmitField(label="EXPORT DATABASE AS CSV")


class GetCSVFormatForm(FlaskForm):
    submit = SubmitField(label="GET CSV FORMAT")


class RetrainModel(FlaskForm):
    submit = SubmitField(label="Retrain the model")


class HyperTuneModel(FlaskForm):
    submit = SubmitField(label="Auto-HyperTune the model")
