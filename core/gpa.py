import pandas as pd
from jinja2 import Environment, FileSystemLoader


def set_environemnt(folder: str, template: str):
    env = Environment(loader=FileSystemLoader(folder))
    template = env.get_template(template)
    return template


def RepublicOfChinaCalendar(i):
    i = str(i)
    rocc, semester = i[:3], i[-1]
    year, semester = int(rocc) + 1911, int(semester)

    if semester == 2:
        year += 1

    return year, SemesterTransform(semester)


def SemesterTransform(semester):
    if semester == 1:
        return "Fall"
    elif semester == 2:
        return "Spring"


def PaddingGrade(i):
    if isinstance(i, str):
        if len(i) == 1:
            return f"{i}&ensp;"
        else:
            return i
    elif isinstance(i, float):
        return f"{i:.2f}"


def Tofloat(i):
    try:
        return float(i)
    except ValueError:
        return i


def ToCenter(i):
    return f"<center>{i}</center>"


class GPA:
    def __init__(self, version: str):
        self.gpamap = self.gpa43 if version == "4.3" else self.gpa40
        self.grade2gpa = self.to_gpa43 if version == "4.3" else self.to_gpa40

    def calculate(self, df: pd.DataFrame):
        df = df[df["Credits"] > 0]
        df = df[df["Grade"] != "Pass"]

        try:
            df["Grade"] = df["Grade"].astype(float)
        except ValueError:
            pass

        if df["Grade"].dtypes == "object":
            df["GPA"] = df["Grade"].map(self.gpamap)

        elif df["Grade"].dtypes in (["int64", "float64"]):
            df["GPA"] = df["Grade"].apply(self.grade2gpa)

        df["GPA"] = df["GPA"] * df["Credits"]

        return round(df["GPA"].sum() / df["Credits"].sum(), 2)

    def total_credits(self, df: pd.DataFrame):
        return df["Credits"].sum()

    def earned_credits(self, df: pd.DataFrame):
        df = df[df["Credits"] > 0]
        df_p = df[df["Grade"] == "Pass"]
        df = df[df["Grade"] != "Pass"]

        try:
            df["Grade"] = df["Grade"].astype(float)
        except ValueError:
            pass

        if df["Grade"].dtypes == "object":
            df["GPA"] = df["Grade"].map(self.gpamap)

        elif df["Grade"].dtypes in (["int64", "float64"]):
            df["GPA"] = df["Grade"].apply(self.grade2gpa)

        df = df[df["GPA"] > 1.0]
        s = df["Credits"].sum() + df_p["Credits"].sum()

        return s

    @property
    def gpa43(self):
        return {
            "A+": 4.3,
            "A": 4.0,
            "A-": 3.7,
            "B+": 3.3,
            "B": 3.0,
            "B-": 2.7,
            "C+": 2.3,
            "C": 2.0,
            "C-": 1.7,
            "D": 1.0,
            "E": 0,
            "P": "Pass",
        }

    @property
    def gpa40(self):
        return {"A": 4.0, "B": 3.0, "C": 2.0, "D": 1.0, "F": 0, "P": "Pass"}

    @staticmethod
    def to_float(score):
        try:
            return float(score)
        except ValueError:
            return score

    @staticmethod
    def to_gpa40(score):
        score = GPA.to_float(score)
        if score == "Pass":
            return "Pass"
        elif score >= 80:
            return 4.0
        elif score >= 70:
            return 3.0
        elif score >= 60:
            return 2.0
        elif score >= 50:
            return 1.0
        else:
            return 0

    @staticmethod
    def to_gpa43(score):
        score = GPA.to_float(score)
        if score == "Pass":
            return "Pass"
        elif score >= 90:
            return 4.3
        elif score >= 85:
            return 4.0
        elif score >= 80:
            return 3.7
        elif score >= 77:
            return 3.3
        elif score >= 73:
            return 3.0
        elif score >= 70:
            return 2.7
        elif score >= 67:
            return 2.3
        elif score >= 63:
            return 2.0
        elif score >= 60:
            return 1.7
        elif score >= 50:
            return 1.0
        else:
            return 0


if __name__ == "__main__":
    import argparse

    import pandas as pd

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", help="input file path")
    parser.add_argument("--output", help="output file path")
    parser.add_argument("--sheet", help="sheet name")
    parser.add_argument("--bg-logo", help="background logo")
    parser.add_argument("--gpa", help="gpa version", type=str, default="4.3")
    parser.add_argument("--university", help="university", type=str)
    parser.add_argument("--major", help="major", type=str)
    parser.add_argument("--std_id", help="student id", type=str)
    parser.add_argument("--std_name", help="student name", type=str)

    args = parser.parse_args()

    # -- read excel file -----------------------------------------------------------------
    df = pd.read_excel(args.input, sheet_name=args.sheet)
    df["Grade"] = df["Grade"].apply(Tofloat)

    df_semester = df["Semester"].apply(RepublicOfChinaCalendar).apply(pd.Series)
    df_semester.columns = ["Year", "Semester-2"]

    df = pd.concat([df, df_semester], axis=1)
    df = df.sort_values(by=["Semester"], ascending=True)

    # -- setup template ------------------------------------------------------------------
    template = set_environemnt(
        folder="static/template/html", template="transcript.html"
    )

    # -- calculate gpa -------------------------------------------------------------------
    gpa = GPA(version=args.gpa)
    overall_gpa_score = gpa.calculate(df[["Credits", "Grade"]])

    # -- group by semester --------------------------------------------------------------
    transcripts = []
    group_by_semester = df.groupby(["Semester"])
    for info, group in group_by_semester:
        year, semester = group["Year"].iloc[0], group["Semester-2"].iloc[0]
        semester_info = {
            "year": year,
            "semester": semester,
            "Total Credits Earned": group["Credits"].sum(),
            "Grade Point Average": gpa.calculate(group[["Credits", "Grade"]]),
        }

        try:
            gpa_key = list(gpa.gpamap.keys())
            group["Grade"] = group["Grade"].apply(gpa.grade2gpa)
            group["Grade"] = group["Grade"].apply(
                lambda x: gpa_key[list(gpa.gpamap.values()).index(x)]
            )

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            pass

        group = group[["Course Code", "Course Title", "Credits", "Grade"]]

        group["Credits"] = group["Credits"].apply(ToCenter)
        group["Grade"] = group["Grade"].apply(PaddingGrade)
        group["Grade"] = group["Grade"].apply(ToCenter)

        semester_info.update(
            {
                "html": group.to_html(
                    index=False,
                    border=0,
                    col_space=[60, 150, 10, 10],
                    justify="left",
                    escape=False,
                )
            }
        )

        transcripts.append(semester_info)

    if len(transcripts) % 2 != 0:
        transcripts.append(
            {
                "year": year + 1,
                "semester": "Spring",
                "Total Credits Earned": "None",
                "Grade Point Average": "None",
                "html": "",
            }
        )

    template = template.render(
        bg_logo=args.bg_logo,
        gpa_version=args.gpa,
        university=args.university,
        major=args.major,
        transcripts=transcripts,
        overall_gpa_score=overall_gpa_score,
        std_id=args.std_id,
        std_name=args.std_name,
        total_credits=gpa.total_credits(df),
        earned_credits=gpa.earned_credits(df),
    )

    with open(f"{args.output}", "w") as f:
        f.write(template)
