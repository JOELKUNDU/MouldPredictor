from predictor import app, state

if __name__ == '__main__':
    state.serverModeOn()
    app.run(debug=True)
