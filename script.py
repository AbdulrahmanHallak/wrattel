import random

import sqlparse
from faker import Faker
from mysql.connector.conversion import MySQLConverter


class Seeder:
    def __init__(self, fake, converter):
        self.fake = fake
        self.converter = converter

    def seed_person(self):
        person_insert = "INSERT INTO person (id, fname, lname, year_of_study, contact_number, join_date, email, address)\nVALUES"
        person_values = "(%s, '%s', '%s', %s, '%s', '%s', '%s', '%s'),\n"
        person_ids = []
        for i in range(100):
            person_id = i + 1
            person_ids.append(person_id)
            person = (
                person_id,
                self.fake.first_name(),
                self.fake.last_name(),
                random.randint(1, 5),
                self.fake.numerify("###-###-###"),
                self.fake.date(),
                self.fake.free_email(),
                self.fake.address(),
            )
            formatted_values = tuple([self.converter.escape(v) for v in person])
            person_insert = person_insert + (person_values % formatted_values)
        person_insert = person_insert.strip()[0:-1] + ";" + ("\n" * 3)
        return person_insert, person_ids

    def seed_student(self, person_ids):
        student_insert = "INSERT INTO student(id, status)\nVALUES"
        student_values = "(%s, '%s'),\n"
        student_ids = []
        # Use the first 90 person_ids for students
        for i in range(90):
            student_id = person_ids[i]
            student_ids.append(student_id)
            student = (
                student_id,
                random.choice(["نشط", "منقطع", "متخرج"]),
            )
            formatted_values = tuple([self.converter.escape(v) for v in student])
            student_insert = student_insert + (student_values % formatted_values)
        student_insert = student_insert.strip()[0:-1] + ";" + ("\n" * 3)
        return student_insert, student_ids

    def seed_supervisor(self, person_ids, student_ids):
        # Use person_ids that are not in student_ids for supervisors
        supervisor_ids = [pid for pid in person_ids if pid not in student_ids]

        supervisor_insert = (
            "INSERT INTO supervisor(id, role, became_supervisor_at, retired_at)\nVALUES"
        )
        supervisor_values = "(%s, '%s', '%s', '%s'),\n"

        assitant_ids = []
        for supervisor_id in supervisor_ids:
            supervisor = (
                supervisor_id,
                random.choice(["مسمع", "مساعد", "مشرف"]),
                self.fake.date(),
                self.fake.date(),
            )
            if supervisor[1] == "مساعد":
                assitant_ids.append(supervisor[0])

            formatted_values = tuple([self.converter.escape(v) for v in supervisor])
            supervisor_insert = supervisor_insert + (
                supervisor_values % formatted_values
            )
        supervisor_insert = supervisor_insert.strip()[0:-1] + ";" + ("\n" * 3)
        return supervisor_insert, supervisor_ids, assitant_ids

    def seed_supervisor_assistants(self, assistant_ids):
        if not assistant_ids:
            return ""

        # Create UPDATE statements for each assistant
        updates = []
        other_supervisors = [s for s in range(91, 101) if s not in assistant_ids][:3]
        for _ in range(len(other_supervisors)):
            supervisor_id = random.choice(other_supervisors)
            assistant_id = random.choice(assistant_ids)
            update = f"UPDATE supervisor SET assistant_id = {assistant_id} WHERE id = {supervisor_id};"
            updates.append(update)

        return "\n".join(updates) + ("\n" * 3)

    def seed_supervision(self, student_ids, supervisor_ids):
        insert_supervision = "INSERT INTO student_supervisor(id, student_id, supervisor_id, retired_at)\nVALUES"
        supervision_values = "(%s, %s, %s, '%s'),\n"
        supervision_id = 1
        for student_id in student_ids:
            supervision = (
                supervision_id,
                student_id,
                random.choice(supervisor_ids),
                self.fake.date(),
            )
            supervision_id += 1
            formatted_values = tuple([self.converter.escape(v) for v in supervision])
            insert_supervision = insert_supervision + (
                supervision_values % formatted_values
            )
        insert_supervision = insert_supervision.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert_supervision)

    def seed_levels(self):
        insert_levels = """\
            INSERT INTO level(id, name, description, plan)
            VALUES(1, 'تلاوة', 'مستوى التجويد ضعيف', 'تلاوة 4 أجزاء على المسمع وتعلم كتاب لغتي وقرآني وعند الانتهاء ينقل للانتقالي'),
            (2, 'غيبي', 'مستوى التجويد جيّد', 'تعلم كتاب المنهج الموحّد في التجويد و تسميع عدد من الصفحات حاضرًا حتّى يصبح تجويده ممتازًا وبناءً على تقاريره ينقل إلى الغيبي'),
            (3, 'انتقالي', 'مستوى التجويد ممتاز', 'تسميع الصفحات غيبًا وإجراء سبر لكل جزء ينهيه وعند حفظه لجميع الأجزاء يبدأ بالإجازة'),
            (4, 'اجازة', 'مستوى التجويد ممتاز وتم حفظ وسبر جميع أجزاء القرآن', 'تعلّم نظم المقدمة الجزريّة وإعادة سبر جميع الأجزاء عند مسمع واحد فقط');
        """ + ("\n" * 3)
        level_ids = [1, 2, 3, 4]
        return sqlparse.format(insert_levels), level_ids

    def seed_student_levels(self, student_ids, level_ids):
        insert = (
            "INSERT INTO student_level(id, level_id, student_id, reached_at)\nVALUES"
        )
        values = "(%s, %s, %s, '%s'),\n"
        student_level_id = 1
        student_level_ids = []
        for student_id in student_ids:
            student = (
                student_level_id,
                random.choice(level_ids),
                student_id,
                self.fake.date(),
            )
            student_level_ids.append(student_level_id)
            student_level_id += 1
            formatted_values = tuple(self.converter.escape(v) for v in student)
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert), student_level_ids

    def seed_errors(self):
        insert_error = f"""\
            INSERT INTO error(id, error_type, score)
            VALUES(1, '{self.converter.escape("تجويدي")}', {self.converter.escape(-4)}),
            (2, '{self.converter.escape("حفظي")}', {self.converter.escape(-3)}),
            (3, '{self.converter.escape("تشكيلي")}', {self.converter.escape(-2)});
        """ + ("\n" * 3)
        error_ids = [1, 2, 3]
        return sqlparse.format(insert_error), error_ids

    def seed_reports(self, supervision_ids, student_level_ids):
        insert = "INSERT INTO report(id, student_supervisor_id, student_level_id, start_page, qty)\nVALUES"
        values = "(%s, %s, %s, '%s', '%s'),\n"
        report_ids = []
        for i, supervision_id in enumerate(supervision_ids):
            for _ in range(10):
                report_id = i * 10 + _ + 1
                report_ids.append(report_id)
                report = (
                    report_id,
                    supervision_id,
                    random.choice(student_level_ids),
                    random.randint(1, 604),
                    random.randint(3, 21),
                )
                formatted_values = tuple(self.converter.escape(v) for v in report)
                insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert), report_ids

    def seed_report_errors(self, report_ids, error_ids):
        insert = "INSERT INTO report_error(id, report_id, error_id, details, error_word)\nVALUES"
        values = "(%s, %s, %s, '%s', '%s'),\n"
        report_error_id = 1
        for report_id in report_ids:
            for _ in range(random.randint(0, 5)):
                error_report = (
                    report_error_id,
                    report_id,
                    random.choice(error_ids),
                    self.fake.sentence()[0:45],
                    self.fake.word(),
                )
                report_error_id += 1
                formatted_values = tuple(
                    [self.converter.escape(v) for v in error_report]
                )
                insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert)

    def seed_exam(self, student_ids, supervisor_ids, student_level_ids):
        insert = "INSERT INTO exam(id, student_id, supervisor_id, student_level_id, exam_type, part, qty, exam_date)\nVALUES"
        values = "(%s, %s, %s, %s, '%s', %s, %s, '%s'),\n"
        exam_ids = []
        for i, student_id in enumerate(student_ids[23:76]):
            exam_id = i + 1
            exam_ids.append(exam_id)
            exam = (
                exam_id,
                student_id,
                random.choice(supervisor_ids),
                random.choice(student_level_ids),
                random.choice(["انتقالي", "مرحلي"]),
                random.randint(1, 30),
                random.randint(1, 30),
                self.fake.date(),
            )
            formatted_values = tuple([self.converter.escape(v) for v in exam])
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert), exam_ids

    def seed_exam_error(self, exam_ids, error_ids):
        insert = (
            "INSERT INTO exam_error(error_id, exam_id, details, error_word)\nVALUES"
        )
        values = "(%s, %s, '%s', '%s'),\n"
        for exam_id in exam_ids:
            exam_error = (
                random.choice(error_ids),
                exam_id,
                self.fake.sentence(2),
                self.fake.word(),
            )
            formatted_values = tuple([self.converter.escape(v) for v in exam_error])
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert)

    def seed_activity_type(self):
        insert = "INSERT INTO activity_type(id, name)\nVALUES"
        values = "(%s, '%s'),\n"
        activity_type_ids = []
        activity_types = [
            "حديث",
            "فقه",
            "عقيدة",
            "سيرة",
            "صحابة",
            "تدبّر",
            "لغتي وقرآني",
            "نظم الجزريّة",
            "تجويد",
            "أسماء الله الحسنى",
            "تفسير",
        ]
        for i in range(10):
            activity_type_id = i + 1
            activity_type_ids.append(activity_type_id)
            activity_type = (
                activity_type_id,
                activity_types[i],
            )
            formatted_values = tuple([self.converter.escape(v) for v in activity_type])
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert), activity_type_ids

    def seed_activity(self, activity_type_ids, supervisor_ids):
        insert = "INSERT INTO activity(id, title, activity_type_id, coordinator_id, presenter_id, activity_date)\nVALUES"
        values = "(%s, '%s', %s, %s, %s,'%s'),\n"
        activity_ids = []
        for i in range(20):
            activity_id = i + 1
            activity_ids.append(activity_id)
            activity = (
                activity_id,
                self.fake.sentence(4),
                random.choice(activity_type_ids),
                random.choice(supervisor_ids),
                random.choice(supervisor_ids),
                self.fake.date(),
            )
            formatted_values = tuple([self.converter.escape(v) for v in activity])
            insert = insert + (values % formatted_values)

        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert), activity_ids

    def seed_acvitity_student(self, activity_ids, student_ids):
        insert = "INSERT INTO activity_student(id, activity_id, student_id)\nVALUES"
        values = "(%s, '%s', '%s'),\n"
        activity_student_id = 1
        for _ in range((len(student_ids) * len(activity_ids) // 3)):
            student_activity = (
                activity_student_id,
                random.choice(activity_ids),
                random.choice(student_ids),
            )
            activity_student_id += 1
            formatted_values = tuple(
                [self.converter.escape(v) for v in student_activity]
            )
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert)

    def seed_achievement(self, person_ids):
        insert = "INSERT INTO achievement(id, num_of_parts, type_of_achievement, date_aquired, person_id)\nVALUES"
        values = "(%s, %s, '%s', '%s', %s),\n"
        achievement_types = ["تلاوة", "غيبي", "اجازة"]
        achievement_id = 1
        for _ in range(20):
            achievement = (
                achievement_id,
                random.randint(1, 30),
                random.choice(achievement_types),
                self.fake.date(),
                random.choice(person_ids),
            )
            achievement_id += 1
            formatted_values = tuple([self.converter.escape(v) for v in achievement])
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert)


def main():
    fake = Faker("ar_SA")
    converter = MySQLConverter()
    seeder = Seeder(fake, converter)
    person_insert, person_ids = seeder.seed_person()
    student_insert, student_ids = seeder.seed_student(person_ids)
    supervisor_insert, supervisor_ids, assistant_ids = seeder.seed_supervisor(
        person_ids, student_ids
    )
    supervisor_assistants_insert = seeder.seed_supervisor_assistants(assistant_ids)
    supervision_insert = seeder.seed_supervision(student_ids, supervisor_ids)
    levels_insert, level_ids = seeder.seed_levels()
    student_levels_insert, student_level_ids = seeder.seed_student_levels(
        student_ids, level_ids
    )
    errors_insert, error_ids = seeder.seed_errors()
    # Generate supervision IDs (1 to len(student_ids))
    supervision_ids = list(range(1, len(student_ids) + 1))
    reports_insert, report_ids = seeder.seed_reports(supervision_ids, student_level_ids)
    report_errors_insert = seeder.seed_report_errors(report_ids, error_ids)
    achievement_insert = seeder.seed_achievement(person_ids)
    exam_insert, exam_ids = seeder.seed_exam(
        student_ids, supervisor_ids, student_level_ids
    )
    exam_error_insert = seeder.seed_exam_error(exam_ids, error_ids)
    activity_type_insert, activity_type_ids = seeder.seed_activity_type()
    activity_insert, activity_ids = seeder.seed_activity(
        activity_type_ids, supervisor_ids
    )
    activity_student_insert = seeder.seed_acvitity_student(activity_ids, student_ids)

    # MySQL configuration statements
    mysql_config = """\
        SET NAMES utf8mb4;
        SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
        SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
        SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';
        SET @old_autocommit=@@autocommit;

        USE wrattel;

        SET AUTOCOMMIT=0;

    """

    mysql_cleanup = """\
        COMMIT;

        SET SQL_MODE=@OLD_SQL_MODE;
        SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
        SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
        SET autocommit=@old_autocommit;
    """

    with open("./data.sql", "w") as f:
        f.write(
            mysql_config
            + person_insert
            + "\n"
            + student_insert
            + "\n"
            + supervisor_insert
            + "\n"
            + supervisor_assistants_insert
            + "\n"
            + supervision_insert
            + "\n"
            + levels_insert
            + "\n"
            + student_levels_insert
            + "\n"
            + errors_insert
            + "\n"
            + reports_insert
            + "\n"
            + report_errors_insert
            + "\n"
            + achievement_insert
            + "\n"
            + exam_insert
            + "\n"
            + exam_error_insert
            + "\n"
            + activity_type_insert
            + "\n"
            + activity_insert
            + "\n"
            + activity_student_insert
            + mysql_cleanup
        )


if __name__ == "__main__":
    main()
