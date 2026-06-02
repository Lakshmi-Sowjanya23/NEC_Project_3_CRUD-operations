from flask import Flask, render_template, request, redirect
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r") as file:
        try:
            return json.load(file)
        except:
            return []


def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


@app.route("/")
def index():
    records = load_data()
    return render_template("index.html", records=records)


@app.route("/add", methods=["POST"])
def add():
    name = request.form["name"]
    age = request.form["age"]

    records = load_data()

    records.append({
        "name": name,
        "age": age
    })

    save_data(records)

    return redirect("/")


@app.route("/delete/<int:index>")
def delete(index):
    records = load_data()

    if 0 <= index < len(records):
        records.pop(index)

    save_data(records)

    return redirect("/")


@app.route("/edit/<int:index>", methods=["POST"])
def edit(index):
    records = load_data()

    if 0 <= index < len(records):
        records[index]["name"] = request.form["name"]
        records[index]["age"] = request.form["age"]

    save_data(records)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)