import os

from flask import Flask, render_template, request, redirect, url_for, send_file
from project import (
    FILENAME,
    load_workouts,
    save_workout,
    validate_entry,
    personal_record,
    weekly_volume,
    delete_workout,
    exercise_progress,
)

app = Flask(__name__)

def build_progress(points):
    if not points:
        return None
    width, height, pad = 600, 220, 30
    weights = [weight for _, weight in points]
    low, high = min(weights), max(weights)
    coords = []
    for i, (day, weight) in enumerate(points):
        share_x = i / (len(points) - 1) if len(points) > 1 else 0.5
        share_y = (weight - low) / (high - low) if high != low else 0.5
        coords.append({
            "x": round(pad + (width - 2 * pad) * share_x, 1),
            "y": round(height - pad - (height - 2 * pad) * share_y, 1),
            "date": day,
            "weight": weight,
        })
    return {
        "width": width,
        "height": height,
        "low": low,
        "high": high,
        "first": points[0][0],
        "last": points[-1][0],
        "points": coords,
        "line": " ".join(f"{c['x']},{c['y']}" for c in coords),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    error = None
    if request.method == "POST":
        try:
            entry = validate_entry(
                request.form["exercise"],
                request.form["sets"],
                request.form["reps"],
                request.form["weight"],
            )
        except ValueError as e:
            error = str(e)
        else:
            save_workout(entry)
            return redirect(url_for("index"))

    workouts = load_workouts()

    stats = {
        "workouts": len(workouts),
        "volume": round(sum(w["sets"] * w["reps"] * w["weight"] for w in workouts)),
        "exercises": len({w["exercise"] for w in workouts}),
    }

    # Personal records: heaviest lift per exercise, biggest first
    names = {w["exercise"] for w in workouts}
    records = sorted(
        ((name, personal_record(workouts, name)) for name in names),
        key=lambda item: item[1],
        reverse=True,
    )

    selected = request.args.get("exercise", "").strip().lower()
    if selected not in names:
        selected = sorted(names)[0] if names else ""
    progress = build_progress(exercise_progress(workouts, selected)) if selected else None

    # Weekly volume chart: latest 8 weeks
    weekly = weekly_volume(workouts)
    weeks = sorted(weekly)[-8:]
    peak = max((weekly[w] for w in weeks), default=0) or 1
    chart = [
        {
            "label": w.split("-")[1],
            "volume": round(weekly[w]),
            "height": round(weekly[w] / peak * 100),
        }
        for w in weeks
    ]

    history = list(reversed(list(enumerate(workouts))))
    return render_template(
        "index.html",
        workouts=history,
        stats=stats,
        records=records,
        chart=chart,
        exercises=sorted(names),
        selected=selected,
        progress=progress,
        error=error,
    )
@app.route("/download")
def download():
    if not os.path.exists(FILENAME) or os.path.getsize(FILENAME) == 0:
        return redirect(url_for("index"))
    return send_file(FILENAME, as_attachment=True, download_name="workouts.csv")

@app.route("/delete/<int:index>", methods=["POST"])
def delete(index):
    try:
        delete_workout(index)
    except ValueError:
        pass
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)