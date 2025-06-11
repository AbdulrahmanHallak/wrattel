import random

import sqlparse
from faker import Faker
from mysql.connector.conversion import MySQLConverter


class Seeder:
    def __init__(self, fake, converter):
        self.fake = fake
        self.converter = converter

    def seed_all(self):
        pass

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
        student_insert = "INSERT INTO student(id, quranic_achievement, status)\nVALUES"
        student_values = "(%s, '%s', '%s'),\n"
        student_ids = []
        # Use the first 90 person_ids for students
        for i in range(90):
            student_id = person_ids[i]
            student_ids.append(student_id)
            student = (
                student_id,
                "random stuff",
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
        for supervisor_id in supervisor_ids:
            supervisor = (
                supervisor_id,
                random.choice(["مسمع", "مساعد", "مشرف"]),
                self.fake.date(),
                self.fake.date(),
            )
            formatted_values = tuple([self.converter.escape(v) for v in supervisor])
            supervisor_insert = supervisor_insert + (
                supervisor_values % formatted_values
            )
        supervisor_insert = supervisor_insert.strip()[0:-1] + ";" + ("\n" * 3)
        return supervisor_insert, supervisor_ids

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
        insert_levels = f"""\
            INSERT INTO level(id, name, description, plan)
            VALUES(1, '{self.converter.escape("تلاوة")}', 'lorem ipsem', 'lorem ipsem'),
            (2, '{self.converter.escape("غيبي")}', 'lorem ipsem', 'lorem ipsem'),
            (3, '{self.converter.escape("انتقالي")}', 'lorem ipsem', 'lorem ipsem'),
            (4, '{self.converter.escape("اجازة")}', 'lorem ipsem', 'lorem ipsem');
        """ + ("\n" * 3)
        level_ids = [1, 2, 3, 4]
        return sqlparse.format(insert_levels), level_ids

    def seed_student_levels(self, student_ids, level_ids):
        insert = (
            "INSERT INTO student_level(id, level_id, student_id, reached_at)\nVALUES"
        )
        values = "(%s, %s, %s, '%s'),\n"
        student_level_id = 1
        for student_id in student_ids:
            student = (
                student_level_id,
                random.choice(level_ids),
                student_id,
                self.fake.date(),
            )
            student_level_id += 1
            formatted_values = tuple(self.converter.escape(v) for v in student)
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert)

    def seed_errors(self):
        insert_error = f"""\
            INSERT INTO error(id, error_type, score)
            VALUES(1, '{self.converter.escape("تجويدي")}', {self.converter.escape(-4)}),
            (2, '{self.converter.escape("حفظي")}', {self.converter.escape(-3)}),
            (3, '{self.converter.escape("تشكيلي")}', {self.converter.escape(-2)});
        """ + ("\n" * 3)
        error_ids = [1, 2, 3]
        return sqlparse.format(insert_error), error_ids

    def seed_reports(self, supervision_ids):
        insert = (
            "INSERT INTO report(id, student_supervisor_id, start_page, qty)\nVALUES"
        )
        values = "(%s, %s, '%s', '%s'),\n"
        report_ids = []
        for i, supervision_id in enumerate(supervision_ids):
            for _ in range(10):
                report_id = i * 10 + _ + 1
                report_ids.append(report_id)
                report = (
                    report_id,
                    supervision_id,
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
                    "lorem ipsem",
                    "lorem ipsem",
                )
                report_error_id += 1
                formatted_values = tuple(
                    [self.converter.escape(v) for v in error_report]
                )
                insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert)

    def seed_certificate(self):
        insert = "INSERT INTO certificate(id, reading)\nVALUES"
        values = "(%s, '%s'),\n"
        cert_ids = []
        for i in range(10):
            cert_id = i + 1
            cert_ids.append(cert_id)
            certificate = (cert_id, self.fake.text(20))
            formatted_values = tuple([self.converter.escape(v) for v in certificate])
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert), cert_ids

    def seed_person_certificate(self, supervisor_ids, cert_ids):
        insert = "INSERT INTO person_certificate(id, certificate_id, person_id, date_acquired)\nVALUES"
        values = "(%s, '%s', '%s', '%s'),\n"
        person_cert_id = 1
        for supervisor_id in supervisor_ids[:3]:
            cert_per = (
                person_cert_id,
                random.choice(cert_ids),
                supervisor_id,
                self.fake.date(),
            )
            person_cert_id += 1
            formatted_values = tuple([self.converter.escape(v) for v in cert_per])
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert)

    def seed_exam(self, student_ids, supervisor_ids):
        insert = "INSERT INTO exam(id, student_id, supervisor_id, exam_type, part, qty, exam_date)\nVALUES"
        values = "(%s, %s, %s, '%s', %s, %s, '%s'),\n"
        exam_ids = []
        for i, student_id in enumerate(student_ids[23:76]):
            exam_id = i + 1
            exam_ids.append(exam_id)
            exam = (
                exam_id,
                student_id,
                random.choice(supervisor_ids),
                random.choice(["انتقالي", " مرحلي"]),
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

    def seed_activity_type(self, supervisor_ids):
        insert = "INSERT INTO activity_type(id, name, presenter_id, student_level_required)\nVALUES"
        values = "(%s, '%s', %s, '%s'),\n"
        activity_type_ids = []
        for i in range(6):
            activity_type_id = i + 1
            activity_type_ids.append(activity_type_id)
            activity_type = (
                activity_type_id,
                self.fake.word(),
                random.choice(supervisor_ids),
                random.choice(["غيبي", "انتقالي"]),
            )
            formatted_values = tuple([self.converter.escape(v) for v in activity_type])
            insert = insert + (values % formatted_values)
        insert = insert.strip()[0:-1] + ";" + ("\n" * 3)
        return sqlparse.format(insert), activity_type_ids

    def seed_activity(self, activity_type_ids, supervisor_ids):
        insert = "INSERT INTO activity(id, title, activity_type_id, coordinator_id, activity_date)\nVALUES"
        values = "(%s, '%s', %s, %s, '%s'),\n"
        activity_ids = []
        for i in range(20):
            activity_id = i + 1
            activity_ids.append(activity_id)
            activity = (
                activity_id,
                self.fake.sentence(4),
                random.choice(activity_type_ids),
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


def main():
    fake = Faker("ar_SA")
    converter = MySQLConverter()
    seeder = Seeder(fake, converter)
    person_insert, person_ids = seeder.seed_person()
    student_insert, student_ids = seeder.seed_student(person_ids)
    supervisor_insert, supervisor_ids = seeder.seed_supervisor(person_ids, student_ids)
    supervision_insert = seeder.seed_supervision(student_ids, supervisor_ids)
    levels_insert, level_ids = seeder.seed_levels()
    student_levels_insert = seeder.seed_student_levels(student_ids, level_ids)
    errors_insert, error_ids = seeder.seed_errors()
    # Generate supervision IDs (1 to len(student_ids))
    supervision_ids = list(range(1, len(student_ids) + 1))
    reports_insert, report_ids = seeder.seed_reports(supervision_ids)
    report_errors_insert = seeder.seed_report_errors(report_ids, error_ids)
    certificate_insert, cert_ids = seeder.seed_certificate()
    person_certificate_insert = seeder.seed_person_certificate(supervisor_ids, cert_ids)
    exam_insert, exam_ids = seeder.seed_exam(student_ids, supervisor_ids)
    exam_error_insert = seeder.seed_exam_error(exam_ids, error_ids)
    activity_type_insert, activity_type_ids = seeder.seed_activity_type(supervisor_ids)
    activity_insert, activity_ids = seeder.seed_activity(
        activity_type_ids, supervisor_ids
    )
    activity_student_insert = seeder.seed_acvitity_student(activity_ids, student_ids)
    with open("./data.sql", "w") as f:
        f.write(
            person_insert
            + "\n"
            + student_insert
            + "\n"
            + supervisor_insert
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
            + certificate_insert
            + "\n"
            + person_certificate_insert
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
        )


if __name__ == "__main__":
    main()
