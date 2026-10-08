"""Sistema de gestión de calificaciones de estudiantes."""

import math

MIN_GRADE = 0.0
MAX_GRADE = 100.0
PASS_THRESHOLD = 60.0
HONOR_THRESHOLD = 90.0
LETTER_SCALE = ((90.0, "A"), (80.0, "B"), (70.0, "C"), (60.0, "D"))
FAIL_LETTER = "F"


class Student:
    """Representa un estudiante y sus calificaciones."""

    def __init__(self, student_id, name):
        """Crea un estudiante validando que ID y nombre no estén vacíos."""
        student_id = str(student_id).strip()
        name = str(name).strip() if name is not None else ""
        if not student_id:
            raise ValueError("El ID no puede estar vacío.")
        if not name:
            raise ValueError("El nombre no puede estar vacío.")
        self.student_id = student_id
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        """Agrega una nota numérica en el rango 0-100."""
        if isinstance(grade, bool):
            raise ValueError(f"Nota inválida: {grade!r} no es numérica.")
        try:
            value = float(grade)
        except (TypeError, ValueError) as error:
            raise ValueError(f"Nota inválida: {grade!r} no es numérica.") from error
        if not math.isfinite(value) or not MIN_GRADE <= value <= MAX_GRADE:
            raise ValueError(
                f"Nota inválida: {grade!r} debe estar entre {MIN_GRADE:g} y {MAX_GRADE:g}."
            )
        self.grades.append(value)

    def remove_grade_by_value(self, value):
        """Elimina la primera nota con el valor indicado."""
        try:
            self.grades.remove(float(value))
        except (TypeError, ValueError) as error:
            raise ValueError(f"No existe la nota {value!r}.") from error

    def remove_grade_by_index(self, index):
        """Elimina la nota en la posición indicada (base 0)."""
        if not isinstance(index, int) or isinstance(index, bool):
            raise IndexError(f"Índice inválido: {index!r}.")
        if not 0 <= index < len(self.grades):
            raise IndexError(
                f"Índice {index} fuera de rango (hay {len(self.grades)} notas)."
            )
        del self.grades[index]

    def average(self):
        """Devuelve el promedio de las notas."""
        if not self.grades:
            raise ValueError("El estudiante no tiene notas registradas.")
        return sum(self.grades) / len(self.grades)

    def letter_grade(self):
        """Convierte el promedio en nota con letra."""
        average = self.average()
        for threshold, letter in LETTER_SCALE:
            if average >= threshold:
                return letter
        return FAIL_LETTER

    def status(self):
        """Devuelve 'Passed' o 'Failed' según el promedio."""
        return "Passed" if self.average() >= PASS_THRESHOLD else "Failed"

    def is_honor_roll(self):
        """Indica si el estudiante está en el cuadro de honor."""
        return self.average() >= HONOR_THRESHOLD

    def summary_report(self):
        """Genera el reporte resumen del estudiante."""
        lines = [
            "=" * 32,
            f"Student ID    : {self.student_id}",
            f"Student Name  : {self.name}",
            f"Grades Count  : {len(self.grades)}",
        ]
        if self.grades:
            lines += [
                f"Average Grade : {self.average():.2f}",
                f"Letter Grade  : {self.letter_grade()}",
                f"Status        : {self.status()}",
                f"Honor Roll    : {self.is_honor_roll()}",
            ]
        else:
            lines.append("Average Grade : N/A (sin notas)")
        lines.append("=" * 32)
        return "\n".join(lines)


def try_action(description, action, *args):
    """Ejecuta una acción mostrando un mensaje claro si falla."""
    try:
        action(*args)
        print(f"[OK] {description}")
    except (ValueError, IndexError) as error:
        print(f"[ERROR] {description}: {error}")


def main():
    """Demuestra los requisitos funcionales."""
    try:
        Student("", "Ana")
    except ValueError as error:
        print(f"[ERROR] Crear estudiante: {error}")

    student = Student("S001", "Ana Pérez")
    for grade in (95.0, 88.5, 100, "Fifty", 150, -5, True):
        try_action(f"Agregar nota {grade!r}", student.add_grade, grade)

    print(student.summary_report())

    try_action("Eliminar nota por valor 88.5", student.remove_grade_by_value, 88.5)
    try_action("Eliminar nota por valor 70", student.remove_grade_by_value, 70)
    try_action("Eliminar nota por índice 0", student.remove_grade_by_index, 0)
    try_action("Eliminar nota por índice 9", student.remove_grade_by_index, 9)

    print(student.summary_report())

    failing = Student("S002", "Luis Mora")
    for grade in (40, 55.5):
        failing.add_grade(grade)
    print(failing.summary_report())

    print(Student("S003", "Sin Notas").summary_report())


if __name__ == "__main__":
    main()
