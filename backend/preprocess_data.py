import glob
import sys
import pandas as pd

DATADIR = "data/"

if __name__ == "__main__":
    for fn in glob.glob(DATADIR + "*.csv"):
        print("Processing: %s", fn, file=sys.stderr, end="")
        df = pd.read_csv(fn)

        avg_grade_list = []
        nb_of_grades_list = []
        for index, row in df.iterrows():
            avg_grade = 0
            for i in range(5):
                avg_grade += (i + 1) * int(row[f"RatingDist{i + 1}"].split(":")[1])
            nb_of_grades = int(row["RatingDistTotal"].split(":")[1])
            if nb_of_grades > 0:
                avg_grade /= nb_of_grades
            avg_grade_list.append(avg_grade)
            nb_of_grades_list.append(nb_of_grades)

        if "avg_grade" not in df:
            df["avg_grade"] = avg_grade_list
        if "nb_of_grades" not in df:
            df["nb_of_grades"] = nb_of_grades_list

        df.to_csv(fn)

        print("...done:", fn, file=sys.stderr)
