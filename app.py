from flask import Flask, render_template, request
from scipy.optimize import linprog

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/simplex", methods=["GET", "POST"])
def simplex():
    if request.method == "POST":
        try:
            # Input dari form
            profit = list(map(float, request.form.get("profit").split(',')))
            constraints = [list(map(float, row.split(','))) for row in request.form.get("constraints").splitlines()]
            bounds = list(map(float, request.form.get("bounds").split(',')))

            # Setup untuk metode simplex
            result = linprog(
                c=[-p for p in profit],  # Maximasi dikonversi ke minimasi
                A_ub=constraints,
                b_ub=bounds,
                method="simplex"
            )

            if result.success:
                optimal_value = -result.fun
                optimal_solution = result.x
                return render_template("simplex.html", result=True, optimal_value=optimal_value, optimal_solution=optimal_solution)
            else:
                return render_template("simplex.html", result=False, error="Optimasi gagal!")
        except Exception as e:
            return render_template("simplex.html", result=False, error=str(e))
    return render_template("simplex.html")

@app.route("/kontak")
def kontak():
    return render_template("kontak.html")

if __name__ == "__main__":
    app.run(debug=True)
